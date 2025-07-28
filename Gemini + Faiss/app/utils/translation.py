from deep_translator import GoogleTranslator
from langdetect import detect

def translate(text: str, target_lang: str = "en") -> str:
    return GoogleTranslator(target=target_lang).translate(text)

def detect_language(text: str) -> str:
    return detect(text)
