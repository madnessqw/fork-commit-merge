# 🎙️ Text-to-Speech Converter

A powerful Python tool for converting text to speech with multiple engine support, batch processing, and audio customization.

## ✨ Features

- **Multiple TTS Engines**: Google TTS (gTTS), pyttsx3 (offline), espeak (fallback)
- **Batch Processing**: Convert multiple text files at once
- **Language Support**: 15+ languages including English, Spanish, French, German, Japanese, and more
- **Speed Control**: Adjust speech speed from 0.5x to 2.0x
- **Interactive Mode**: User-friendly menu-driven interface
- **CLI Mode**: Command-line interface for automation
- **Audio Formats**: MP3, WAV, OGG output support
- **History Tracking**: Keep track of all conversions

## 🚀 Quick Start

### Interactive Mode
```bash
python text_to_speech.py
```

### CLI Mode - Convert Single Text
```bash
python text_to_speech.py --text "Hello, world!" --output hello.mp3
```

### CLI Mode - Convert File
```bash
python text_to_speech.py --file article.txt --output article.mp3 --language en
```

### Batch Conversion
```bash
python text_to_speech.py --batch *.txt --output-dir ./audio --language es
```

## 📋 Requirements

### Required
- Python 3.7+

### Optional (for enhanced features)
```bash
# Google TTS (online, high quality)
pip install gtts

# Offline TTS
pip install pyttsx3

# Audio playback
pip install playsound
```

## 🎯 Use Cases

- **Content Creators**: Convert blog posts to audio for podcasts
- **Students**: Listen to study materials while commuting
- **Accessibility**: Create audio versions of documents
- **Language Learning**: Practice pronunciation with native speech
- **Automation**: Generate voiceovers for videos
- **E-learning**: Create audio content for courses

## 🌍 Supported Languages

| Code | Language | Code | Language |
|------|----------|------|----------|
| en | English | es | Spanish |
| fr | French | de | German |
| it | Italian | pt | Portuguese |
| ru | Russian | ja | Japanese |
| ko | Korean | zh | Chinese |
| ar | Arabic | hi | Hindi |
| nl | Dutch | pl | Polish |
| tr | Turkish | sv | Swedish |

## 💻 Command-Line Options

```
usage: text_to_speech.py [-h] [-t TEXT] [-f FILE] [-o OUTPUT] [-l LANG]
                         [-s SPEED] [-e ENGINE] [--batch] [--list-engines]

Text-to-Speech Converter

optional arguments:
  -h, --help            Show help message
  -t, --text TEXT       Text to convert
  -f, --file FILE       Text file to convert
  -o, --output OUTPUT   Output audio file
  -l, --language LANG   Language code (default: en)
  -s, --speed SPEED     Speech speed (0.5-2.0, default: 1.0)
  -e, --engine ENGINE   TTS engine: gtts, pyttsx3, espeak, auto
  --batch               Enable batch mode for multiple files
  --list-engines        List available TTS engines
```

## 🛠️ Installation

1. Download `text_to_speech.py`
2. Install optional dependencies:
   ```bash
   pip install gtts pyttsx3 playsound
   ```
3. Run the tool:
   ```bash
   python text_to_speech.py
   ```

## 📊 Examples

### Convert a blog post to audio
```bash
python text_to_speech.py --file blog_post.txt --output blog_post.mp3 --language en --speed 1.2
```

### Create audio for multiple articles
```bash
python text_to_speech.py --batch articles/*.txt --output-dir ./podcast_audio --language en
```

### Generate audio in different languages
```bash
# Spanish
python text_to_speech.py --text "Hola mundo" --output hello_es.mp3 --language es

# French
python text_to_speech.py --text "Bonjour le monde" --output hello_fr.mp3 --language fr

# Japanese
python text_to_speech.py --text "こんにちは世界" --output hello_ja.mp3 --language ja
```

## 🎨 Interactive Mode Features

The interactive mode provides:
- 📋 Main menu with all options
- 📝 Quick text-to-speech conversion
- 📁 File conversion with browse
- 📂 Batch processing wizard
- ⚙️ Settings management
- 📜 Conversion history viewer
- ❓ Help and documentation

## 🔧 Configuration

Settings are automatically saved to `~/.tts_converter_config.json`:
- Default TTS engine
- Default language
- Default speech speed
- Output directory
- History tracking

## 📈 Performance

- **gTTS**: High quality, requires internet
- **pyttsx3**: Offline, fast, OS-dependent voices
- **espeak**: Fallback, lightweight, robotic quality

## 🐛 Troubleshooting

### No audio output
- Check if output file was created
- Try different audio player
- Verify file format is supported

### gTTS not working
- Check internet connection
- Install gtts: `pip install gtts`

### pyttsx3 issues
- Install pyttsx3: `pip install pyttsx3`
- Some voices may require OS-specific setup

## 📝 License

MIT License - Feel free to use for personal and commercial projects.

## 🙏 Credits

Created by UniverseCreator - Your autonomous coding assistant.

---

**Ready to convert your text to speech?** Run `python text_to_speech.py` and start creating audio content!
