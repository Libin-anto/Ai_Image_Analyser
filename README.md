# AI Image Analyzer & Synthesizer

A full-stack web and CLI application that extracts text (OCR) and detects objects from images, then synthesizes a natural language audio summary using Google Text-to-Speech (gTTS). 

## Features
- **Object Detection**: Uses YOLOv8 to locate and identify objects within an image.
- **Optical Character Recognition (OCR)**: Uses Tesseract to extract readable text from images.
- **Natural Language Summarization**: Dynamically constructs human-like sentences detailing the findings.
- **Text-to-Speech (TTS)**: Converts the natural language summary into high-quality audio using `gTTS`.
- **Premium Web UI**: A beautiful, dark-themed, glassmorphism UI built with Flask, HTML, CSS, and JS.
- **CLI Mode**: A fast, terminal-based way to analyze images without starting the web server.

## Prerequisites
- **Python**: Version 3.8 or higher.
- **Tesseract OCR**: Must be installed on your system.
  - *Windows*: Download from [UB-Mannheim/tesseract](https://github.com/UB-Mannheim/tesseract/wiki).
  - *Mac*: `brew install tesseract`
  - *Linux*: `sudo apt-get install tesseract-ocr`

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/ai-image-analyzer.git
   cd ai-image-analyzer
   ```

2. Create a virtual environment and install the dependencies:
   ```bash
   python -m venv venv
   # On Windows use:
   # venv\Scripts\activate
   # On Mac/Linux use:
   # source venv/bin/activate
   pip install -r requirements.txt
   ```

3. Configure Tesseract (Windows Users):
   If you installed Tesseract in a non-standard directory, open `src/config.py` and update the path. For example:
   ```python
   TESSERACT_CMD = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
   ```

## Usage

### 1. Web Application (Recommended)
To run the web interface, execute the Flask server:
```bash
python app.py
```
Then, open your web browser and navigate to `http://127.0.0.1:5000`. You can drag-and-drop images for analysis or use the standalone Text-to-Speech tab.

### 2. Command Line Interface (CLI)
To run the analyzer from the terminal without the web UI:
```bash
python main.py --image sample_images/hello_en.png
```

**Available CLI Flags:**
- `--image <path>`: Path to the image file (Required).
- `--no_speak`: Disables audio playback and only prints the summary.
- `--lang <code/en/ta>`: Language for the voice (default: `en`).
- `--ocr_lang <code>`: Tesseract OCR language (default: `eng`).
- `--model <name>`: YOLOv8 model to use (default: `yolov8n.pt`).

## Project Structure
- `app.py` - Flask web server and API endpoints.
- `main.py` - Command-line interface entry point.
- `src/` - Core logic for OCR, Object Detection, and TTS.
- `static/` - Web frontend assets (HTML, CSS, JS) and dynamically uploaded/generated files.
- `requirements.txt` - Python package dependencies.
