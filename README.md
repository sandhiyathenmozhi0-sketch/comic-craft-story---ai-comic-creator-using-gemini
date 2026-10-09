# 🎨 ComicCraft — AI Comic Story Creator

ComicCraft is an AI-powered web application that transforms a user's imagination into a five-panel comic story. Users can provide a story idea, choose a character name, select a setting, tone, and art style, and generate a comic with AI-written storylines and narration.

The application uses **Google Gemini** for story outline generation and narration, and the **Hugging Face Inference API** for AI-generated illustrations. Users can preview their generated comics and export them as downloadable PDF files.

## ✨ Features

* 📝 AI-powered story generation using Google Gemini
* 🎭 Custom character names and story settings
* 🎨 Selectable comic art styles and story tones
* 💬 AI-generated dialogue and narration
* 🖼️ AI-generated comic illustrations through Hugging Face
* 📖 Five-panel comic preview
* 📄 Downloadable PDF comic export
* ⚡ FastAPI backend and web-based interface
* 🔌 JSON API endpoint for programmatic comic generation
* 🔐 Environment-variable configuration for API credentials
* 🧪 Placeholder illustrations when image generation is unavailable

## 🛠️ Technology Stack

* **Backend:** Python, FastAPI
* **AI story generation:** Google Gemini API
* **AI image generation:** Hugging Face Inference API
* **Frontend:** HTML, CSS, Jinja2 templates
* **PDF generation:** FPDF2
* **Validation:** Pydantic
* **Configuration:** python-dotenv

## 🚀 Getting Started

1. Clone this repository.
2. Create and activate a Python virtual environment.
3. Install dependencies using `pip install -r requirements.txt`.
4. Copy `.env.example` to `.env`.
5. Add your Google Gemini API key to `.env`.
6. Optionally add a Hugging Face access token for AI illustrations.
7. Run the application using `uvicorn app.main:app --reload`.
8. Open `http://127.0.0.1:8000` in your browser.

See the README setup instructions for the full installation and deployment guide.

## 🔑 API Configuration

The application requires a Google Gemini API key for story generation. A Hugging Face token is optional and enables the configured image-generation service.

Keep API keys private. Never commit your `.env` file or publish API credentials in source code.

## 📌 Project Goal

The goal of ComicCraft is to make comic creation easier and more accessible by combining generative AI, creative storytelling, illustration generation, and PDF export in a single web application.

## 📜 License

Choose and add an appropriate open-source license before distributing the project. If no license is included, all rights remain with the copyright holder by default.
