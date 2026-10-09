from pathlib import Path
from datetime import datetime
from io import BytesIO
import requests
from fpdf import FPDF
from PIL import Image

BASE_DIR = Path(__file__).resolve().parents[1]
EXPORTS_DIR = BASE_DIR / "static" / "exports"
EXPORTS_DIR.mkdir(parents=True, exist_ok=True)

def _image_to_jpeg(image_path: Path) -> str:
    with Image.open(image_path) as img:
        rgb = img.convert("RGB")
        temp_path = image_path.with_suffix(".export.jpg")
        rgb.save(temp_path, "JPEG", quality=90)
    return str(temp_path)

def save_pdf(layout: list[dict], title: str = "ComicCraft Comic") -> str:
    pdf = FPDF(unit="mm", format="A4")
    pdf.set_auto_page_break(auto=True, margin=14)
    temporary_images = []
    try:
        for panel in layout:
            pdf.add_page()
            pdf.set_font("Helvetica", "B", 18)
            safe_title = str(panel.get("title", "Comic panel")).encode("latin-1", "replace").decode("latin-1")
            pdf.multi_cell(0, 10, f"Panel {panel.get('panel_number', '')}: {safe_title}")
            image_path = str(panel.get("image_path", ""))
            local_image = None
            if image_path.startswith("/static/"):
                local_image = BASE_DIR / image_path.lstrip("/")
            elif image_path.startswith("http://") or image_path.startswith("https://"):
                try:
                    r = requests.get(image_path, timeout=20); r.raise_for_status()
                    tmp = EXPORTS_DIR / f"remote_{datetime.now().timestamp()}.png"
                    tmp.write_bytes(r.content); local_image = tmp; temporary_images.append(tmp)
                except Exception:
                    local_image = None
            if local_image and local_image.exists():
                try:
                    jpeg = _image_to_jpeg(local_image); temporary_images.append(Path(jpeg))
                    pdf.image(jpeg, x=15, y=pdf.get_y() + 2, w=180, h=100, keep_aspect_ratio=True)
                    pdf.ln(105)
                except Exception:
                    pdf.ln(4)
            for label, value in [
                ("Scene", panel.get("scene_description", "")),
                ("Caption", panel.get("caption", "")),
                ("Narration", panel.get("narration", "")),
                ("Dialogue", panel.get("dialogue", "")),
            ]:
                if value:
                    pdf.set_font("Helvetica", "B", 11)
                    pdf.cell(0, 7, label, new_x="LMARGIN", new_y="NEXT")
                    pdf.set_font("Helvetica", "", 10)
                    safe = str(value).encode("latin-1", "replace").decode("latin-1")
                    pdf.multi_cell(0, 5, safe)
                    pdf.ln(1)
        filename = f"comiccraft_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        output = EXPORTS_DIR / filename
        pdf.output(str(output))
        return f"/static/exports/{filename}"
    finally:
        for path in temporary_images:
            try: path.unlink(missing_ok=True)
            except OSError: pass
