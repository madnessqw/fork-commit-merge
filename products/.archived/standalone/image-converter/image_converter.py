#!/usr/bin/env python3
"""
Universal Image Converter - Product #30
Batch convert, resize, and optimize images
Supports: JPG, PNG, WEBP, GIF, BMP, TIFF
Features: Batch processing, resize presets, quality control, format conversion
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime
from typing import List, Tuple, Optional

# Optional dependencies with fallbacks
try:
    from PIL import Image, ImageOps
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False
    print("Warning: Pillow not installed. Install with: pip install Pillow")


class ImageConverter:
    """Universal image conversion and optimization tool."""

    # Format mappings
    FORMAT_MAP = {
        '.jpg': 'JPEG',
        '.jpeg': 'JPEG',
        '.png': 'PNG',
        '.webp': 'WEBP',
        '.gif': 'GIF',
        '.bmp': 'BMP',
        '.tiff': 'TIFF',
        '.tif': 'TIFF'
    }

    # Preset sizes for common use cases
    PRESETS = {
        'thumbnail': (150, 150),
        'avatar': (400, 400),
        'social': (1200, 630),
        'instagram': (1080, 1080),
        'twitter': (1200, 675),
        'facebook': (1200, 630),
        'linkedin': (1200, 627),
        'hd': (1920, 1080),
        '4k': (3840, 2160),
        'small': (800, 600),
        'medium': (1280, 960),
        'large': (1920, 1440)
    }

    def __init__(self, config_path: Optional[str] = None):
        self.config = self._load_config(config_path)
        self.history = []

    def _load_config(self, config_path: Optional[str]) -> dict:
        """Load configuration from file or return defaults."""
        default_config = {
            'default_quality': 85,
            'default_format': 'WEBP',
            'preserve_metadata': True,
            'output_suffix': '_converted',
            'history_file': '.image_converter_history.json'
        }

        if config_path and os.path.exists(config_path):
            try:
                with open(config_path, 'r') as f:
                    return {**default_config, **json.load(f)}
            except Exception:
                pass

        return default_config

    def _get_format(self, filepath: str) -> Optional[str]:
        """Get PIL format from file extension."""
        ext = Path(filepath).suffix.lower()
        return self.FORMAT_MAP.get(ext)

    def _validate_image(self, filepath: str) -> bool:
        """Check if file is a valid image."""
        if not os.path.exists(filepath):
            return False
        ext = Path(filepath).suffix.lower()
        return ext in self.FORMAT_MAP

    def convert_image(
        self,
        input_path: str,
        output_path: Optional[str] = None,
        target_format: Optional[str] = None,
        size: Optional[Tuple[int, int]] = None,
        quality: Optional[int] = None,
        maintain_aspect: bool = True,
        optimize: bool = True
    ) -> dict:
        """
        Convert a single image with optional resizing.

        Args:
            input_path: Path to input image
            output_path: Path for output (auto-generated if None)
            target_format: Output format (JPEG, PNG, WEBP, etc.)
            size: Target size as (width, height)
            quality: Compression quality (1-100)
            maintain_aspect: Keep aspect ratio when resizing
            optimize: Apply optimization

        Returns:
            dict with conversion results
        """
        if not PIL_AVAILABLE:
            return {'success': False, 'error': 'Pillow not installed'}

        if not self._validate_image(input_path):
            return {'success': False, 'error': f'Invalid or unsupported image: {input_path}'}

        try:
            # Open image
            with Image.open(input_path) as img:
                # Convert to RGB if necessary (for JPEG/WebP)
                if target_format in ['JPEG', 'WEBP'] and img.mode in ('RGBA', 'P'):
                    img = img.convert('RGB')

                original_size = img.size

                # Resize if specified
                if size:
                    if maintain_aspect:
                        img.thumbnail(size, Image.Resampling.LANCZOS)
                    else:
                        img = img.resize(size, Image.Resampling.LANCZOS)

                # Determine output format
                if not target_format:
                    if output_path:
                        ext = Path(output_path).suffix.lower()
                        target_format = self.FORMAT_MAP.get(ext, 'PNG')
                    else:
                        target_format = self.config['default_format']

                # Generate output path if not provided
                if not output_path:
                    input_name = Path(input_path).stem
                    output_dir = Path(input_path).parent
                    ext = target_format.lower()
                    if ext == 'jpeg':
                        ext = 'jpg'
                    output_path = output_dir / f"{input_name}{self.config['output_suffix']}.{ext}"

                # Save with appropriate options
                save_kwargs = {}
                if target_format in ['JPEG', 'WEBP']:
                    save_kwargs['quality'] = quality or self.config['default_quality']
                    save_kwargs['optimize'] = optimize
                elif target_format == 'PNG':
                    save_kwargs['optimize'] = optimize

                img.save(output_path, target_format, **save_kwargs)

                # Get file sizes for comparison
                original_bytes = os.path.getsize(input_path)
                converted_bytes = os.path.getsize(output_path)
                savings_percent = ((original_bytes - converted_bytes) / original_bytes) * 100

                result = {
                    'success': True,
                    'input': str(input_path),
                    'output': str(output_path),
                    'original_size': original_size,
                    'final_size': img.size,
                    'original_bytes': original_bytes,
                    'converted_bytes': converted_bytes,
                    'savings_percent': round(savings_percent, 2),
                    'format': target_format
                }

                self.history.append(result)
                return result

        except Exception as e:
            return {'success': False, 'error': str(e)}

    def batch_convert(
        self,
        input_dir: str,
        output_dir: Optional[str] = None,
        target_format: str = 'WEBP',
        size_preset: Optional[str] = None,
        quality: int = 85,
        recursive: bool = False
    ) -> List[dict]:
        """
        Convert all images in a directory.

        Args:
            input_dir: Directory containing images
            output_dir: Output directory (auto-created if None)
            target_format: Target format for all images
            size_preset: Use a named preset (thumbnail, social, etc.)
            quality: Compression quality
            recursive: Process subdirectories

        Returns:
            List of conversion results
        """
        if not PIL_AVAILABLE:
            return [{'success': False, 'error': 'Pillow not installed'}]

        input_path = Path(input_dir)
        if not input_path.exists():
            return [{'success': False, 'error': f'Directory not found: {input_dir}'}]

        # Create output directory
        if output_dir:
            output_path = Path(output_dir)
        else:
            output_path = input_path / 'converted'
        output_path.mkdir(exist_ok=True)

        # Get size from preset
        size = None
        if size_preset and size_preset in self.PRESETS:
            size =