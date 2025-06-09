import re
from xml.sax.saxutils import escape
from bs4 import BeautifulSoup
from colorama import Fore
from modules.logging import log_info
import os

class SubtitleBlock:
    def __init__(self, index=None, start_time=None, end_time=None, text=None):
        self.index = index
        self.start_time = start_time
        self.end_time = end_time
        self.text = text

def parse_srt(content):
    """Parse SRT content into SubtitleBlock objects"""
    blocks = []
    for block in re.split(r'\n\s*\n', content.strip()):
        lines = [line.strip() for line in block.split('\n') if line.strip()]
        if len(lines) >= 3:
            try:
                block = SubtitleBlock(
                    index=lines[0],
                    start_time=lines[1].split('-->')[0].strip(),
                    end_time=lines[1].split('-->')[1].strip(),
                    text='\n'.join(lines[2:]))
                blocks.append(block)
            except Exception as e:
                log_info(f"Failed to parse SRT block: {e}", Fore.RED)
    return blocks

def parse_vtt(content):
    """Parse WebVTT content into SubtitleBlock objects"""
    blocks = []
    for block in content.strip().split('\n\n'):
        if '-->' in block:
            lines = block.split('\n')
            time_line = None
            text_lines = []
            
            for line in lines:
                if '-->' in line:
                    time_line = line
                else:
                    text_lines.append(line)
            
            if time_line:
                try:
                    start, end = time_line.split('-->')
                    blocks.append(SubtitleBlock(
                        start_time=start.strip(),
                        end_time=end.strip(),
                        text='\n'.join(text_lines)))
                except Exception as e:
                    log_info(f"Failed to parse VTT block: {e}", Fore.RED)
    return blocks

def parse_sbv(content):
    """Parse SBV content into SubtitleBlock objects"""
    blocks = []
    current_block = None
    
    for line in content.split('\n'):
        if '-->' in line:
            if current_block:
                blocks.append(current_block)
            try:
                start, end = line.split('-->')
                current_block = SubtitleBlock(
                    start_time=start.strip(),
                    end_time=end.strip())
            except:
                current_block = None
        elif current_block:
            if current_block.text:
                current_block.text += '\n' + line.strip()
            else:
                current_block.text = line.strip()
    
    if current_block:
        blocks.append(current_block)
    return blocks

def convert_to_ttml(blocks, source_lang, target_lang, translate_func, output_ext='.ttml'):
    """Convert subtitle blocks to TTML format"""
    ttml = [f'''<?xml version="1.0" encoding="UTF-8"?>
<tt xmlns="http://www.w3.org/ns/ttml" xml:lang="{target_lang}">
<head>
<styling>
<style xml:id="default" tts:color="white" tts:fontFamily="sansSerif" tts:fontSize="100%"/>
</styling>
</head>
<body>
<div>''']
    
    for block in blocks:
        try:
            translated = translate_func(block.text, source_lang, target_lang)
            # Ensure proper time format based on output extension
            start_time = format_time(block.start_time, output_ext)
            end_time = format_time(block.end_time, output_ext)
            ttml.append(f'<p begin="{start_time}" end="{end_time}">{escape(translated)}</p>')
        except Exception as e:
            log_info(f"TTML conversion error: {e}", Fore.RED)
    
    ttml.append('''</div>
</body>
</tt>''')
    return '\n'.join(ttml)

def convert_to_srt(blocks, source_lang, target_lang, translate_func, output_ext='.srt'):
    """Convert subtitle blocks to SRT format"""
    output = []
    for i, block in enumerate(blocks, 1):
        try:
            translated = translate_func(block.text, source_lang, target_lang)
            # Format time according to SRT standards
            start_time = format_time(block.start_time, output_ext)
            end_time = format_time(block.end_time, output_ext)
            output.append(f"{i}\n{start_time} --> {end_time}\n{translated}\n")
        except Exception as e:
            log_info(f"SRT conversion error: {e}", Fore.RED)
    return '\n'.join(output)

def convert_to_vtt(blocks, source_lang, target_lang, translate_func, output_ext='.vtt'):
    """Convert subtitle blocks to VTT format"""
    output = ["WEBVTT\n"]
    for block in blocks:
        try:
            translated = translate_func(block.text, source_lang, target_lang)
            # Format time according to VTT standards
            start_time = format_time(block.start_time, output_ext)
            end_time = format_time(block.end_time, output_ext)
            output.append(f"{start_time} --> {end_time}\n{translated}\n")
        except Exception as e:
            log_info(f"VTT conversion error: {e}", Fore.RED)
    return '\n'.join(output)

def convert_to_ssa(content, source_lang, target_lang, translate_func, output_ext='.ssa'):
    """Convert SSA/ASS content"""
    output = []
    for line in content.split('\n'):
        if line.startswith("Dialogue:"):
            parts = line.split(',', 9)
            if len(parts) == 10:
                parts[9] = translate_func(parts[9], source_lang, target_lang)
                line = ','.join(parts)
        output.append(line)
    return '\n'.join(output)

def convert_ttml(content, source_lang, target_lang, translate_func, output_ext='.ttml'):
    """Convert TTML content"""
    soup = BeautifulSoup(content, 'xml')
    for p in soup.find_all('p'):
        if p.string:
            p.string.replace_with(translate_func(p.string, source_lang, target_lang))
    return soup.prettify()

def convert_to_sbv(blocks, source_lang, target_lang, translate_func, output_ext='.sbv'):
    """Convert subtitle blocks to SBV format"""
    output = []
    for block in blocks:
        try:
            translated = translate_func(block.text, source_lang, target_lang)
            # Format time according to SBV standards
            start_time = format_time(block.start_time, output_ext)
            end_time = format_time(block.end_time, output_ext)
            output.append(f"{start_time} --> {end_time}\n{translated}\n")
        except Exception as e:
            log_info(f"SBV conversion error: {e}", Fore.RED)
    return '\n'.join(output)

def convert_txt(content, source_lang, target_lang, translate_func, output_ext='.txt'):
    """Convert plain text content"""
    return '\n'.join(translate_func(line, source_lang, target_lang) for line in content.split('\n'))

def format_time(time_str, output_ext):
    """Format time string according to the output extension's standards"""
    if not time_str:
        return time_str
    
    # Common time format conversions
    if output_ext.lower() in ['.srt']:
        return time_str.replace('.', ',')  # SRT uses commas for milliseconds
    elif output_ext.lower() in ['.vtt', '.ttml', '.sbv']:
        return time_str.replace(',', '.')  # Most others use periods
    elif output_ext.lower() in ['.ssa', '.ass']:
        # Convert to SSA time format (H:MM:SS.cc)
        parts = time_str.replace(',', '.').split(':')
        if len(parts) == 3:
            h, m, s = parts
            if '.' in s:
                s, ms = s.split('.')
                cs = f"{int(ms[:2]):02d}"  # Convert milliseconds to centiseconds
                return f"{int(h)}:{m}:{s}.{cs}"
        return time_str
    return time_str  # Default case