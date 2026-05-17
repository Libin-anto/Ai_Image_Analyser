import sys
import json
import os
import argparse
from src.ocr import extract_text
from src.detect import YoloDetector

def build_summary(text: str, labels: list) -> str:
    if not text and not labels:
        return "I could not detect any text or recognizable objects in the image."
    
    summary_parts = ["I have analyzed the image."]
    
    if labels:
        from collections import Counter
        label_counts = Counter(labels)
        objects_desc = []
        for label, count in label_counts.items():
            if count == 1:
                objects_desc.append(f"one {label}")
            else:
                objects_desc.append(f"{count} {label}s")
        
        if len(objects_desc) > 1:
            objects_str = ", ".join(objects_desc[:-1]) + f", and {objects_desc[-1]}"
        else:
            objects_str = objects_desc[0]
            
        summary_parts.append(f"I found {objects_str}.")
    else:
        summary_parts.append("I did not find any recognizable objects.")
        
    if text:
        clean_text = " ".join(text.split())
        text_short = (clean_text[:500] + "...") if len(clean_text) > 500 else clean_text
        summary_parts.append(f"Additionally, the text extracted from the image reads as follows: {text_short}")
        
    return " ".join(summary_parts)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--image", required=True)
    parser.add_argument("--out_img_path", required=True)
    args = parser.parse_args()

    try:
        if not os.path.exists(args.image):
            raise FileNotFoundError(f"Image not found: {args.image}")

        text = extract_text(args.image, lang="eng")
        
        detector = YoloDetector(model_name="yolov8n.pt")
        labels, _ = detector.detect(args.image, save_vis=True, out_path=args.out_img_path)

        summary = build_summary(text, labels)

        result = {
            "success": True,
            "text": text,
            "objects": labels,
            "summary": summary
        }
        print(json.dumps(result))
    except Exception as e:
        error_result = {
            "success": False,
            "error": str(e)
        }
        print(json.dumps(error_result))

if __name__ == "__main__":
    main()
