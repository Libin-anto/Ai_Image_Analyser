import argparse
import os
from src.ocr import extract_text
from src.detect import YoloDetector
from src.tts import speak

def build_summary(text: str, labels):
    text_part = text if text else "(no text detected)"
    labels_part = ", ".join(labels) if labels else "(no objects detected)"
    # Keep the summary short for TTS
    text_short = (text_part[:180] + "...") if len(text_part) > 180 else text_part
    summary = f"Text detected: {text_short}. Objects found: {labels_part}."
    return summary

def main():
    parser = argparse.ArgumentParser(description="AI Image Analyzer: OCR + YOLO + TTS")
    parser.add_argument("--image", required=True, help="Path to the input image (.jpg/.png)")
    parser.add_argument("--lang", default="en", choices=["en", "ta"], help="Voice language for summary (en or ta)")
    parser.add_argument("--ocr_lang", default="eng", help="Tesseract OCR language, e.g., 'eng', 'tam', or 'eng+tam'")
    parser.add_argument("--model", default="yolov8n.pt", help="YOLOv8 model to use (e.g., yolov8n.pt)")
    parser.add_argument("--no_speak", action="store_true", help="Disable voice and only print summary")
    args = parser.parse_args()

    if not os.path.exists(args.image):
        raise FileNotFoundError(f"Image not found: {args.image}")

    # OCR
    text = extract_text(args.image, lang=args.ocr_lang)

    # Detection
    detector = YoloDetector(model_name=args.model)
    labels, out_img = detector.detect(args.image, save_vis=True, out_path="outputs/detections.jpg")

    # Summary
    summary = build_summary(text, labels)

    print("="*60)
    print("AI Image Analyzer Result")
    print("="*60)
    print("OCR Text:")
    print(text if text else "(none)")
    print("-"*60)
    print(f"Objects: {', '.join(labels) if labels else '(none)'}")
    print("-"*60)
    print(f"Detection image saved to: {out_img}")
    print("-"*60)
    print("Summary:")
    print(summary)
    print("="*60)

    # TTS
    if not args.no_speak:
        speak(summary, lang=args.lang)

if __name__ == "__main__":
    main()
