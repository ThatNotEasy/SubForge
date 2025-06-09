import os
from modules import (
    translator,
    format,
    converter,
    banners,
    args_parser,
    logging
)
from colorama import Fore, init

def translate_subtitle_file(input_path, output_path, source_lang='auto', target_lang='en', output_ext=None):
    try:
        logging.log_info(f"Reading input file: {input_path}", Fore.CYAN)
        with open(input_path, 'r', encoding='utf-8', errors='replace') as f:
            content = f.read()

        if source_lang == 'auto':
            logging.log_info("Detecting source language...", Fore.YELLOW)
            source_lang = format.detect_language(content)
            logging.log_info(f"Detected source language: {source_lang}", Fore.GREEN)

        input_ext = format.detect_format(input_path)
        output_ext = output_ext or input_ext
        logging.log_info(f"Converting from {input_ext} to {output_ext}", Fore.CYAN)

        translated = process_content(content, input_ext, output_ext, source_lang, target_lang)

        os.makedirs(os.path.dirname(output_path) or '.', exist_ok=True)
        logging.log_info(f"Saving output to: {output_path}", Fore.CYAN)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(translated)

        logging.log_info("Conversion completed successfully!", Fore.GREEN)
        
    except Exception as e:
        logging.log_error(f"Conversion failed: {str(e)}")
        raise

def process_content(content, input_ext, output_ext, source_lang, target_lang):
    """Route processing to appropriate converter based on formats"""
    format_handlers = {
        '.srt': handle_srt,
        '.vtt': handle_vtt,
        '.ssa': handle_ssa,
        '.ass': handle_ssa,
        '.ttml': handle_ttml,
        '.dfxp': handle_ttml,
        '.xml': handle_ttml,
        '.sbv': handle_sbv,
        '.txt': handle_txt
    }
    
    handler = format_handlers.get(input_ext.lower())
    if not handler:
        raise ValueError(f"Unsupported input format: {input_ext}")
    
    return handler(content, source_lang, target_lang, output_ext)

def handle_srt(content, source_lang, target_lang, output_ext):
    blocks = converter.parse_srt(content)
    
    if output_ext.lower() in ['.ttml', '.dfxp', '.xml']:
        logging.log_info("Converting SRT to TTML format", Fore.CYAN)
        return converter.convert_to_ttml(blocks, source_lang, target_lang, translator.translate_text)
    
    elif output_ext.lower() in ['.ssa', '.ass']:
        logging.log_info("Converting SRT to SSA/ASS format", Fore.CYAN)
        return converter.convert_to_ssa(blocks, source_lang, target_lang, translator.translate_text)
    
    elif output_ext.lower() == '.vtt':
        logging.log_info("Converting SRT to VTT format", Fore.CYAN)
        return converter.convert_to_vtt(blocks, source_lang, target_lang, translator.translate_text)

    elif output_ext.lower() == '.sbv':
        logging.log_info("Converting SRT to SBV format", Fore.CYAN)
        return converter.convert_to_sbv(blocks, source_lang, target_lang, translator.translate_text)
    
    logging.log_info("Retaining SRT format", Fore.CYAN)
    return converter.convert_to_srt(blocks, source_lang, target_lang, translator.translate_text)

def handle_vtt(content, source_lang, target_lang, output_ext):
    blocks = converter.parse_vtt(content)
    if output_ext.lower() in ['.ttml', '.dfxp', '.xml']:
        logging.log_info("Converting VTT to TTML format", Fore.CYAN)
        return converter.convert_to_ttml(blocks, source_lang, target_lang, translator.translate_text)
    elif output_ext.lower() in ['.ssa', '.ass']:
        logging.log_info("Converting VTT to SSA/ASS format", Fore.CYAN)
        return converter.convert_to_ssa(blocks, source_lang, target_lang, translator.translate_text)
    logging.log_info("Retaining VTT format", Fore.CYAN)
    return converter.convert_to_vtt(blocks, source_lang, target_lang, translator.translate_text)

def handle_ssa(content, source_lang, target_lang, output_ext):
    return converter.convert_ssa(content, source_lang, target_lang, translator.translate_text)

def handle_ttml(content, source_lang, target_lang, output_ext):
    return converter.convert_ttml(content, source_lang, target_lang, translator.translate_text)

def handle_sbv(content, source_lang, target_lang, output_ext):
    blocks = converter.parse_sbv(content)
    
    if output_ext.lower() in ['.ttml', '.dfxp', '.xml']:
        logging.log_info("Converting SBV to TTML format", Fore.CYAN)
        return converter.convert_to_ttml(blocks, source_lang, target_lang, translator.translate_text)
    
    elif output_ext.lower() in ['.ssa', '.ass']:
        logging.log_info("Converting SBV to SSA/ASS format", Fore.CYAN)
        return converter.convert_to_ssa(blocks, source_lang, target_lang, translator.translate_text)
    
    elif output_ext.lower() == '.vtt':
        logging.log_info("Converting SBV to VTT format", Fore.CYAN)
        return converter.convert_to_vtt(blocks, source_lang, target_lang, translator.translate_text)
    
    elif output_ext.lower() == '.srt':
        logging.log_info("Converting SBV to SRT format", Fore.CYAN)
        return converter.convert_to_srt(blocks, source_lang, target_lang, translator.translate_text)

    logging.log_error("Unsupported SBV output format")
    raise ValueError("Failed to generate valid SBV output")

def handle_txt(content, source_lang, target_lang, output_ext):
    return converter.convert_txt(content, source_lang, target_lang, translator.translate_text)

if __name__ == "__main__":
    init()  # Initialize colorama
    banners.banners()
    args = args_parser.parse_arguments()
    translate_subtitle_file(
        input_path=args.input,
        output_path=args.output,
        source_lang=args.source,
        target_lang=args.target,
        output_ext=args.extension
    )