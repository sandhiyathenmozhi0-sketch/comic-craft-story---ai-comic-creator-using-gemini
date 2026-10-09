from pathlib import Path
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.routes import router

BASE_DIR = Path(__file__).resolve().parent.parent
(BASE_DIR / "app" / "static" / "panels").mkdir(parents=True, exist_ok=True)
(BASE_DIR / "app" / "static" / "exports").mkdir(parents=True, exist_ok=True)

app = FastAPI(
    title="ComicCraft - AI Comic Story Creator",
    description="Generate five-panel comics with Gemini and Hugging Face image generation.",
    version="1.0.0",
)
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "app" / "static")), name="static")
app.include_router(router)
