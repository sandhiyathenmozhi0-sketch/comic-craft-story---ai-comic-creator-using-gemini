from pydantic import BaseModel, Field
from typing import Literal

class PromptRequest(BaseModel):
    story_prompt: str = Field(..., min_length=5, max_length=1200)
    character_name: str = Field(default="Alex", min_length=1, max_length=80)
    setting: str = Field(default="enchanted forest", max_length=120)
    tone: Literal["light-hearted", "dramatic", "poetic", "funny"] = "light-hearted"
    art_style: Literal["anime", "pixel art", "comic book", "realistic"] = "comic book"
