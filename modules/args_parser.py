import argparse
import os
from modules.format import detect_format
from modules.logging import log_error, log_info
from colorama import Fore

def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Subtitle Translator & Converter",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    
    # Required arguments
    parser.add_argument(
        "-i", "--input",
        required=True,
        help="Input subtitle file path (required)",
        metavar="FILE"
    )
    
    parser.add_argument(
        "-o", "--output",
        required=True,
        help="Output file name (without extension) (required)",
        metavar="NAME"
    )
    
    parser.add_argument(
        "-e", "--extension",
        required=True,
        help=(
            "Output format extension (required) "
            "(srt, vtt, ttml, dfxp, xml, ssa, ass, sbv, txt)"
        ),
        choices=['srt', 'vtt', 'ttml', 'dfxp', 'xml', 'ssa', 'ass', 'sbv', 'txt'],
        metavar="EXT"
    )
    
    parser.add_argument(
        "-t", "--target",
        required=True,
        help="Target language code (required) (e.g., en, ms, ru)",
        metavar="LANG"
    )
    
    # Optional arguments
    parser.add_argument(
        "-s", "--source",
        default="auto",
        help="Source language code (auto-detection if not specified)",
        metavar="LANG"
    )
    
    args = parser.parse_args()
    
    # Validate input file
    if not os.path.exists(args.input):
        log_error(f"Input file not found: {args.input}")
        exit(1)
    
    # Process extension
    if not args.extension.startswith('.'):
        args.extension = f".{args.extension}"
    
    # Construct output path
    args.output_path = f"{args.output}_{args.target}{args.extension}"
    log_info(f"Output will be saved to: {args.output_path}", Fore.CYAN)
    
    return args

def get_arguments():
    try:
        return parse_arguments()
    except Exception as e:
        log_error(f"Argument parsing failed: {e}")
        exit(1)