import os
import uuid
# pyrefly: ignore [missing-import]
from flask import Flask, request, jsonify
from flask_cors import CORS
# pyrefly: ignore [missing-import]
from werkzeug.utils import secure_filename
from src.ocr import extract_text
from src.detect import YoloDetector
from src.tts import save_audio
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__, static_folder='outputs', static_url_path='/outputs')
CORS(app)

app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['OUTPUT_FOLDER'] = 'outputs'

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['OUTPUT_FOLDER'], exist_ok=True)

detector = YoloDetector(model_name="yolov8n.pt")

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


@app.route('/api/analyze', methods=['POST'])
def analyze():
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'}), 400
    
    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'No image selected'}), 400

    filename = secure_filename(file.filename)
    unique_id = str(uuid.uuid4())[:8]
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], f"{unique_id}_{filename}")
    file.save(filepath)

    try:
        # OCR
        text = extract_text(filepath, lang="eng")
        
        # Detection
        out_img_name = f"det_{unique_id}_{filename}"
        out_img_path = os.path.join(app.config['OUTPUT_FOLDER'], out_img_name)
        labels, _ = detector.detect(filepath, save_vis=True, out_path=out_img_path)

        # Summary
        summary = build_summary(text, labels)

        # Generate Audio
        audio_name = f"audio_{unique_id}.mp3"
        audio_path = os.path.join(app.config['OUTPUT_FOLDER'], audio_name)
        save_audio(summary, audio_path, lang="en")

        return jsonify({
            'text': text,
            'objects': labels,
            'summary': summary,
            'image_url': f"/outputs/{out_img_name}",
            'audio_url': f"/outputs/{audio_name}"
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/speak', methods=['POST'])
def speak_api():
    data = request.json
    text = data.get('text', '')
    if not text:
        return jsonify({'error': 'No text provided'}), 400

    unique_id = str(uuid.uuid4())[:8]
    audio_name = f"speak_{unique_id}.mp3"
    audio_path = os.path.join(app.config['OUTPUT_FOLDER'], audio_name)
    
    success = save_audio(text, audio_path, lang="en")
    if success:
        return jsonify({'audio_url': f"/outputs/{audio_name}"})
    else:
        return jsonify({'error': 'Failed to generate audio'}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
