# 📱 QR Code Generator

A powerful, standalone Python tool for generating QR codes for URLs, WiFi networks, contact cards, emails, phone numbers, SMS messages, and plain text.

## Features

✅ **Multiple QR Types**: URL, Text, WiFi, Email, Contact (vCard), Phone, SMS  
✅ **Customizable**: Colors, sizes, error correction levels, borders  
✅ **Logo Support**: Embed your logo in the center of QR codes  
✅ **Interactive Mode**: Step-by-step guided creation  
✅ **CLI Mode**: Quick generation with command-line arguments  
✅ **Zero Dependencies**: Only requires `qrcode` and `Pillow`  
✅ **Cross-Platform**: Works on Windows, macOS, and Linux  

## Installation

### Option 1: Direct Download
Download `qr_generator.py` and run it directly:

```bash
python qr_generator.py --interactive
```

### Option 2: Install Dependencies
```bash
pip install qrcode[pil]
```

## Usage

### Interactive Mode (Recommended for beginners)
```bash
python qr_generator.py --interactive
# or simply:
python qr_generator.py
```

### Quick Examples

**Generate a URL QR code:**
```bash
python qr_generator.py -d "https://example.com" -o website.png
```

**Generate a WiFi QR code:**
```bash
python qr_generator.py --wifi "MyNetwork" -p "password123" -o wifi.png
```

**Generate a contact card:**
```bash
python qr_generator.py --contact "John Doe" --phone "+1234567890" --email "john@example.com" -o contact.png
```

**Generate an email QR code:**
```bash
python qr_generator.py --to "contact@example.com" --subject "Hello" --body "Message here" -o email.png
```

**Add a logo to your QR code:**
```bash
python qr_generator.py -d "https://example.com" --logo logo.png -o branded.png
```

**Customize colors:**
```bash
python qr_generator.py -d "https://example.com" --fg-color "#0066cc" --bg-color "#f0f0f0" -o colored.png
```

## QR Code Types

### 1. URL/Website
Creates a scannable link to any website.

### 2. Plain Text
Encode any text message, notes, or information.

### 3. WiFi Network
Generate QR codes that automatically connect devices to WiFi:
- Works with all modern phones (iOS 11+, Android 10+)
- Supports WPA, WEP, and open networks
- Option for hidden networks

### 4. Email
Pre-filled email messages with recipient, subject, and body.

### 5. Contact Card (vCard)
Standard vCard format compatible with all phones:
- Name, phone, email, organization
- Imports directly to contacts app

### 6. Phone Number
Direct dial QR codes for instant calling.

### 7. SMS
Pre-composed text messages ready to send.

## Advanced Options

| Option | Description | Default |
|--------|-------------|---------|
| `--box-size` | Size of each QR module in pixels | 10 |
| `--border` | Border width in modules | 4 |
| `--error-correction` | Error correction level (L/M/Q/H) | M |
| `--fg-color` | Foreground/QR color | black |
| `--bg-color` | Background color | white |
| `--logo` | Path to logo image to embed | none |

### Error Correction Levels

- **L** (Low): ~7% correction capability
- **M** (Medium): ~15% correction capability ✓ Recommended
- **Q** (Quartile): ~25% correction capability
- **H** (High): ~30% correction capability - Required for logos

## Use Cases

🏢 **Business**: Put on business cards, flyers, storefronts  
🏠 **Personal**: WiFi sharing, contact sharing, event invites  
📦 **Products**: Link to manuals, warranty info, support  
🎫 **Events**: Tickets, schedules, venue maps  
📱 **Marketing**: Campaign tracking, social media links  
🔐 **Security**: 2FA backup codes, secure note sharing  

## Output Examples

All generated QR codes are saved as PNG images with:
- High resolution (suitable for print)
- Transparent background option (use "transparent" as bg-color)
- Customizable dimensions

## Tips

1. **Test before printing**: Always scan the QR code before mass printing
2. **Size matters**: For print, use at least 2cm × 2cm for reliable scanning
3. **Contrast is key**: Ensure good contrast between foreground and background
4. **Logo placement**: Use high error correction (H) when adding logos
5. **Short URLs**: Use URL shorteners for cleaner, more scannable codes

## License

MIT License - Feel free to use for personal and commercial projects.

## Support

For issues or feature requests, please refer to the documentation or contact the developer.

---

**Version**: 1.0.0  
**Requires**: Python 3.6+  
**Dependencies**: qrcode, Pillow
