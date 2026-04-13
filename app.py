import streamlit as st
import os
import tempfile
from stt import transcribe_audio
from intent import detect_intent, get_intent_label
from tools import execute_tool

st.set_page_config(
    page_title="VOXEN — Voice AI Agent",
    page_icon="🎙",
    layout="centered"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Mono:wght@300;400;500&display=swap');

* { font-family: 'Syne', sans-serif; }
code, pre { font-family: 'DM Mono', monospace !important; }

html, body, [data-testid="stAppViewContainer"] { color: #e8e6f0; }

[data-testid="stAppViewContainer"] {
    background-image: url("app/static/bg.jpg");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
    min-height: 100vh;
    position: relative;
}

[data-testid="stAppViewContainer"]::before {
    content: '';
    position: fixed;
    top: 0; left: 0;
    width: 100%; height: 100%;
    background: rgba(5, 5, 20, 0.78);
    pointer-events: none;
    z-index: 0;
}

[data-testid="stHeader"] { background: transparent; }
[data-testid="stSidebar"] { display: none; }
[data-testid="stAppViewContainer"] > div { position: relative; z-index: 1; }
section[data-testid="stMain"] > div { padding-top: 2rem; }

.hero-badge {
    display: inline-block;
    background: rgba(139,92,246,0.15);
    border: 1px solid rgba(139,92,246,0.4);
    color: #a78bfa;
    padding: 4px 14px;
    border-radius: 20px;
    font-size: 11px;
    letter-spacing: 3px;
    text-transform: uppercase;
    margin-bottom: 16px;
}

.hero-title {
    font-size: 64px;
    font-weight: 800;
    line-height: 1;
    letter-spacing: -2px;
    background: linear-gradient(135deg, #fff 0%, #a78bfa 50%, #60a5fa 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin: 0;
}

.hero-sub {
    font-size: 15px;
    color: #9ca3af;
    margin-top: 12px;
    letter-spacing: 0.3px;
    font-weight: 400;
}

.result-box {
    background: rgba(10,10,30,0.6);
    border: 1px solid rgba(139,92,246,0.25);
    border-radius: 12px;
    padding: 18px 22px;
    margin: 10px 0;
    font-size: 15px;
    color: #e8e6f0;
    line-height: 1.6;
    backdrop-filter: blur(10px);
}

.intent-badge {
    display: inline-block;
    background: linear-gradient(135deg, #7c3aed, #2563eb);
    color: white;
    padding: 8px 20px;
    border-radius: 30px;
    font-size: 13px;
    font-weight: 600;
    letter-spacing: 0.5px;
}

.step-number {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 28px; height: 28px;
    background: linear-gradient(135deg, #7c3aed, #2563eb);
    border-radius: 50%;
    font-size: 12px;
    font-weight: 700;
    color: white;
    margin-right: 10px;
}

.section-title {
    font-size: 13px;
    font-weight: 700;
    letter-spacing: 1px;
    text-transform: uppercase;
    color: #9ca3af;
    display: flex;
    align-items: center;
    gap: 8px;
    margin-bottom: 14px;
}

.card-label {
    font-size: 10px;
    letter-spacing: 3px;
    text-transform: uppercase;
    color: #6b7280;
    margin-bottom: 8px;
    font-weight: 600;
}

.divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(139,92,246,0.4), transparent);
    margin: 28px 0;
}

.stButton > button {
    background: linear-gradient(135deg, #7c3aed, #2563eb) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 12px 28px !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 600 !important;
    font-size: 14px !important;
    letter-spacing: 0.5px !important;
    width: 100% !important;
    transition: all 0.2s !important;
}
.stButton > button:hover {
    opacity: 0.85 !important;
    transform: translateY(-1px) !important;
}

div[data-testid="stFileUploader"] {
    background: rgba(10,10,30,0.5) !important;
    border: 1px dashed rgba(139,92,246,0.4) !important;
    border-radius: 12px !important;
    padding: 8px !important;
    backdrop-filter: blur(10px) !important;
}

[data-testid="stExpander"] {
    background: rgba(10,10,30,0.5) !important;
    border: 1px solid rgba(255,255,255,0.07) !important;
    border-radius: 10px !important;
    backdrop-filter: blur(10px) !important;
}

.stSpinner > div { border-top-color: #7c3aed !important; }
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: #7c3aed; border-radius: 4px; }

/* ── Custom toggle buttons ── */
.toggle-row {
    display: flex;
    gap: 12px;
    margin-bottom: 20px;
}

.toggle-btn {
    flex: 1;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 8px;
    padding: 22px 16px;
    border-radius: 18px;
    cursor: pointer;
    font-family: 'Syne', sans-serif;
    font-weight: 700;
    border: none;
    outline: none;
    min-height: 110px;
    transition: all 0.3s cubic-bezier(0.4,0,0.2,1);
    background-size: 200% 200%;
}

.toggle-btn .btn-icon  { font-size: 28px; line-height: 1; }
.toggle-btn .btn-title { font-size: 14px; font-weight: 700; letter-spacing: 0.3px; }
.toggle-btn .btn-sub   { font-size: 11px; font-weight: 400; opacity: 0.8; }

/* UPLOAD — hot pink → violet → indigo */
.upload-btn {
    background: linear-gradient(135deg, #f43f5e, #a855f7, #6366f1);
    border: 2px solid rgba(244,63,94,0.6);
    color: #fff;
    box-shadow: 0 0 36px rgba(244,63,94,0.4), 0 8px 28px rgba(99,102,241,0.35);
    text-shadow: 0 1px 6px rgba(0,0,0,0.3);
    animation: gradpulse 3s ease infinite;
}
.upload-btn:hover {
    transform: translateY(-4px) scale(1.03);
    box-shadow: 0 0 56px rgba(244,63,94,0.6), 0 12px 40px rgba(99,102,241,0.5);
}
.upload-btn.inactive {
    background: linear-gradient(135deg, rgba(244,63,94,0.12), rgba(168,85,247,0.12), rgba(99,102,241,0.12));
    border: 2px solid rgba(244,63,94,0.2);
    color: rgba(255,255,255,0.4);
    box-shadow: none;
    text-shadow: none;
    animation: none;
}
.upload-btn.inactive:hover {
    background: linear-gradient(135deg, rgba(244,63,94,0.25), rgba(168,85,247,0.25), rgba(99,102,241,0.25));
    color: rgba(255,255,255,0.7);
    border-color: rgba(244,63,94,0.4);
    transform: translateY(-2px);
}

/* MIC — cyan → blue → violet */
.mic-btn {
    background: linear-gradient(135deg, #06b6d4, #3b82f6, #8b5cf6);
    border: 2px solid rgba(6,182,212,0.6);
    color: #fff;
    box-shadow: 0 0 36px rgba(6,182,212,0.4), 0 8px 28px rgba(59,130,246,0.35);
    text-shadow: 0 1px 6px rgba(0,0,0,0.3);
    animation: gradpulse 3s ease infinite reverse;
}
.mic-btn:hover {
    transform: translateY(-4px) scale(1.03);
    box-shadow: 0 0 56px rgba(6,182,212,0.6), 0 12px 40px rgba(59,130,246,0.5);
}
.mic-btn.inactive {
    background: linear-gradient(135deg, rgba(6,182,212,0.12), rgba(59,130,246,0.12), rgba(139,92,246,0.12));
    border: 2px solid rgba(6,182,212,0.2);
    color: rgba(255,255,255,0.4);
    box-shadow: none;
    text-shadow: none;
    animation: none;
}
.mic-btn.inactive:hover {
    background: linear-gradient(135deg, rgba(6,182,212,0.25), rgba(59,130,246,0.25), rgba(139,92,246,0.25));
    color: rgba(255,255,255,0.7);
    border-color: rgba(6,182,212,0.4);
    transform: translateY(-2px);
}

@keyframes gradpulse {
    0%, 100% { box-shadow: 0 0 36px rgba(244,63,94,0.4), 0 8px 28px rgba(99,102,241,0.35); }
    50%       { box-shadow: 0 0 52px rgba(244,63,94,0.65), 0 8px 36px rgba(99,102,241,0.55); }
}
</style>
""", unsafe_allow_html=True)

# ── Hero ─────────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center; padding: 40px 0 20px;">
    <div class="hero-badge">Voice Intelligence Platform</div>
    <h1 class="hero-title">VOXEN</h1>
    <p class="hero-sub">Speak. Understand. Execute — your voice, turned into action.</p>
    <div style="margin: 28px auto; width: 180px; height: 180px;">
        <svg viewBox="0 0 220 220" xmlns="http://www.w3.org/2000/svg" style="width:100%;height:100%;">
            <defs>
                <radialGradient id="coreGrad" cx="50%" cy="50%" r="50%">
                    <stop offset="0%" stop-color="#a78bfa"/>
                    <stop offset="100%" stop-color="#2563eb"/>
                </radialGradient>
                <radialGradient id="glowGrad" cx="50%" cy="50%" r="50%">
                    <stop offset="0%" stop-color="#7c3aed" stop-opacity="0.4"/>
                    <stop offset="100%" stop-color="#7c3aed" stop-opacity="0"/>
                </radialGradient>
                <filter id="blur1"><feGaussianBlur stdDeviation="6"/></filter>
            </defs>
            <circle cx="110" cy="110" r="100" fill="url(#glowGrad)" filter="url(#blur1)">
                <animate attributeName="r" values="90;105;90" dur="3s" repeatCount="indefinite"/>
                <animate attributeName="opacity" values="0.6;1;0.6" dur="3s" repeatCount="indefinite"/>
            </circle>
            <circle cx="110" cy="110" r="90" fill="none" stroke="rgba(139,92,246,0.3)" stroke-width="1" stroke-dasharray="8 6">
                <animateTransform attributeName="transform" type="rotate" from="0 110 110" to="360 110 110" dur="12s" repeatCount="indefinite"/>
            </circle>
            <circle cx="110" cy="110" r="72" fill="none" stroke="rgba(96,165,250,0.4)" stroke-width="1" stroke-dasharray="4 8">
                <animateTransform attributeName="transform" type="rotate" from="360 110 110" to="0 110 110" dur="8s" repeatCount="indefinite"/>
            </circle>
            <circle cx="110" cy="20" r="5" fill="#a78bfa">
                <animateTransform attributeName="transform" type="rotate" from="0 110 110" to="360 110 110" dur="6s" repeatCount="indefinite"/>
                <animate attributeName="opacity" values="1;0.4;1" dur="6s" repeatCount="indefinite"/>
            </circle>
            <circle cx="110" cy="200" r="4" fill="#60a5fa">
                <animateTransform attributeName="transform" type="rotate" from="0 110 110" to="360 110 110" dur="9s" repeatCount="indefinite"/>
                <animate attributeName="opacity" values="0.4;1;0.4" dur="9s" repeatCount="indefinite"/>
            </circle>
            <circle cx="20" cy="110" r="3" fill="#34d399">
                <animateTransform attributeName="transform" type="rotate" from="0 110 110" to="-360 110 110" dur="7s" repeatCount="indefinite"/>
            </circle>
            <circle cx="110" cy="110" r="54" fill="url(#coreGrad)" opacity="0.95">
                <animate attributeName="r" values="52;56;52" dur="3s" repeatCount="indefinite"/>
            </circle>
            <circle cx="110" cy="110" r="40" fill="white" opacity="0.07">
                <animate attributeName="r" values="38;44;38" dur="3s" repeatCount="indefinite"/>
                <animate attributeName="opacity" values="0.05;0.12;0.05" dur="3s" repeatCount="indefinite"/>
            </circle>
            <rect x="102" y="88" width="16" height="24" rx="8" fill="white" opacity="0.95"/>
            <path d="M96 112 Q96 126 110 126 Q124 126 124 112" fill="none" stroke="white" stroke-width="2.5" stroke-linecap="round" opacity="0.95"/>
            <line x1="110" y1="126" x2="110" y2="134" stroke="white" stroke-width="2.5" stroke-linecap="round" opacity="0.95"/>
            <line x1="104" y1="134" x2="116" y2="134" stroke="white" stroke-width="2.5" stroke-linecap="round" opacity="0.95"/>
            <rect x="72" y="106" width="4" height="8" rx="2" fill="#a78bfa" opacity="0.8">
                <animate attributeName="height" values="8;18;8" dur="1.2s" repeatCount="indefinite"/>
                <animate attributeName="y" values="106;101;106" dur="1.2s" repeatCount="indefinite"/>
            </rect>
            <rect x="80" y="102" width="4" height="16" rx="2" fill="#a78bfa" opacity="0.9">
                <animate attributeName="height" values="16;6;16" dur="0.9s" repeatCount="indefinite"/>
                <animate attributeName="y" values="102;107;102" dur="0.9s" repeatCount="indefinite"/>
            </rect>
            <rect x="144" y="106" width="4" height="8" rx="2" fill="#60a5fa" opacity="0.8">
                <animate attributeName="height" values="8;20;8" dur="1.0s" repeatCount="indefinite"/>
                <animate attributeName="y" values="106;100;106" dur="1.0s" repeatCount="indefinite"/>
            </rect>
            <rect x="136" y="103" width="4" height="14" rx="2" fill="#60a5fa" opacity="0.9">
                <animate attributeName="height" values="14;5;14" dur="1.4s" repeatCount="indefinite"/>
                <animate attributeName="y" values="103;108;103" dur="1.4s" repeatCount="indefinite"/>
            </rect>
        </svg>
    </div>
</div>
<div class="divider"></div>
""", unsafe_allow_html=True)

# ── Session state ─────────────────────────────────────────────
if "history" not in st.session_state:
    st.session_state.history = []
if "input_method" not in st.session_state:
    st.session_state.input_method = "Upload Audio File"
if "audio_file_path" not in st.session_state:
    st.session_state.audio_file_path = None
if "uploaded_file_name" not in st.session_state:
    st.session_state.uploaded_file_name = None

# ── Audio Input ───────────────────────────────────────────────
st.markdown("""
<div class="section-title">
    <span class="step-number">1</span> Audio Input
</div>
""", unsafe_allow_html=True)

is_upload = st.session_state.input_method == "Upload Audio File"

upload_cls = "toggle-btn upload-btn" + ("" if is_upload else " inactive")
mic_cls    = "toggle-btn mic-btn"    + ("" if not is_upload else " inactive")

# Beautiful HTML toggle buttons — onclick triggers hidden st.button
st.markdown(f"""
<div class="toggle-row">
  <button class="{upload_cls}" onclick="window.parent.document.querySelectorAll('[data-testid=stButton] button')[0].click()">
    <span class="btn-icon">☁️</span>
    <span class="btn-title">Upload Audio File</span>
    <span class="btn-sub">wav · mp3 · m4a · ogg</span>
  </button>
  <button class="{mic_cls}" onclick="window.parent.document.querySelectorAll('[data-testid=stButton] button')[1].click()">
    <span class="btn-icon">🎙️</span>
    <span class="btn-title">Record from Microphone</span>
    <span class="btn-sub">live capture</span>
  </button>
</div>
""", unsafe_allow_html=True)

# Hidden trigger buttons (invisible, wired via onclick above)
col1, col2 = st.columns(2)
with col1:
    if st.button("__upload__", key="btn_upload"):
        st.session_state.input_method = "Upload Audio File"
        st.session_state.audio_file_path = None
        st.session_state.uploaded_file_name = None
        st.rerun()
with col2:
    if st.button("__mic__", key="btn_mic"):
        st.session_state.input_method = "Record from Microphone"
        st.session_state.audio_file_path = None
        st.session_state.uploaded_file_name = None
        st.rerun()

# Push trigger buttons off screen
st.markdown("""
<style>
div[data-testid="stHorizontalBlock"] div[data-testid="stButton"] button {
    position: fixed !important;
    top: -999px !important;
    left: -999px !important;
    width: 1px !important;
    height: 1px !important;
    opacity: 0 !important;
    pointer-events: none !important;
}
</style>
""", unsafe_allow_html=True)

input_method = st.session_state.input_method

if input_method == "Upload Audio File":
    uploaded_file = st.file_uploader(
        "Upload audio",
        type=["wav", "mp3", "m4a", "ogg"],
        label_visibility="collapsed"
    )
    if uploaded_file:
        if uploaded_file.name != st.session_state.uploaded_file_name:
            suffix = "." + uploaded_file.name.split(".")[-1]
            with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
                tmp.write(uploaded_file.read())
                st.session_state.audio_file_path = tmp.name
                st.session_state.uploaded_file_name = uploaded_file.name
        st.audio(uploaded_file)
        st.markdown('<div class="result-box">✦ Audio loaded and ready to process</div>', unsafe_allow_html=True)
    else:
        st.session_state.audio_file_path = None
        st.session_state.uploaded_file_name = None

elif input_method == "Record from Microphone":
    try:
        from audiorecorder import audiorecorder
        audio = audiorecorder("⬤  Start Recording", "◼  Stop Recording")
        if len(audio) > 0:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
                audio.export(tmp.name, format="wav")
                st.session_state.audio_file_path = tmp.name
            st.audio(audio.export().read())
            st.markdown('<div class="result-box">✦ Recording captured successfully</div>', unsafe_allow_html=True)
    except Exception:
        st.warning("Microphone unavailable — please use file upload instead.")

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

audio_file_path = st.session_state.audio_file_path

# ── Process ───────────────────────────────────────────────────
if audio_file_path:
    st.markdown("""
    <div class="section-title">
        <span class="step-number">2</span> Process & Execute
    </div>
    """, unsafe_allow_html=True)

    if st.button("▶  Run VOXEN Agent", use_container_width=True):

        with st.spinner("Transcribing audio..."):
            transcribed_text = transcribe_audio(audio_file_path)

        st.markdown('<div class="card-label">What you said</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="result-box">❝ {transcribed_text} ❞</div>', unsafe_allow_html=True)

        with st.spinner("Analysing intent..."):
            intent_data = detect_intent(transcribed_text)

        intent = intent_data.get("intent", "chat")
        intent_label = get_intent_label(intent)

        st.markdown('<div class="card-label" style="margin-top:20px;">Detected intent</div>', unsafe_allow_html=True)
        st.markdown(f'<div style="margin:8px 0 16px;"><span class="intent-badge">{intent_label}</span></div>', unsafe_allow_html=True)

        with st.expander("View raw intent data"):
            st.json(intent_data)

        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

        with st.spinner("Executing action..."):
            result = execute_tool(intent_data, transcribed_text)

        st.markdown('<div class="card-label">Action taken</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="result-box">⚡ {result.get("action","")}</div>', unsafe_allow_html=True)

        st.markdown('<div class="card-label" style="margin-top:20px;">Output</div>', unsafe_allow_html=True)
        if intent == "write_code":
            st.code(result.get("output", ""), language="python")
        else:
            st.markdown(f'<div class="result-box">{result.get("output","")}</div>', unsafe_allow_html=True)

        if result.get("success"):
            st.success("✦ Action completed successfully")
        else:
            st.error("✦ Something went wrong")

        st.session_state.history.append({
            "transcription": transcribed_text,
            "intent": intent_label,
            "action": result.get("action", ""),
            "output": result.get("output", ""),
            "success": result.get("success", False)
        })

        try:
            os.unlink(audio_file_path)
        except:
            pass
        st.session_state.audio_file_path = None
        st.session_state.uploaded_file_name = None

# ── Session History ───────────────────────────────────────────
if st.session_state.history:
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="section-title">
        <span class="step-number">✦</span> Session Log
    </div>
    """, unsafe_allow_html=True)

    for i, item in enumerate(reversed(st.session_state.history)):
        dot = '🟢' if item['success'] else '🔴'
        with st.expander(f"{dot}  Request #{len(st.session_state.history) - i} — {item['intent']}"):
            st.markdown(f'<div class="card-label">You said</div><div class="result-box">{item["transcription"]}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="card-label" style="margin-top:12px;">Action</div><div class="result-box">{item["action"]}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="card-label" style="margin-top:12px;">Output</div><div class="result-box">{item["output"][:300]}{"..." if len(item["output"])>300 else ""}</div>', unsafe_allow_html=True)

# ── Footer ────────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center; padding: 48px 0 24px; color: #6b7280; font-size: 12px; letter-spacing: 1px;">
    VOXEN v1.0 &nbsp;·&nbsp; Voice Intelligence Platform
</div>
""", unsafe_allow_html=True)