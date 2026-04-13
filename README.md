# VOXEN — Voice-Controlled Local AI Agent

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![Streamlit](https://img.shields.io/badge/UI-Streamlit-red)
![Groq](https://img.shields.io/badge/API-Groq-orange)
![License](https://img.shields.io/badge/License-MIT-green)

VOXEN is a voice-controlled AI agent that listens to your voice,
understands your intent, and executes real actions on your local
machine — all through a clean, modern UI.

---

## Demo

> Upload an audio file or record your voice → VOXEN transcribes it,
> detects your intent, and executes the action automatically.

---

## System Architecture

Audio Input (Upload / Microphone)
↓
Speech-to-Text (Groq Whisper API)
↓
Intent Detection (Groq Llama 3.3)
↓
Tool Execution Engine
├── Write Code   → saves to output/
├── Create File  → saves to output/
├── Summarize    → returns summary
└── General Chat → returns answer
↓
VOXEN Streamlit UI (displays results)

---

## Supported Intents

| Intent | What it does |
|---|---|
| Write Code | Generates code and saves it to output/ folder |
| Create File | Creates a new file or folder in output/ |
| Summarize | Summarizes the provided text |
| General Chat | Answers questions conversationally |

---

## Project Structure

voice-agent/
├── app.py            # Streamlit UI — main entry point
├── stt.py            # Speech-to-Text module
├── intent.py         # Intent Detection module
├── tools.py          # Tool Execution module
├── config.py         # API keys and settings (not pushed to GitHub)
├── output/           # All generated files are saved here
├── requirements.txt  # Python dependencies
└── README.md

---

## Setup Instructions

### 1. Clone the repository
```bash
git clone https://github.com/adhilaashraf/voice-agent.git
cd voice-agent
```

### 2. Install dependencies
```bash
pip install streamlit groq scipy numpy python-dotenv streamlit-audiorecorder
```

### 3. Create config.py and add your Groq API key
Create a file called `config.py` in the root folder:
```python
GROQ_API_KEY = "your_groq_api_key_here"
WHISPER_MODEL = "whisper-large-v3"
LLM_MODEL = "llama-3.3-70b-versatile"
OUTPUT_FOLDER = "output"
```

> Get your free Groq API key at https://console.groq.com

### 4. Run the app
```bash
streamlit run app.py
```

### 5. Open in browser

---

## Models Used

| Task | Model | Provider |
|---|---|---|
| Speech-to-Text | whisper-large-v3 | Groq API |
| Intent Detection | llama-3.3-70b-versatile | Groq API |
| Code Generation | llama-3.3-70b-versatile | Groq API |
| Summarization | llama-3.3-70b-versatile | Groq API |

---

## Hardware Workaround — Why Groq API instead of Local HuggingFace Whisper?

The assignment recommends using a HuggingFace model such as Whisper
or wav2vec locally. However, this project uses the **Groq API** for
both Speech-to-Text and LLM inference. Here is the detailed reason:

### Machine Specifications
- RAM: 8GB
- GPU: None (integrated graphics only)
- OS: Windows 11

### Why local Whisper failed on this machine

**1. Memory Issue**
Whisper models require significant RAM to load. The smallest Whisper
model (whisper-tiny) needs around 1GB of RAM just to load, while
whisper-base needs 1.5GB and whisper-large needs over 6GB. On an
8GB RAM machine running Windows, other system processes consume
around 4-5GB, leaving insufficient memory for the model to run
without crashing.

**2. Speed Issue**
Without a dedicated GPU, Whisper runs on CPU only. Transcribing
even a 5-second audio clip takes 30-90 seconds on CPU. This makes
the user experience completely unusable for a real-time voice agent.

**3. Dependency Conflicts**
Installing HuggingFace transformers, torch, and torchaudio on
Windows without a GPU requires the CPU-only version of PyTorch
which is over 800MB in size. This caused multiple dependency
conflicts during installation on this machine.

### Why Groq API is the right solution

**1. Same Whisper Model**
Groq API runs the exact same whisper-large-v3 model — the most
accurate version of Whisper. The transcription quality is identical
or better than running it locally.

**2. Extremely Fast**
Groq's LPU (Language Processing Unit) hardware processes audio and
text at speeds that are 10-100x faster than running on CPU locally.
A 5-second audio clip is transcribed in under 1 second.

**3. Free Tier Available**
Groq provides a generous free tier with no credit card required,
making it accessible for development and demonstration purposes.

**4. Assignment Explicitly Allows It**
The assignment states — "If your local machine cannot run this model
efficiently, you may use an API-based STT service like Groq or
OpenAI. If you choose this route, please document why in your README."
This section serves as that documentation.

---

## Safety

All file creation and code writing is strictly restricted to the
`output/` folder inside the project directory. The system will never
create, modify, or delete files outside this folder, preventing any
accidental system modifications.

---

## Features

- Two audio input methods — file upload and microphone recording
- Accurate speech-to-text using Whisper Large V3
- Smart intent classification using Llama 3.3 70B
- Automatic code generation and file saving
- Session history log with success/failure tracking
- Clean dark UI with animated visuals
- Graceful error handling for all edge cases

---

## Tech Stack

- **Frontend** — Streamlit with custom HTML/CSS
- **Speech-to-Text** — Groq Whisper API
- **LLM** — Groq Llama 3.3 70B
- **Language** — Python 3.10+
- **File I/O** — Python os module

---

## Author

**Athila Ashraf**
Built for Mem0 AI/ML & Generative AI Developer Intern Assignment

---

## License

MIT License — feel free to use and modify this project.
