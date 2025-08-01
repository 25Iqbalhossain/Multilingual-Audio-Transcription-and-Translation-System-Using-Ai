
# chat_stream.py

import os
import groq
import re
from langdetect import detect, DetectorFactory

DetectorFactory.seed = 0

native_lang_names = {
    "en":    "English",
    "fr":    "Français",
    "bn":    "বাংলা",
    "hi":    "हिन्दी",
    "zh-cn": "简体中文",
    "es":    "Español",
    "ar":    "العربية",
    "ru":    "Русский",
    "de":    "Deutsch",
    "ja":    "日本語",
    "ko":    "한국어",
    "ur":    "اردو",
    "id":    "Bahasa Indonesia",   # ← ensure this is in your dict
}

os.environ.pop("SSL_CERT_FILE", None)


def clean_text(text: str) -> str:
    return re.sub(r"\*(.*?)\*", r"\1", text).replace("*", "")

def detect_language(text: str) -> str:
    try:
        return detect(text)
    except:
        return "unknown"

def get_native_language_name(code: str) -> str:
    return native_lang_names.get(code, code)

def stream_chat_response(prompt: str) -> str:
    lang_code = detect_language(prompt)
    native   = get_native_language_name(lang_code)
    print(f"\nUser said: {prompt!r} ({native})")

    try:
        response = client.chat.completions.create(
            model="meta-llama/llama-4-scout-17b-16e-instruct",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an AI translator. "
                        "Translate everything the user says into Simplified Chinese only—"
                        "no explanations, no markdown, no extra formatting."
                        "If he said bangla english and hindi whatever convert it into chinese."
                    )
                },
                {"role": "user", "content": prompt}
            ],
            stream=True,
            max_tokens=300
        )
    except Exception as e:
        print(f"❌ Groq API error: {e}")
        return ""    # never return None

    chunks = []
    try:
        for chunk in response:
            delta = chunk.choices[0].delta.content
            if delta:
                piece = clean_text(delta)
                print(piece, end="", flush=True)  # live console echo
                chunks.append(piece)
    except Exception as e:
        print(f"\n❌ Error reading streamed response: {e}")
        return ""

    print()  # newline after streaming
    return "".join(chunks)