from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.models import InterviewRequest, InterviewResponse
from app.session_store import get_or_create
from app.prompts import build_system_prompt
from app.llm import call_model

app = FastAPI()
app.mount("/static", StaticFiles(directory="static", html=True), name="static")

@app.post("/api/interview", response_model=InterviewResponse)
def interview(req: InterviewRequest):
    session = get_or_create(req.sessionId)

    if not session["history"]:
        if req.candidate is None:
            return InterviewResponse(reply="Missing candidate data to start interview.", done=True)
        system_prompt = build_system_prompt(req.candidate)
        session["history"].append({"role": "system", "content": system_prompt})
        session["history"].append({"role": "user", "content": "Begin the interview."})
    else:
        if req.message is None:
            return InterviewResponse(reply="Session already started — send a 'message' field to continue.", done=False)
        session["history"].append({"role": "user", "content": req.message})

    result = call_model(session["history"])
    session["history"].append({"role": "assistant", "content": result["reply"]})

    return InterviewResponse(**result)