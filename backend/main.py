"""
Backend API for AI Meeting Notes Generator.

This FastAPI application accepts audio files of meetings, transcribes them
using OpenAI's Whisper model, and then summarizes the transcription into
structured meeting notes using LLaMA 2 via Ollama.
"""

import whisper
from fastapi import FastAPI, UploadFile, File
import requests
import json

# Load the Whisper speech recognition model at startup
# Using "base" model balances accuracy and speed for real-time transcription
model = whisper.load_model("base")

app = FastAPI()
OLLAMA_TIMEOUT_SECONDS = 1800

OLLAMA_API_URL = "http://localhost:11434/api/generate"


def read_ollama_stream(response: requests.Response) -> str:
    """Read Ollama's streamed NDJSON chunks into one response string."""
    chunks = []
    for line in response.iter_lines(decode_unicode=True):
        if not line:
            continue
        data = json.loads(line)
        chunks.append(data.get("response", ""))
        if data.get("done"):
            break
    return "".join(chunks).strip()


def call_ollama(payload: dict) -> str:
    """Call Ollama with streaming enabled so long local generations stay alive."""
    streamed_payload = {**payload, "stream": True}
    with requests.post(
        OLLAMA_API_URL,
        json=streamed_payload,
        timeout=(100, OLLAMA_TIMEOUT_SECONDS),
        stream=True,
    ) as response:
        response.raise_for_status()
        return read_ollama_stream(response)

@app.post("/transcribe/")
async def transcribe_audio(file: UploadFile = File(...)):
    """
    Transcribe an audio file to text.

    Uses OpenAI's Whisper model for speech-to-text transcription,
    then summarizes the transcription using LLaMA 2.

    Args:
        file: An uploaded audio file (MP3, WAV, etc.)

    Returns:
        A dictionary containing the transcribed text and summary
    """
    # Read the uploaded audio file contents into memory
    contents = await file.read()

    # Write the audio data to a temporary file
    # Whisper requires a file path rather than raw bytes for transcription
    with open("temp_audio.mp3", "wb") as f:
        f.write(contents)

    # Use Whisper to transcribe the audio file to text
    # The model automatically handles language detection and transcription
    result = model.transcribe("temp_audio.mp3")

    # Extract the transcribed text from the result dictionary
    transcription = result["text"]

    # Send the transcription to Ollama for summarization.
    # The helper streams chunks from Ollama, then returns one complete summary.
    summary = call_ollama({
        "model": "llama2",  # Using llama2 for summarization
        "prompt": f"Summarize this meeting transcription into key points:\n\n{transcription}",
    })

    # Return both transcription and summary to the frontend
    return {"transcription": transcription, "summary": summary}
