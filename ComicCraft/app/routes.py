from pathlib import Path
import os
import traceback
from fastapi import APIRouter, Form, Request, HTTPException
from fastapi.responses import HTMLResponse, FileResponse, JSONResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv
from app.models import PromptRequest
from app.services.gemini_flash import generate_outline
from app.services.gemini_pro import generate_story
from app.services.image_generator import generate_image
from app.services.layout_builder import build_comic_layout
from app.services.exporters import save_pdf

load_dotenv()
router = APIRouter()
BASE_DIR = Path(__file__).resolve().parent.parent
templates = Jinja2Templates(directory=str(BASE_DIR / "app" / "templates"))

def _create_comic(data: PromptRequest) -> dict:
    outline = generate_outline(data.story_prompt, data.character_name, data.setting, data.tone, data.art_style)
    story = generate_story(outline, data.character_name, data.tone)
    image_paths = [generate_image(panel["image_prompt"], data.art_style) for panel in outline]
    layout = build_comic_layout(outline, image_paths)
    pdf_path = save_pdf(layout, title=f"{data.character_name}'s Comic")
    return {"layout": layout, "story": story, "pdf_path": pdf_path, "inputs": data.model_dump()}

@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(request=request, name="index.html", context={"error": None})

@router.post("/generate", response_class=HTMLResponse)
async def generate_form(
    request: Request,
    story_prompt: str = Form(...),
    character_name: str = Form("Alex"),
    setting: str = Form("enchanted forest"),
    tone: str = Form("light-hearted"),
    art_style: str = Form("comic book"),
):
    try:
        data = PromptRequest(story_prompt=story_prompt, character_name=character_name,
                             setting=setting, tone=tone, art_style=art_style)
        result = _create_comic(data)
        return templates.TemplateResponse(request=request, name="comic_preview.html",
                                          context={**result, "error": None})
    except Exception as exc:
        message = str(exc) if isinstance(exc, (ValueError, RuntimeError)) else "Comic generation failed. Check your API keys and terminal logs."
        return templates.TemplateResponse(request=request, name="index.html",
                                          context={"error": message}, status_code=500)

@router.post("/generate-comic/json")
async def generate_json(data: PromptRequest):
    try:
        result = _create_comic(data)
        return JSONResponse(content=result)
    except Exception as exc:
        raise HTTPException(status_code=502, detail=str(exc))

@router.post("/test-image")
async def test_image(prompt: str = Form(...), art_style: str = Form("comic book")):
    try:
        image_path = generate_image(prompt, art_style)
        return {"image_path": image_path}
    except Exception as exc:
        raise HTTPException(status_code=502, detail=str(exc))

@router.get("/export-success", response_class=HTMLResponse)
async def export_success(request: Request, pdf: str = ""):
    return templates.TemplateResponse(request=request, name="export_success.html",
                                      context={"pdf_path": pdf})

@router.get("/download/{filename}")
async def download_pdf(filename: str):
    # Only serve files in the export directory; prevent path traversal.
    export_dir = (BASE_DIR / "app" / "static" / "exports").resolve()
    candidate = (export_dir / filename).resolve()
    if candidate.parent != export_dir or not candidate.is_file() or not candidate.name.endswith(".pdf"):
        raise HTTPException(status_code=404, detail="PDF not found.")
    return FileResponse(candidate, media_type="application/pdf", filename=candidate.name)
