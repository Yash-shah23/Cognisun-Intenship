# app/tts.py

from gtts import gTTS
import uuid
import os

def text_to_speech(text: str) -> str:
    # Create output folder if it doesn't exist
    output_folder = "app/audio"
    os.makedirs(output_folder, exist_ok=True)

    filename = f"{uuid.uuid4()}.mp3"
    file_path = os.path.join(output_folder, filename)

    tts = gTTS(text=text, lang='en')
    tts.save(file_path)

    return f"/audio/{filename}"
