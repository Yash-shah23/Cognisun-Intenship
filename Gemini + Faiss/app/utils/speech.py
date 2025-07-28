import speech_recognition as sr

def speech_to_text(audio_file_path: str) -> str:
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_file_path) as source:
        audio_data = recognizer.record(source)
        return recognizer.recognize_google(audio_data)
