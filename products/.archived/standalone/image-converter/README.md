# Universal Image Converter

A powerful Python tool for batch converting, resizing, and optimizing images. Supports 6+ formats with preset sizes for social media, web optimization, and batch processing.

## Features

- **Multi-Format Support**: JPG, PNG, WEBP, GIF, BMP, TIFF
- **Batch Processing**: Convert entire directories at once
- **Smart Presets**: Pre-configured sizes for social media platforms
- **Quality Control**: Adjustable compression (1-100)
- **Aspect Ratio**: Optional aspect ratio preservation
- **Size Optimization**: Automatic file size reduction
- **Recursive Mode**: Process subdirectories
- **History Tracking**: Save conversion logs

## Quick Start

### Interactive Mode (Recommended)
```bash
python image_converter.py
```

### Command Line
```bash
# Convert single image to WEBP
python image_converter.py photo.jpg -f WEBP -q 85

# Resize to social media size
python image_converter.py photo.jpg -p social -f WEBP

# Batch convert directory
python image_converter.py ./images -f WEBP -r

# Custom size
python image_converter.py photo.jpg -s 800x600 -f JPEG -q 90
```

## Size Presets

| Preset | Dimensions | Use Case |
|--------|-----------|----------|
| thumbnail | 150x150 | Icons, avatars |
| avatar | 400x400 | Profile pictures |
| social | 1200x630 | General social media |
| instagram | 1080x1080 | Instagram posts |
| twitter | 1200x675 | Twitter/X cards |
| facebook | 1200x630 | Facebook posts |
| linkedin | 1200x627 | LinkedIn shares |
| hd | 1920x1080 | HD displays |
| 4k | 3840x2160 | 4K displays |
| small | 800x600 | Email attachments |
| medium | 1280x960 | Web galleries |
| large | 1920x1440 | High-res web |

## Examples

### Optimize for Web
```bash
# Convert all images to WEBP (best compression)
python image_converter.py ./photos -f WEBP -q 85 -r
```

### Create Thumbnails
```bash
# Generate thumbnails preserving aspect ratio
python image_converter.py photo.jpg -p thumbnail -f PNG
```

### Social Media Batch
```bash
# Prepare images for Instagram
python image_converter.py ./raw -p instagram -f JPEG -q 95 -r
```

## Installation

1. Install Python 3.7+
2. Install Pillow:
```bash
pip install Pillow
```
3. Download `image_converter.py`
4. Run: `python image_converter.py`

## CLI Options

```
usage: image_converter.py [-h] [-o OUTPUT] [-f {JPEG,PNG,WEBP,GIF,BMP,TIFF}]
                          [-q QUALITY] [-s SIZE] [-p PRESET] [-r]
                          [--no-aspect] [-i]
                          input

positional arguments:
  input                 Input image file or directory

optional arguments:
  -h, --help            show help message
  -o, --output          Output file or directory
  -f, --format          Output format (default: WEBP)
  -q, --quality         Compression quality 1-100 (default: 85)
  -s, --size            Target size (e.g., 800x600)
  -p, --preset          Use size preset
  -r, --recursive       Process subdirectories
  --no-aspect           Don't maintain aspect ratio
  -i, --interactive     Interactive mode
```

## Output

After conversion, you'll see:
- ✅ Success message
- 📊 File size reduction percentage
- 💾 History saved to `.image_converter_history.json`

## Use Cases

- **Web Developers**: Optimize images for faster loading
- **Content Creators**: Batch resize for social media
- **Photographers**: Convert RAW exports to web formats
- **E-commerce**: Standardize product image sizes
- **Bloggers**: Optimize featured images
- **Designers**: Create asset libraries

## Tips

- **WEBP** offers best compression with quality
- **PNG** for images needing transparency
- **JPEG** for maximum compatibility
- Quality 85-90 is the sweet spot for web
- Use `-r` flag for batch processing folders
- History file tracks all conversions

## License

MIT License - Feel free to use commercially
