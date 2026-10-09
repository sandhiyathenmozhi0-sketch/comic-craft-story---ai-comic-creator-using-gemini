import os
from google import genai

def generate_story(outline: list[dict], character_name: str, tone: str) -> str:
    """Expand the panel outline into readable narration/dialogue while retaining panel mapping."""
    api_key = os.getenv("GEMINI_API_KEY", "").strip()
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY is missing. Add it to your .env file.")
    client = genai.Client(api_key=api_key)
    model = os.getenv("GEMINI_STORY_MODEL", "gemini-2.5-flash")
    prompt = f"""
Write polished comic narration and dialogue for this five-panel story.
Character: {character_name}. Tone: {tone}.
Preserve the five-panel sequence. Do not invent extra panels. Keep each panel's title.
Return plain text with headings Panel 1 through Panel 5 and concise, vivid narration/dialogue.
Outline JSON:
{outline}
"""
    response = client.models.generate_content(model=model, contents=prompt)
    story = (response.text or "").strip()
    if not story:
        raise RuntimeError("Gemini returned an empty story. Please try again.")
    return story
