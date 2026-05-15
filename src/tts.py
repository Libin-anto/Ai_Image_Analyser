import os
from gtts import gTTS

def speak(text: str, lang: str = "en") -> None:
    """
    Speak the given text. This generates a temp file and plays it locally.
    """
    try:
        tts = gTTS(text=text, lang=lang)
        temp_file = "temp_speech.mp3"
        tts.save(temp_file)
        
        if os.name == 'nt':
            # Windows play
            os.system(f"start {temp_file}")
        else:
            # Mac/Linux play
            os.system(f"afplay {temp_file} || mpg123 {temp_file}")
    except Exception as e:
        print(f"Speech error: {e}")

def save_audio(text: str, filepath: str, lang: str = "en") -> bool:
    """
    Save the given text to an audio file using gTTS.
    Returns True if successful, False otherwise.
    """
    try:
        tts = gTTS(text=text, lang=lang)
        tts.save(filepath)
        return True
    except Exception as e:
        print(f"Error saving audio with gTTS: {e}")
        return False
