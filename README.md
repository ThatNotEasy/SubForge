# SubForge 📜🌐

This Python tool allows you to translate subtitle files between various formats and languages. It supports a wide range of subtitle file formats, including `.srt`, `.vtt`, `.sbv`, `.ssa`, `.ttml`, and `.txt`. You can easily convert subtitles from one language to another, while preserving timestamps and formatting.

It uses **Google Translate** via the `deep_translator` library to perform translations and `langdetect` to auto-detect the source language. The translated subtitles can be saved in multiple formats, including `SRT`, `VTT`, and `TTML` (XML).

## Features 🚀

- **Supports multiple subtitle formats**: `.srt`, `.vtt`, `.sbv`, `.ssa`, `.ttml`, `.txt`
- **Auto-language detection**: Detects the source language automatically if not specified.
- **Google Translate integration**: Translates subtitles using Google Translate API.
- **Output options**: Convert subtitles into different formats (`.ttml`, `.dfxp`, `.xml`, etc.)
- **Preserves timestamps**: Ensures that the timing of each subtitle is kept intact during translation.
- **Handles special characters**: Escapes and processes special characters in the subtitle content to avoid errors.

## Installation 🛠️

To use this tool, you need to have Python installed. Then, you can install the required dependencies using `pip`:

```bash
pip install -r requirements.txt
```

## Usage 📄

To run the tool, simply execute the script, provide the input subtitle file path, and specify the target language and output format. Here's how you can use it:

1. **Provide the input subtitle file** (e.g., `.srt`, `.vtt`, `.sbv`, `.txt`).
2. **Choose the target language** (e.g., `en` for English, `ms` for Malay, `ru` for Russian).
3. **Select the output format** (e.g., `.srt`, `.vtt`, `.ttml`).

### Example

Run the Python script and follow the prompts:

```bash
python main.py
```

Enter the input file path:

```
Enter subtitle file path: movie.srt
```

Enter the target language:

```
Enter target language (e.g., en, ms, ru): en
```

Enter the output format:

```
Output format (e.g., .srt, .vtt, .ttml): .ttml
```

The tool will translate the subtitles and save the translated file as `movie_translated_en.ttml`.

## Supported Subtitle Formats 📁

- **.srt**: SubRip Subtitle file format.
- **.vtt**: WebVTT (Web Video Text Tracks).
- **.sbv**: SubRip Subtitle format used for YouTube captions.
- **.ssa** / **.ass**: Advanced SubStation Alpha subtitle format.
- **.ttml** / **.dfxp** / **.xml**: Timed Text Markup Language (TTML), used for various subtitle and captioning purposes.
- **.txt**: Plain text subtitles (one line per subtitle).

## Contributing 🤝

Contributions are welcome! If you have any bug fixes, enhancements, or suggestions, feel free to fork the repository and create a pull request. Make sure to update tests as appropriate.