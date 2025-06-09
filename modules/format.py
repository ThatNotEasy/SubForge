import re
import os
from langdetect import detect

def detect_format(filename):
    """Detect subtitle format from file extension"""
    ext = os.path.splitext(filename)[1].lower()
    return ext if ext in {'.srt', '.vtt', '.ssa', '.ass', '.ttml', '.dfxp', '.xml', '.sbv', '.txt'} else '.txt'

def detect_language(content):
    """Detect language from text content"""
    try:
        sample = ' '.join(re.findall(r'[^\d\W_]+', content)[:50])
        return detect(sample)
    except:
        return 'en'