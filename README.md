# Multilingual Audio Transcription and Translation System

This system processes spoken input in **Bangla**, **English**, or **Hindi**, transcribes it using Whisper, translates the transcript into **Chinese** using a Large Language Model (LLM) via the **Grok API**, and then generates spoken Chinese output using **ElevenLabs TTS**.

---

## 🔧 Technologies Used

- **Whisper (STD Models)**: For automatic speech recognition (ASR) of Bangla, English, and Hindi audio.
- **Grok API**: To access a powerful large language model for translation into Chinese.
- **ElevenLabs TTS**: For high-quality Chinese text-to-speech output.
- **Python**: The primary programming language used to orchestrate the pipeline.

---

## 🚀 Features

- Supports speech input in **Bangla**, **English**, and **Hindi**
- Uses Whisper ASR for accurate multilingual transcription
- Translates transcripts into **Chinese** using an LLM via the Grok API
- Outputs natural-sounding Chinese speech via ElevenLabs TTS
- Modular design for easy integration and scaling

---

## 📁 Project Structure

multilingual-translator/
│
├── audio_input/ # Input audio files
├── transcriptions/ # Transcribed text
├── translations/ # Chinese translations
├── tts_output/ # Final Chinese audio files
│
├── whisper_transcribe.py # Handles transcription using Whisper
├── translate_with_grok.py # Calls Grok API for translation
├── tts_with_elevenlabs.py # Converts Chinese text to speech
├── main.py # Orchestration script
│
└── README.md # Project documentation



## ⚙️ How It Works

1. **Input**: An audio file in Bangla, English, or Hindi is uploaded.
2. **Transcription**: `whisper_transcribe.py` uses STD Whisper models to convert speech to text.
3. **Translation**: `translate_with_grok.py` sends the transcription to the Grok API, returning the Chinese translation.
4. **Text-to-Speech**: `tts_with_elevenlabs.py` uses ElevenLabs API to synthesize the Chinese translation into audio.
5. **Output**: The system outputs a natural-sounding Chinese audio file.

---

## 🧪 Example Usage

```bash
python main.py --input_path ./audio_input/sample_hindi.wav



🔑 API Keys
You will need the following API keys:

Grok API Key – for LLM translation

ElevenLabs API Key – for TTS synthesis

Set them as environment variables or in a .env file:

📌 Requirements
Python 3.8+

