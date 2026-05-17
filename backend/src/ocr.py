import os
from PIL import Image
import pytesseract
from .config import TESSERACT_CMD

# Configure Tesseract path if provided (Windows)
if TESSERACT_CMD and os.path.exists(TESSERACT_CMD):
    pytesseract.pytesseract.tesseract_cmd = TESSERACT_CMD

def extract_text(image_path: str, lang: str = "eng") -> str:
    """
    Extract text from an image using Tesseract OCR.
    :param image_path: Path to the input image.
    :param lang: Tesseract language(s), e.g., 'eng', 'tam', or 'eng+tam'.
    :return: The extracted text as a string.
    """
    try:
        img = Image.open(image_path)
        text = pytesseract.image_to_string(img, lang=lang)
        return text.strip()
    except pytesseract.TesseractNotFoundError as e:
        raise RuntimeError(
            "Tesseract not found. Please install Tesseract OCR and/or set TESSERACT_CMD in src/config.py"
        ) from e
