import os
import base64
import tempfile
import traceback
import re

from flask import Flask, render_template, send_from_directory
from flask_socketio import SocketIO, emit

from .chat_stream import stream_chat_response, client as groq_client
from .tts import generate_tts_audio

from bntranslit import BNTransliteration
bn = BNTransliteration(r"C:\Users\25ikb\OneDrive\Desktop\translate_with_chatbot\backend\bntranslit_model.pth")

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/tts_audio/<filename>")
def serve_tts_audio(filename):
    return send_from_directory("templates", filename)

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(
        os.path.join(app.root_path, 'static'),
        'favicon.ico',
        mimetype='image/vnd.microsoft.icon'
    )

@socketio.on("connect")
def handle_connect():
    print("Client connected")

@socketio.on("disconnect")
def handle_disconnect():
    print("Client disconnected")

@socketio.on("user_message")
def handle_user_message(data):
    user_text = data.get("message", "").strip()
    print(f"Received user message: {user_text!r}")

    if not user_text:
        return emit("bot_text", {"text": "Sorry, I didn't catch that."})

    # 🔍 Attempt transliteration if Bangla-like keywords detected
    bangla_keywords = ["ami", "tumi", "ki", "bhalo", "keno", "kotha"]
    if any(re.search(rf"\b{kw}\b", user_text, re.IGNORECASE) for kw in bangla_keywords):
        try:
            print("Attempting transliteration before translation")
            user_text = bn.translit(user_text)
        except Exception:
            print("Transliteration failed; continuing with original text")

    # 1️⃣ Chat → Chinese translation
    try:
        translated = stream_chat_response(user_text) or "Sorry, I couldn't translate that."
        emit("bot_text", {"text": translated})
    except Exception:
        print("Error during translation:")
        traceback.print_exc()
        return emit("bot_text", {"text": "Oops, something went wrong translating."})

    # 2️⃣ Chinese → TTS
    try:
        wav_bytes, mp3_path = generate_tts_audio(translated)
        if not wav_bytes:
            return emit("bot_text", {"text": "I couldn't generate audio for that."})

        audio_b64 = base64.b64encode(wav_bytes).decode("utf-8")
        emit("bot_audio", {"audio": audio_b64})
    except Exception:
        print("Error during TTS generation:")
        traceback.print_exc()
        emit("bot_text", {"text": "Audio generation failed."})

@socketio.on("voice_message")
def handle_voice_message(data):
    audio_b64 = data.get("audio", "")
    if not audio_b64:
        emit("transcription", {"text": "⚠️ No audio data received."})
        return

    try:
        audio_bytes = base64.b64decode(audio_b64)
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
            tmp.write(audio_bytes)
            tmp.seek(0)

            response = groq_client.audio.transcriptions.create(
                model="whisper-large-v3",
                file=tmp,
                language="bn"
            )
            transcript = response.text.strip()

        os.remove(tmp.name)

        # Use preloaded transliteration model
        try:
            display_version = bn.translit(transcript)
        except Exception:
            display_version = transcript

        emit("transcription", {
            "text": f"User said: '{display_version}' (বাংলা)",
            "raw": transcript
        })

        # Forward to bot logic
        handle_user_message({"message": transcript})

    except Exception as e:
        traceback.print_exc()
        emit("transcription", {"text": "⚠️ Transcription failed."})

if __name__ == "__main__":
    socketio.run(app, debug=True)
