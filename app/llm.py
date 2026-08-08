import os, json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.environ["GROQ_API_KEY"], base_url="https://api.groq.com/openai/v1")

def call_model(messages: list[dict], retries: int = 2) -> dict:
    for attempt in range(retries + 1):
        resp = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            temperature=0.7,
            max_tokens=800,
            response_format={"type": "json_object"},  # forces valid JSON output
        )
        content = resp.choices[0].message.content

        if not content:
            continue  # empty response, retry

        content = content.strip()
        if content.startswith("```"):
            content = content.strip("`").lstrip("json").strip()

        try:
            return json.loads(content)
        except json.JSONDecodeError:
            continue  # malformed, retry

    # If every retry failed, never let the request crash — degrade gracefully
    return {
        "reply": "Sorry, could you rephrase that? Let's continue.",
        "done": False,
        "feedback": None,
    }