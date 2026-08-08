# Crucible 🎯
### AI-Powered Technical Interview Agent

<div align="center">

![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Groq](https://img.shields.io/badge/Groq-LLM%20Inference-F55036?style=for-the-badge&logo=lightning&logoColor=white)
![Render](https://img.shields.io/badge/Render-Deployed-46E3B7?style=for-the-badge&logo=render&logoColor=white)
![Status](https://img.shields.io/badge/Status-Submitted-22C55E?style=for-the-badge)

<br/>

**A conversational AI agent that conducts personalized, adaptive technical interviews based on a candidate's actual learning journey through a 31-day AI engineering cohort — then delivers structured, actionable feedback.**

[**🚀 Live Demo**](https://crucible-ib0j.onrender.com/) &nbsp;|&nbsp; [**📄 AI Usage Log**](PROMPTS.md)

</div>

---

## 📌 The Problem

After completing an intensive AI engineering cohort, learners can build the systems — but struggle to confidently *explain* the engineering decisions behind them in a real interview setting. Crucible closes that gap: it's an interviewer that already knows exactly what each candidate built, what they struggled with, and what they skipped — and asks accordingly.

---

## 🚀 Live Demo

**[https://crucible-ib0j.onrender.com/](https://crucible-ib0j.onrender.com/)**

> ⚠️ **First request may take up to a minute.** This is deployed on Render's free tier, which spins the server down after periods of inactivity. The first request wakes it back up; every request after that is fast.

---

## ✨ What It Does

- 🎯 **Personalizes to each candidate** — pulls their actual completed missions, attempts, and skipped topics from `candidates.json` to decide what to ask
- 💬 **Conducts a real multi-turn interview** — minimum 8 questions, spanning at least 4 distinct curriculum days
- 🧠 **Generates genuine follow-ups** — every next question reacts to what the candidate just said, not a fixed script
- 🧵 **Maintains full conversation context** — session-based, so the model always knows what's already been asked and answered
- 📋 **Produces structured feedback on completion** — a summary, strengths, gaps, and next steps, generated from the actual conversation

---

## 🛠️ Tech Stack

| Category | Tool |
|---|---|
| 🐍 Backend | Python 3.11, FastAPI |
| ⚡ LLM Inference | Groq (Llama 3.3 70B, OpenAI-compatible SDK) |
| 🌐 Frontend | Vanilla HTML/CSS/JS (no build step) |
| ☁️ Deployment | Render |
| 🗃️ State | In-memory session store (per technical spec — no persistence required) |

---

## 📁 Project Structure

```text
crucible/
├── app/
│   ├── main.py            # FastAPI app, /api/interview route, root redirect
│   ├── llm.py             # Groq client — JSON-mode enforced, retry + fallback
│   ├── prompts.py         # Builds the interviewer system prompt from curriculum + candidate data
│   ├── session_store.py   # In-memory per-session conversation state
│   └── models.py          # Pydantic request/response schemas
│
├── data/
│   ├── curriculum.json    # 31-day cohort curriculum
│   └── candidates.json    # Candidate mission history and learning signals
│
├── static/
│   └── index.html         # Chat UI — candidate picker, live conversation, feedback panel
│
├── PROMPTS.md             # Full AI usage log
├── requirements.txt
└── .env.example
```

---

## 🔌 API Contract

Implements the single required endpoint exactly as defined in the technical spec:
POST /api/interview
**Start a session:**
```json
{
  "sessionId": "abc-123",
  "candidate": { ...candidate object from candidates.json... }
}
```

**Continue a session:**
```json
{
  "sessionId": "abc-123",
  "message": "candidate's answer"
}
```

**Response (mid-interview):**
```json
{
  "reply": "...",
  "done": false
}
```

**Response (interview complete):**
```json
{
  "reply": "...",
  "done": true,
  "feedback": {
    "summary": "...",
    "strengths": ["..."],
    "gaps": ["..."],
    "next": ["..."]
  }
}
```

No authentication required, per spec.

---

## 🧠 How It Works

1. On the first request, the candidate's `passed` missions are cross-referenced against `curriculum.json` to build a personalized system prompt — the model only asks about topics the candidate actually completed.
2. The model is instructed to ask one question at a time, generate a genuine follow-up before switching topics, cover at least 8 questions across at least 4 curriculum days, and adapt difficulty based on the candidate's attempt counts and signals.
3. Every response is forced into strict JSON via Groq's `response_format: json_object`, with retry logic and a graceful fallback if the model ever returns malformed output — so a parsing hiccup never crashes the interview mid-conversation.
4. Once the model determines enough ground has been covered, it sets `done: true` and generates the structured feedback object in the same turn.

---

## ▶️ Run Locally

```bash
git clone https://github.com/mysticalayushi/crucible.git
cd crucible

python -m venv .venv
.venv\Scripts\Activate.ps1        # Windows PowerShell
# source .venv/bin/activate       # macOS/Linux

pip install -r requirements.txt

cp .env.example .env              # then add your own GROQ_API_KEY
uvicorn app.main:app --reload
```

Open `http://127.0.0.1:8000/` — it redirects to the chat UI.

Get a free Groq API key at [console.groq.com](https://console.groq.com) — no credit card required.

---

## ⚠️ Known Limitations

- **Cold starts** on Render's free tier (see Live Demo note above)
- **No persistence** — conversation state lives in memory and resets on server restart (intentional, per the spec's "out of scope" list)
- **Single-process session store** — fine for this scope; a production version would move to Redis or similar for multi-instance deployments

---

## 🔭 Future Improvements

- [ ] Move session state to Redis for horizontal scaling
- [ ] Add streaming responses for a more natural typing-indicator feel
- [ ] Voice input/output
- [ ] Persist interview transcripts for candidate progress tracking over time

---

## 📋 Project Info

| Field | Detail |
|---|---|
| 👩‍💻 Built by | Ayushi Rai |
| 🏆 Event | ABTalks Vibe Code Hackathon |
| 🤖 AI Tool Used | Claude (Anthropic) — full log in [PROMPTS.md](PROMPTS.md) |
| 📅 Date | August 2026 |

---

<div align="center">
<sub>Built solo, end-to-end, during the hackathon build window.</sub>
</div>