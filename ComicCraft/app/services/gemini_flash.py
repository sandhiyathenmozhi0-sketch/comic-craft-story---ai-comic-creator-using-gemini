import json
import os
import re
from typing import Any
from google import genai
from google.genai import types

def _extract_json(text: str) -> Any:
    text = text.strip()
    text = re.sub(r"^```(?:json)?\s*", "", text)
    text = re.sub(r"\s*```$", "", text)
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        match = re.search(r"\[[\s\S]*\]", text)
        if match:
            return json.loads(match.group(0))
        raise ValueError("The story model did not return valid JSON. Please try again.")

def generate_outline(story_prompt: str, character_name: str, setting: str, tone: str, art_style: str) -> list[dict]:
    api_key = os.getenv("GEMINI_API_KEY", "").strip()
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY is missing. Add it to your .env file.")
    client = genai.Client(api_key=api_key)
    model = os.getenv("GEMINI_OUTLINE_MODEL", "gemini-2.5-flash")
    instruction = f"""
Create exactly five sequential comic panels. Return ONLY a valid JSON array with five objects.
Each object must contain: panel_number (integer), title (string), scene_description (string),
image_prompt (string), caption (string), narration (string), dialogue (string).
Keep the same character appearance across all panels. Avoid text/lettering inside the generated image.
Story idea: {story_prompt}
Main character: {character_name}
Setting: {setting}
Tone: {tone}
Art style: {art_style}
Make the story coherent, safe, and suitable for a general audience.
"""
    response = client.models.generate_content(
        model=model,
        contents=instruction,
        config=types.GenerateContentConfig(temperature=0.8, response_mime_type="application/json"),
    )
    data = _extract_json(response.text or "")
    if not isinstance(data, list) or len(data) != 5:
        raise ValueError("The model did not return exactly five panels. Please submit again.")
    cleaned = []
    required = ("title", "scene_description", "image_prompt", "caption", "narration", "dialogue")
    for i, panel in enumerate(data, start=1):
        if not isinstance(panel, dict):
            raise ValueError("Invalid panel data returned by the model.")
        item = {"panel_number": i}
        for key in required:
            item[key] = str(panel.get(key, "")).strip() or ("A new scene unfolds." if key != "title" else f"Panel {i}")
        item["image_prompt"] = (
            f"{item['image_prompt']}. {art_style} comic illustration, {setting}, "
            "consistent character design, cinematic composition, no words, no text, no watermark"
        )
        cleaned.append(item)
    return cleaned
