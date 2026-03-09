# LearnSphere - Generative AI-Powered Machine Learning Learning System

## Setup Instructions

### 1. Install Dependencies
```
pip install -r requirements.txt
```

### 2. Configure API Key
- Copy `.env.example` to `.env`
- Add your Google Gemini API key:
```
GEMINI_API_KEY=your_key_here
```
Get your key from: https://ai.google.dev/

### 3. Run the Application
```
python app.py
```

### 4. Open in Browser
```
http://localhost:5000
```

---

## Project Structure
```
learnsphere/
├── app.py              # Main Flask application
├── genai_utils.py      # Gemini AI integration
├── audio_utils.py      # Text-to-speech (gTTS)
├── image_utils.py      # Image generation
├── code_executor.py    # Code generation + dependency detection
├── requirements.txt    # Python dependencies
├── .env                # API keys (create from .env.example)
├── templates/
│   ├── base.html       # Base layout
│   ├── index.html      # Home dashboard
│   ├── text.html       # Text explanation page
│   ├── code.html       # Code generation page
│   ├── audio.html      # Audio lesson page
│   └── visual.html     # Visual diagram page
└── generated/
    ├── audio/          # Generated MP3 files
    ├── code/           # Generated Python files
    └── images/         # Generated diagram images
```

## Features
- Text Explanation — Structured ML concept breakdowns (Beginner / Intermediate / Comprehensive)
- Code Generation — Executable Python with dependency detection and Colab instructions
- Audio Lessons — MP3 conversational lessons via gTTS
- Visual Diagrams — Educational diagrams via Gemini Image Generation

## Tech Stack
- Backend: Flask (Python)
- AI: Google Gemini 2.0 Flash
- TTS: gTTS
- Frontend: HTML5, CSS3, JavaScript
