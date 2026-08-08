sessions: dict[str, dict] = {}

def get_or_create(session_id: str) -> dict:
    if session_id not in sessions:
        sessions[session_id] = {"history": [], "days_covered": set(), "question_count": 0}
    return sessions[session_id]