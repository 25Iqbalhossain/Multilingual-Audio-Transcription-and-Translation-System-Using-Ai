
# tts.py
import os
import io
import requests
from pydub import AudioSegment
from datetime import datetime

ELEVENLABS_API_KEY 
VOICE_ID 

def generate_tts_audio(text: str):
    try:
        endpoint = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"
        headers  = {
            "xi-api-key": ELEVENLABS_API_KEY,
            "Content-Type": "application/json"
        }
        payload = {
            "text": text,
            "model_id": "eleven_monolingual_v1",
            "voice_settings": {"stability": 0.4, "similarity_boost": 0.8}
        }

        resp = requests.post(endpoint, headers=headers, json=payload, timeout=30)
        resp.raise_for_status()

        os.makedirs("templates", exist_ok=True)
        fname    = f"tts_{datetime.now():%Y%m%d%H%M%S%f}.mp3"
        mp3_path = os.path.join("templates", fname)
        with open(mp3_path, "wb") as f:
            f.write(resp.content)

        # Export WAV into a BytesIO buffer
        audio = AudioSegment.from_file(mp3_path, format="mp3")
        buf   = io.BytesIO()
        audio.export(buf, format="wav")
        wav_bytes = buf.getvalue()

        return wav_bytes, mp3_path

    except Exception as e:
        print(f"❌ TTS generation failed: {e}")
        return None, None
