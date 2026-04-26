"""
Frontend Application for AI Meeting Notes Generator.

This Streamlit app allows users to upload audio recordings of meetings.
The audio is transcribed using Whisper and then summarized into key points
using LLaMA 2 for easy documentation and sharing.
"""

import os
import sys

import streamlit as st
import requests

PACKAGE_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "..")
)
if PACKAGE_ROOT not in sys.path:
    sys.path.insert(0, PACKAGE_ROOT)

from components import render_app_footer, run_with_status_updates

st.title("AI Meeting Notes Generator")

uploaded_file = st.file_uploader("Upload meeting audio (MP3, WAV)...", type=["mp3", "wav", "m4a"])


if uploaded_file is not None:
    st.audio(uploaded_file, format="audio/wav")

    if st.button("Generate Notes"):
        files = {"file": uploaded_file.getvalue()}
        response = run_with_status_updates(
            lambda: requests.post(
                "http://localhost:8000/transcribe/",
                files=files
            ),
            start_message="Transcribing and summarizing your meeting..."
        )

        if response.status_code == 200:
            data = response.json()
            st.subheader("Transcription:")
            st.write(data.get("transcription", ""))
            st.subheader("Meeting Summary:")
            st.write(data.get("summary", ""))
        else:
            st.error("Error processing audio. Make sure the backend is running.")


render_app_footer()
