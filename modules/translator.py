from deep_translator import GoogleTranslator
from langdetect import detect

def translate_text(text, source_lang, target_lang):
    try:
        if not text.strip():
            return text
            
        if source_lang == 'auto':
            try:
                source_lang = detect(text)
            except:
                source_lang = 'en'
                
        if target_lang == "ms":  # Special case for Malay
            return GoogleTranslator(
                source=source_lang,
                target="ms",
                api_url="https://translate.googleapis.com"
            ).translate(text)
        return GoogleTranslator(source=source_lang, target=target_lang).translate(text)
    except Exception as e:
        print(f"Translation error: {e}")
        return text