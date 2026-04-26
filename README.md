# Project 5: AI Meeting Notes Generator

An AI-powered meeting notes generator that transcribes audio recordings and automatically generates structured meeting notes with summaries, action items, and transcripts. Perfect for teams, project managers, and anyone who needs to document meetings.

## Features

- **Audio Transcription**: Uses Whisper AI for accurate speech-to-text
- **Concise Summary**: Generates a brief overview of the meeting
- **Key Action Items**: Extracts actionable tasks and decisions
- **Full Transcript**: Provides complete text of the meeting
- **FastAPI Backend**: Efficient REST API for processing
- **Streamlit Frontend**: User-friendly interface for meeting documentation
- **Local Processing**: All transcription and analysis runs locally using Ollama LLMs - no external API dependencies

## Architecture

### Backend Components

1. **Audio Processor** (`backend/main.py`)
   - Handles audio file uploads
   - Manages transcription queue
   - Processes meeting recordings

2. **Transcription Service** (`backend/main.py`)
   - Uses Whisper AI for speech-to-text
   - Generates accurate transcripts
   - Handles various audio formats

3. **Meeting Analyzer** (`backend/main.py`)
   - Extracts key points from transcripts
   - Generates action items
   - Creates meeting summaries

### Frontend Components

1. **Streamlit UI** (`frontend/app.py`)
   - User interface for audio upload
   - Results display and visualization
   - Export functionality

2. **Reusable Components** (`frontend/components.py`)
   - Modular UI elements
   - Consistent styling and layout

## Installation

### Prerequisites

- Python 3.8 or higher
- Ollama installed and running (for local LLM inference)
- FFmpeg (for audio processing, if needed)

### Setup Steps

1. **Navigate to the project directory**:
   ```bash
   cd SchoolOfAI/Official/soai-05-meeting-notes
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Install and start Ollama** (if not already installed):
   ```bash
   # Install Ollama from https://ollama.com
   # Pull a model (llama2 is recommended)
   ollama pull llama2
   # Start Ollama service
   ollama serve
   ```

5. **Install Whisper** (if not already installed):
   ```bash
   pip install openai-whisper
   ```

## Running the Application

### Backend API

1. **Start the FastAPI backend**:
   ```bash
   uvicorn backend.main:app --reload
   ```

2. **Access the API**: Navigate to `http://localhost:8000` for API documentation

### Frontend UI

1. **Start the Streamlit application** (in a new terminal):
   ```bash
   streamlit run frontend/app.py
   ```

2. **Open your browser**: Navigate to `http://localhost:8501`

## Usage

### 1. Upload Meeting Recording

- Select an audio file (MP3, WAV, M4A, etc.)
- Or record directly in the browser
- Click "Upload" to process the audio

### 2. Generate Meeting Notes

- Click "Generate Notes" to start processing
- Wait for transcription and analysis
- View the structured results

### 3. Review Results

- **Summary**: Brief overview of the meeting
- **Action Items**: List of tasks and decisions
- **Full Transcript**: Complete text of the meeting
- **Key Points**: Important topics discussed

### 4. Export Results

- Copy notes for sharing
- Export as text or JSON
- Save for future reference

## Workflow

```
Upload Audio → Backend API → Whisper → Transcribe → LLaMA 2 → Generate Notes → Display Results
     ↓               ↓            ↓          ↓            ↓                ↓                  ↓
  Select file     FastAPI      Speech-to   Extract      Summarize    Show to
  or record      endpoint     Text       key points    user
```

## Configuration

### Environment Variables (Optional)

Create a `.env` file in the project root:

```env
OLLAMA_MODEL=llama2
OLLAMA_API_URL=http://localhost:11434/api/generate
```

### Ollama Models

The system supports any Ollama model. Recommended models:
- `llama2` - Good balance of speed and accuracy for summarization (default)

### Whisper Models

Whisper supports multiple models for different accuracy/speed tradeoffs:
- `tiny` - Fastest, less accurate
- `base` - Good balance
- `small` - More accurate, slower
- `medium` - Even more accurate
- `large` - Most accurate, slowest

## Project Structure

```
soai-05-meeting-notes/
├── backend/
│   └── main.py                  # FastAPI backend
├── frontend/
│   ├── app.py                    # Streamlit UI
│   └── components.py             # Reusable UI components
├── requirements.txt              # Python dependencies
└── README.md                   # This file
```

## Dependencies

- `fastapi` - Web API framework
- `uvicorn` - ASGI server
- `streamlit` - Web UI framework
- `openai-whisper` - Speech recognition
- `requests` - HTTP client for Ollama API
- `python-dateutil` - Date/time parsing

## Troubleshooting

### Ollama Connection Issues

If you see connection errors:
1. Verify Ollama is running: `ollama list`
2. Check the API URL: `curl http://localhost:11434/api/generate`
3. Ensure the model is pulled: `ollama pull llama2`

### Whisper Issues

If transcription fails:
1. Verify Whisper is installed: `pip list | grep whisper`
2. Check audio format is supported
3. Ensure audio quality is good
4. Try a different Whisper model size

### Backend API Issues

If the backend isn't responding:
1. Verify uvicorn is running: `ps aux | grep uvicorn`
2. Check the port isn't in use: `lsof -i :8000`
3. Review backend logs for errors

### Frontend Connection Issues

If the frontend can't connect to the backend:
1. Verify both services are running
2. Check the API URL in frontend/app.py
3. Ensure CORS is configured correctly

### Audio Processing Issues

If audio upload fails:
1. Check file format is supported
2. Verify file size isn't too large
3. Ensure audio quality is sufficient
4. Try a shorter recording

### Slow Performance

For faster processing:
1. Use a smaller Whisper model (tiny or base)
2. Reduce audio length if possible
3. Increase Ollama's GPU resources if available
4. Use a faster LLM model

## Use Cases

- **Team Meetings**: Document team discussions and decisions
- **Project Reviews**: Record and analyze project review meetings
- **Client Meetings**: Document client calls and requirements
- **Training Sessions**: Capture training content for reference
- **Interview Documentation**: Record interviews for later analysis
- **Personal Notes**: Voice-to-text for personal organization

## Important Notes

- All processing happens locally - no data is sent to external servers
- Transcription accuracy depends on audio quality and speaker clarity
- Meeting quality depends on the clarity of discussion
- Action items are AI-generated and should be verified
- This tool provides structure but not legal or business advice

## License

This project is part of the School of AI curriculum.
