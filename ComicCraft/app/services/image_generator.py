import os
import re
import uuid
from pathlib import Path
import requests
from PIL import Image, ImageDraw

BASE_DIR = Path(__file__).resolve().parents[1]
PANELS_DIR = BASE_DIR / "static" / "panels"
PANELS_DIR.mkdir(parents=True, exist_ok=True)

def _placeholder(path: Path, prompt: str, style: str) -> None:
    """Create a labelled visual placeholder if no image provider is configured."""
    image = Image.new("RGB", (768, 512), "#f3e8ff")
    draw = ImageDraw.Draw(image)
    draw.rounded_rectangle((22, 22, 746, 490), radius=24, outline="#6d28d9", width=5)
    draw.text((48, 55), "ComicCraft • Image preview", fill="#4c1d95")
    words = (prompt[:150] + "...") if len(prompt) > 150 else prompt
    lines, line = [], ""
    for word in words.split():
        if len(line) + len(word) > 46:
            lines.append(line); line = word
        else:
            line = (line + " " + word).strip()
    if line: lines.append(line)
    for idx, item in enumerate(lines[:6]):
        draw.text((48, 120 + idx * 34), item, fill="#312e81")
    draw.text((48, 430), f"Style: {style} | Configure HF_API_KEY for AI images", fill="#6d28d9")
    image.save(path, format="PNG")

def generate_image(image_prompt: str, art_style: str = "comic book") -> str:
    """Generate an image through Hugging Face Inference API, or a clearly labelled placeholder."""
    filename = f"panel_{uuid.uuid4().hex[:12]}.png"
    output_path = PANELS_DIR / filename
    token = os.getenv("HF_API_KEY", "").strip()
    model = os.getenv("HF_IMAGE_MODEL", "stabilityai/stable-diffusion-xl-base-1.0")
    if token:
        try:
            url = f"https://router.huggingface.co/hf-inference/models/{model}"
            response = requests.post(
                url,
                headers={"Authorization": f"Bearer {token}", "Accept": "image/png"},
                json={"inputs": f"{image_prompt}, {art_style} illustration"},
                timeout=180,
            )
            response.raise_for_status()
            content_type = response.headers.get("content-type", "")
            if "image" not in content_type:
                raise RuntimeError("Image service returned a non-image response.")
            output_path.write_bytes(response.content)
            # Verify bytes are a valid image before serving/exporting.
            with Image.open(output_path) as im:
                im.verify()
            return f"/static/panels/{filename}"
        except Exception:
            # Keep the full web app usable and provide an explicit placeholder.
            if output_path.exists():
                output_path.unlink()
    _placeholder(output_path, image_prompt, art_style)
    return f"/static/panels/{filename}"
