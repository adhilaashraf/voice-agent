# VOXEN — Voice-Controlled Local AI Agent

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![Streamlit](https://img.shields.io/badge/UI-Streamlit-red)
![Groq](https://img.shields.io/badge/API-Groq-orange)
![License](https://img.shields.io/badge/License-MIT-green)

VOXEN is a voice-controlled AI agent I built for the Mem0 internship
assignment. You talk to it — either by uploading an audio file or
recording live — and it figures out what you want and actually does it.
Write code, create files, summarize text, or just have a conversation.
The whole pipeline runs through a Streamlit UI that shows you every
step of what happened.

---

## Demo

Upload an audio file or hit record → VOXEN transcribes what you said,
detects your intent, and executes the action. Results show up instantly
in the UI along with the full session log.

---

## How it works

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

## What it can do

| Intent | What happens |
|---|---|
| Write Code | Generates code and saves it directly to the output/ folder |
| Create File | Creates a new file or folder inside output/ |
| Summarize | Reads the text and gives you a clean summary |
| General Chat | Answers your question conversationally |

---

## Project Structure

voice-agent/
├── app.py            # Streamlit UI — start here
├── stt.py            # Handles audio transcription
├── intent.py         # Classifies what the user wants
├── tools.py          # Does the actual work based on intent
├── config.py         # Your API keys — not pushed to GitHub
├── output/           # Everything generated goes here
├── requirements.txt  # Dependencies
└── README.md

---

## Getting it running

### 1. Clone the repo
```bash
git clone https://github.com/adhilaashraf/voice-agent.git
cd voice-agent
```

### 2. Install dependencies
```bash
pip install streamlit groq scipy numpy python-dotenv streamlit-audiorecorder
```

### 3. Set up your API key
Create a `config.py` file in the root folder and add this:
```python
GROQ_API_KEY = "your_groq_api_key_here"
WHISPER_MODEL = "whisper-large-v3"
LLM_MODEL = "llama-3.3-70b-versatile"
OUTPUT_FOLDER = "output"
```

You can get a free Groq API key at https://console.groq.com — no
credit card needed.

### 4. Run it
```bash
streamlit run app.py
```

---

## Models used

| Task | Model | Where |
|---|---|---|
| Speech-to-Text | whisper-large-v3 | Groq API |
| Intent Detection | llama-3.3-70b-versatile | Groq API |
| Code Generation | llama-3.3-70b-versatile | Groq API |
| Summarization | llama-3.3-70b-versatile | Groq API |

---

## Why I used Groq instead of running Whisper locally

The assignment suggests running a HuggingFace Whisper model locally,
and I did try that first. It didn't work out, and here's exactly why.

**My machine specs:**
- RAM: 8GB
- GPU: None (integrated graphics only)
- OS: Windows 11

**What went wrong with local Whisper:**

Memory was the first problem. Even whisper-tiny needs around 1GB just
to load, and whisper-large needs over 6GB. On a Windows machine with
8GB total, the OS and background processes already eat through 4-5GB
before you even start. The model kept crashing on load.

Speed was the second problem. Running Whisper on CPU without a GPU
means transcribing a 5-second audio clip takes somewhere between 30
and 90 seconds. That's not a voice agent anymore, that's just waiting.

The third issue was the dependency stack. Getting HuggingFace
transformers, torch, and torchaudio installed on Windows without a
GPU means pulling the CPU-only PyTorch build, which is 800MB+ and
caused several conflicts with other packages during setup.

**Why Groq works:**

Groq runs the exact same whisper-large-v3 model — the most accurate
version — on their LPU hardware. That same 5-second clip gets
transcribed in under a second. The quality is at least as good as
local, the speed is dramatically better, and there's a free tier
that doesn't even ask for a credit card.

The assignment also explicitly says — *"If your local machine cannot
run this model efficiently, you may use an API-based STT service like
Groq or OpenAI. If you choose this route, please document why in your
README."* — so this section is that documentation.

---

## A note on safety

Every file and piece of code this agent generates goes strictly into
the `output/` folder. It will not touch anything outside that
directory. I hardcoded that restriction in `tools.py` so there's no
way it accidentally writes somewhere it shouldn't.

---

## Everything else it does

- Upload audio files or record directly from the mic
- Transcribes using Whisper Large V3 (accurate even with background noise)
- Classifies intent with Llama 3.3 70B
- Generates working code and saves it automatically
- Keeps a session log with success/failure status for every request
- Handles errors without crashing — mic not available, bad audio,
  unrecognized intent — all caught and shown cleanly in the UI

---

## Tech stack

- **Frontend** — Streamlit with custom HTML/CSS
- **Speech-to-Text** — Groq Whisper API
- **LLM** — Groq Llama 3.3 70B
- **Language** — Python 3.10+
- **File I/O** — Python os module

---

## Author

**Athila Ashraf**
Built for the Mem0 AI/ML & Generative AI Developer Intern Assignment.

---

## License

MIT — use it, modify it, do whatever you want with it.
