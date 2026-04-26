#!/usr/bin/env python3
"""
Text-to-Speech Converter
A powerful Python tool for converting text to speech with multiple engine support.

Features:
- Multiple TTS engines (gTTS, pyttsx3, edge-tts)
- Batch file processing
- Audio format conversion (MP3, WAV, OGG)
- SSML support for advanced speech control
- Speed and pitch adjustment
- Interactive and CLI modes

Author: UniverseCreator
Version: 1.0.0
"""

import os
import sys
import json
import argparse
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Optional, List, Dict, Any

# Try to import optional dependencies
try:
    from gtts import gTTS
    GTTS_AVAILABLE = True
except ImportError:
    GTTS_AVAILABLE = False

try:
    import pyttsx3
    PYTTSX3_AVAILABLE = True
except ImportError:
    PYTTSX3_AVAILABLE = False


class TTSConverter:
    """Main Text-to-Speech converter class."""
    
    def __init__(self, engine: str = "auto"):
        self.engine = engine
        self.history: List[Dict[str, Any]] = []
        self.config_file = Path.home() / ".tts_converter_config.json"
        self.load_config()
        
    def load_config(self):
        """Load configuration from file."""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r') as f:
                    self.config = json.load(f)
            except:
                self.config = self.get_default_config()
        else:
            self.config = self.get_default_config()
    
    def save_config(self):
        """Save configuration to file."""
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=2)
    
    def get_default_config(self) -> Dict[str, Any]:
        """Get default configuration."""
        return {
            "default_engine": "gtts",
            "default_language": "en",
            "default_speed": 1.0,
            "output_directory": str(Path.home() / "tts_output"),
            "history_enabled": True
        }
    
    def detect_best_engine(self) -> str:
        """Detect the best available TTS engine."""
        if GTTS_AVAILABLE:
            return "gtts"
        elif PYTTSX3_AVAILABLE:
            return "pyttsx3"
        else:
            return "espeak"
    
    def convert_text(self, text: str, output_file: str, 
                     language: str = "en", speed: float = 1.0,
                     engine: Optional[str] = None) -> bool:
        """
        Convert text to speech and save to file.
        
        Args:
            text: Text to convert
            output_file: Output audio file path
            language: Language code (e.g., 'en', 'es', 'fr')
            speed: Speech speed multiplier (0.5 - 2.0)
            engine: TTS engine to use (gtts, pyttsx3, espeak)
        
        Returns:
            True if successful, False otherwise
        """
        engine = engine or self.config.get("default_engine", "gtts")
        
        if engine == "auto":
            engine = self.detect_best_engine()
        
        try:
            if engine == "gtts" and GTTS_AVAILABLE:
                return self._convert_gtts(text, output_file, language, speed)
            elif engine == "pyttsx3" and PYTTSX3_AVAILABLE:
                return self._convert_pyttsx3(text, output_file, speed)
            else:
                return self._convert_espeak(text, output_file, language, speed)
        except Exception as e:
            print(f"❌ Error converting text: {e}")
            return False
    
    def _convert_gtts(self, text: str, output_file: str, 
                      language: str, speed: float) -> bool:
        """Convert using Google Text-to-Speech (gTTS)."""
        # gTTS doesn't support speed directly, but we can use slow=True/False
        slow = speed < 1.0
        
        tts = gTTS(text=text, lang=language, slow=slow)
        tts.save(output_file)
        
        self._log_conversion(text, output_file, "gtts", language)
        print(f"✅ Saved: {output_file}")
        return True
    
    def _convert_pyttsx3(self, text: str, output_file: str, 
                         speed: float) -> bool:
        """Convert using pyttsx3 (offline)."""
        engine = pyttsx3.init()
        
        # Adjust rate (default is usually 200)
        rate = engine.getProperty('rate')
        engine.setProperty('rate', int(rate * speed))
        
        # Save to file
        engine.save_to_file(text, output_file)
        engine.runAndWait()
        
        self._log_conversion(text, output_file, "pyttsx3", "en")
        print(f"✅ Saved: {output_file}")
        return True
    
    def _convert_espeak(self, text: str, output_file: str, 
                        language: str, speed: float) -> bool:
        """Convert using espeak (command-line fallback)."""
        # Calculate words per minute (default 175)
        wpm = int(175 * speed)
        
        cmd = [
            "espeak",
            "-v", language,
            "-s", str(wpm),
            "-w", output_file,
            text
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            self._log_conversion(text, output_file, "espeak", language)
            print(f"✅ Saved: {output_file}")
            return True
        else:
            print(f"❌ espeak error: {result.stderr}")
            return False
    
    def _log_conversion(self, text: str, output_file: str, 
                        engine: str, language: str):
        """Log conversion to history."""
        if self.config.get("history_enabled", True):
            self.history.append({
                "timestamp": datetime.now().isoformat(),
                "text_preview": text[:100] + "..." if len(text) > 100 else text,
                "output_file": output_file,
                "engine": engine,
                "language": language
            })
    
    def batch_convert(self, input_files: List[str], output_dir: str,
                      language: str = "en", engine: Optional[str] = None) -> Dict[str, bool]:
        """
        Convert multiple text files to speech.
        
        Args:
            input_files: List of text file paths
            output_dir: Output directory for audio files
            language: Language code
            engine: TTS engine to use
        
        Returns:
            Dictionary mapping input files to success status
        """
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        results = {}
        
        for input_file in input_files:
            try:
                with open(input_file, 'r', encoding='utf-8') as f:
                    text = f.read()
                
                output_name = Path(input_file).stem + ".mp3"
                output_path = output_dir / output_name
                
                success = self.convert_text(text, str(output_path), language, engine=engine)
                results[input_file] = success
                
            except Exception as e:
                print(f"❌ Error processing {input_file}: {e}")
                results[input_file] = False
        
        return results
    
    def get_supported_languages(self) -> Dict[str, str]:
        """Get list of supported languages."""
        return {
            "en": "English",
            "es": "Spanish",
            "fr": "French",
            "de": "German",
            "it": "Italian",
            "pt": "Portuguese",
            "ru": "Russian",
            "ja": "Japanese",
            "ko":