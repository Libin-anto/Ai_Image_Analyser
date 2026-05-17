import sys
import json
import argparse
from src.tts import save_audio

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--text", required=True)
    parser.add_argument("--out_audio_path", required=True)
    args = parser.parse_args()

    try:
        success = save_audio(args.text, args.out_audio_path, lang="en")
        if success:
            result = {"success": True}
        else:
            result = {"success": False, "error": "Failed to generate audio"}
        print(json.dumps(result))
    except Exception as e:
        error_result = {
            "success": False,
            "error": str(e)
        }
        print(json.dumps(error_result))

if __name__ == "__main__":
    main()
