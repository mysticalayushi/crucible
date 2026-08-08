# AI Usage Log — Crucible

All prompts below were sent to Claude (Anthropic) during the ABTalks Vibe Code Hackathon build window.

## Problem Selection

Prompt: Asked to compare the two hackathon problem statements (Interview Agent vs. Autonomous AI Creator) given the provided curriculum.json, candidates.json, technical-spec.md, and a Q&A PDF — specifically which needed fewer API keys and was more realistic to finish solo in one day.
→ Got a side-by-side comparison and a recommendation to build the Interview Agent, with reasoning around API key count, hosting risk, and testability within a single day.

## Naming & Architecture

Prompt: Asked for creative name ideas for the interview agent project (to double as the repo name), then a full step-by-step build plan — architecture choice, folder structure, and starter code.
→ Landed on "Crucible." Got a FastAPI + Groq architecture plan, full folder structure, and initial code for main.py, llm.py, prompts.py, session_store.py, models.py.

## Windows Folder Setup

Prompt: Asked for the folder/file creation commands specifically for Windows (PowerShell), in a single line.
→ Got a PowerShell one-liner using New-Item to scaffold the full project structure.

## Environment Setup

Prompt: Pasted a "Python was not found" error after running `python3 -m venv .venv`.
→ Diagnosed the Windows Store alias intercepting `python3`; recommended using `python` instead and disabling the App Execution Alias.

Prompt: "How to create Grok API key step by step?"
→ Clarified Groq vs. Grok (xAI) naming confusion, then gave a step-by-step console.groq.com signup and key-generation walkthrough.

## Backend Debugging

Prompt: Reported uvicorn appeared "stuck" after startup (with a screenshot of the VS Code terminal showing "Application startup complete").
→ Explained this is normal idle-server behavior, not a hang, and gave test commands (curl / Invoke-RestMethod) to confirm the server was actually responding.

Prompt: Pasted a `KeyError: 'GROQ_API_KEY'` traceback.
→ Diagnosed a missing/misconfigured .env file; walked through creating .env from .env.example and verifying dotenv could read it.

Prompt: Pasted an `openai.BadRequestError` ('messages.3.content' not nullable) traceback.
→ Diagnosed a session-reuse bug: resending a "start interview" request against an already-started session appended a null message. Added guard clauses in main.py to handle missing `candidate`/`message` fields gracefully.

Prompt: Pasted a `json.decoder.JSONDecodeError: Expecting value` traceback occurring intermittently mid-interview.
→ Diagnosed inconsistent/empty JSON output from the Groq model. Rewrote llm.py to use `response_format={"type": "json_object"}`, added retry logic, and a graceful fallback response instead of a 500 error.

Prompt: Reported PowerShell variable/session confusion across multiple terminal windows causing repeated "Field required" and "Session already started" errors during manual testing.
→ Explained PowerShell variable scope across terminal sessions; recommended a reusable test_request.ps1 script for consistent fresh-session testing.

Prompt: Confirmed a full manual interview run completed successfully across 4 curriculum days (Embeddings, Vector Databases, Retrieval & Matching Engine, Prompt Engineering) and asked to verify the final `done`/`feedback` fields.
→ Confirmed the response contract matched the technical spec; flagged that question count should be checked against the 8-question minimum.

## Frontend

Prompt: Asked for the static/index.html chat UI to replace manual PowerShell testing.
→ Built a full single-page chat interface: candidate dropdown (loaded from data/candidates.json), message thread, input box, and a structured feedback panel shown when the interview ends. Also added a `/data` static mount in main.py so the frontend could fetch candidates.json directly.

## Git & Deployment

Prompt: Reported duplicate .env/.env.example files, with the real Groq API key mistakenly left in .env.example, plus a "fatal: not a git repository" error on `git add .` (with a screenshot of the VS Code file explorer and terminal).
→ Flagged the exposed key in .env.example as a real leak risk and recommended rotating the key; walked through `git init`, `git remote add origin`, and correct commit/push sequence.

Prompt: Pasted a malformed remote URL error ("Repository not found").
→ Diagnosed a missing repo-name segment in the remote URL; corrected it via `git remote remove origin` + `git remote add origin` with the proper GitHub URL.

Prompt: Pasted a "failed to push some refs... fetch first" rejection.
→ Diagnosed a pre-existing auto-generated commit on the GitHub remote (likely from repo initialization with a README); walked through `git pull --allow-unrelated-histories`, resolving the merge conflict, and pushing again.

Prompt: Asked for a complete AI Usage Log for PROMPTS.md based on this conversation, plus commands to commit the index.html and main.py changes made after the initial commit.
→ Produced this log and the follow-up git commands to commit the remaining frontend and backend changes.