# ComicCraft — AI Comic Story Creator

ComicCraft is a FastAPI web app based on the supplied project documentation. It collects a story prompt, character, setting, tone, and art style; asks Gemini to create a five-panel outline and narration; generates illustrations through the Hugging Face Inference API when configured; previews the comic; and exports a PDF.

## Requirements

- Python 3.11 or 3.12 recommended
- VS Code
- Gemini API key
- Optional Hugging Face access token for AI-generated images
- Internet connection for the AI APIs

> Provider model names and inference availability can change. The model names are configurable in `.env`. If Hugging Face image generation is not configured or unavailable, the app creates clearly labelled placeholder images so the rest of the workflow remains testable.

## 1. Open the project

Extract the ZIP, then open the `ComicCraft` folder in VS Code (`File → Open Folder`).

## 2. Create and activate a virtual environment (Windows PowerShell)

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

If PowerShell blocks activation, use Command Prompt instead:

```bat
py -3.12 -m venv .venv
.venv\Scripts\activate.bat
python -m pip install --upgrade pip
pip install -r requirements.txt
```

If `py -3.12` is not available, install Python 3.12 and enable “Add Python to PATH” during installation.

## 3. Configure API keys

1. Copy `.env.example` and rename the copy to `.env`.
2. Open `.env` and replace `GEMINI_API_KEY` with your Gemini API key.
3. Optionally set `HF_API_KEY` to a Hugging Face user access token to enable image generation.
4. Save the file. Never share or commit `.env`.

Gemini is required for story generation. Hugging Face image generation is optional; without it, the application uses labelled placeholder images.

## 4. Run the app

From the project root, with the virtual environment active:

```powershell
uvicorn app.main:app --reload
```

Open:
- Website: http://127.0.0.1:8000
- Interactive API docs: http://127.0.0.1:8000/docs

Stop the server with `Ctrl+C`.

## 5. Test the complete flow

1. Open the website.
2. Enter a story idea of at least five characters.
3. Choose the character name, setting, tone, and art style.
4. Click **Create my comic**. Wait while Gemini generates the five-panel story and images.
5. Review the comic preview.
6. Click **Download comic PDF** to save the PDF.
7. Test the JSON endpoint from `/docs` using `POST /generate-comic/json`, for example:

```json
{
  "story_prompt": "A brave fox finds a glowing door in an enchanted forest",
  "character_name": "Milo",
  "setting": "enchanted forest",
  "tone": "funny",
  "art_style": "comic book"
}
```

## API routes

| Method | Route | Purpose |
|---|---|---|
| GET | `/` | Home form |
| POST | `/generate` | Generate and preview comic from form input |
| POST | `/generate-comic/json` | Generate comic from JSON |
| POST | `/test-image` | Test illustration generation |
| GET | `/export-success` | Export confirmation page |
| GET | `/download/{filename}` | Securely download an exported PDF |

## Project structure

```text
ComicCraft/
├── app/
│   ├── main.py
│   ├── routes.py
│   ├── models.py
│   ├── services/
│   │   ├── gemini_flash.py
│   │   ├── gemini_pro.py
│   │   ├── image_generator.py
│   │   ├── layout_builder.py
│   │   └── exporters.py
│   ├── templates/
│   │   ├── index.html
│   │   ├── comic_preview.html
│   │   └── export_success.html
│   └── static/
│       ├── css/styles.css
│       ├── panels/
│       └── exports/
├── .env.example
├── requirements.txt
└── README.md
```

## Troubleshooting

- **`GEMINI_API_KEY is missing`**: ensure `.env` exists in the project root and contains the key.
- **Gemini model error**: check the key and access in Google AI Studio; if needed, change `GEMINI_OUTLINE_MODEL` and `GEMINI_STORY_MODEL` to models enabled for your account.
- **Images show placeholders**: add a valid Hugging Face token and verify that the selected model is available through the Inference API. Some models may be unavailable or require access approval.
- **Module not found**: activate `.venv` and run `pip install -r requirements.txt` from the project root.
- **PDF text accents/special symbols**: the PDF export uses FPDF's built-in Helvetica encoding and replaces unsupported characters; use plain ASCII if you need maximum compatibility.
- **Slow generation**: image generation is a remote request per panel and can take a few minutes.

## Security notes

Keep API keys private. Do not expose `.env`, do not commit secrets, and do not use debug mode on a public production server. This project is configured for local development, not hardened public deployment.
