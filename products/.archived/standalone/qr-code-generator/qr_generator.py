#!/usr/bin/env python3
"""
QR Code Generator - Standalone Tool
Generates QR codes for URLs, text, WiFi, contact cards, and more.
Zero dependencies beyond Python standard library + qrcode/pillow.
"""

import argparse
import sys
import os
from datetime import datetime
from pathlib import Path

# Try to import qrcode, provide fallback if not available
try:
    import qrcode
    from qrcode.constants import ERROR_CORRECT_L, ERROR_CORRECT_M, ERROR_CORRECT_Q, ERROR_CORRECT_H
    QRCODE_AVAILABLE = True
except ImportError:
    QRCODE_AVAILABLE = False

try:
    from PIL import Image
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

__version__ = "1.0.0"


def print_banner():
    """Print the tool banner."""
    banner = """
╔══════════════════════════════════════════════════════════╗
║              📱 QR CODE GENERATOR v1.0.0                 ║
║         Generate QR codes for any purpose               ║
╚══════════════════════════════════════════════════════════╝
    """
    print(banner)


def check_dependencies():
    """Check if required dependencies are available."""
    if not QRCODE_AVAILABLE:
        print("❌ Error: 'qrcode' module not found.")
        print("   Install with: pip install qrcode[pil]")
        return False
    if not PIL_AVAILABLE:
        print("❌ Error: 'Pillow' module not found.")
        print("   Install with: pip install Pillow")
        return False
    return True


def generate_wifi_qr(ssid, password, security="WPA", hidden=False):
    """Generate WiFi QR code string."""
    hidden_str = ";H:true" if hidden else ""
    return f"WIFI:T:{security};S:{ssid};P:{password}{hidden_str};;"


def generate_contact_qr(name, phone, email="", org=""):
    """Generate vCard QR code string."""
    vcard = f"BEGIN:VCARD\nVERSION:3.0\nFN:{name}\n"
    if phone:
        vcard += f"TEL:{phone}\n"
    if email:
        vcard += f"EMAIL:{email}\n"
    if org:
        vcard += f"ORG:{org}\n"
    vcard += "END:VCARD"
    return vcard


def generate_email_qr(email, subject="", body=""):
    """Generate email QR code string."""
    qr_data = f"mailto:{email}"
    if subject or body:
        qr_data += "?"
        if subject:
            qr_data += f"subject={subject.replace(' ', '%20')}"
        if body:
            if subject:
                qr_data += "&"
            qr_data += f"body={body.replace(' ', '%20')}"
    return qr_data


def generate_qr_code(data, filename, error_correction="M", box_size=10, border=4, 
                     fg_color="black", bg_color="white", logo_path=None):
    """Generate a QR code image."""
    
    # Map error correction string to constant
    ec_map = {
        "L": ERROR_CORRECT_L,
        "M": ERROR_CORRECT_M,
        "Q": ERROR_CORRECT_Q,
        "H": ERROR_CORRECT_H
    }
    error_correction = ec_map.get(error_correction.upper(), ERROR_CORRECT_M)
    
    # Create QR code instance
    qr = qrcode.QRCode(
        version=None,
        error_correction=error_correction,
        box_size=box_size,
        border=border,
    )
    
    qr.add_data(data)
    qr.make(fit=True)
    
    # Create image
    img = qr.make_image(fill_color=fg_color, back_color=bg_color)
    
    # Add logo if provided
    if logo_path and os.path.exists(logo_path):
        try:
            logo = Image.open(logo_path)
            # Resize logo to fit in center (max 20% of QR size)
            qr_width, qr_height = img.size
            logo_size = int(qr_width * 0.2)
            logo = logo.resize((logo_size, logo_size), Image.Resampling.LANCZOS)
            
            # Calculate position
            pos = ((qr_width - logo_size) // 2, (qr_height - logo_size) // 2)
            
            # Paste logo
            if logo.mode == 'RGBA':
                img.paste(logo, pos, logo)
            else:
                img.paste(logo, pos)
        except Exception as e:
            print(f"⚠️  Warning: Could not add logo: {e}")
    
    # Save image
    img.save(filename)
    return filename


def interactive_mode():
    """Run in interactive mode."""
    print_banner()
    
    if not check_dependencies():
        return 1
    
    print("\n📋 QR Code Types:")
    print("   1. URL/Website")
    print("   2. Plain Text")
    print("   3. WiFi Network")
    print("   4. Email Message")
    print("   5. Contact Card (vCard)")
    print("   6. Phone Number")
    print("   7. SMS Message")
    
    choice = input("\nSelect type (1-7): ").strip()
    
    if choice == "1":
        data = input("Enter URL: ").strip()
        if not data.startswith(('http://', 'https://')):
            data = 'https://' + data
        filename = input("Output filename (default: qr_url.png): ").strip() or "qr_url.png"
        
    elif choice == "2":
        print("Enter text (press Enter twice to finish):")
        lines = []
        while True:
            line = input()
            if line == "":
                break
            lines.append(line)
        data = "\n".join(lines)
        filename = input("Output filename (default: qr_text.png): ").strip() or "qr_text.png"
        
    elif choice == "3":
        ssid = input("WiFi Network Name (SSID): ").strip()
        password = input("WiFi Password: ").strip()
        security = input("Security type (WPA/WEP/nopass, default: WPA): ").strip().upper() or "WPA"
        hidden = input("Hidden network? (y/n, default: n): ").strip().lower() == "y"
        data = generate_wifi_qr(ssid, password, security, hidden)
        filename = input("Output filename (default: qr_wifi.png): ").strip() or "qr_wifi.png"
        
    elif choice == "4":
        email = input("Email address: ").strip()
        subject = input("Subject (optional): ").strip()
        body = input("Body text (optional): ").strip()
        data = generate_email_qr(email, subject, body)
        filename = input("Output filename (default: qr_email.png): ").strip() or "qr_email.png"
        
    elif choice == "5":
        name = input("Full Name: ").strip()
        phone = input("Phone Number: ").strip()
        email = input("Email (optional): ").strip()
        org = input("Organization (optional): ").strip()
        data = generate_contact_qr(name, phone, email, org)
        filename = input("Output filename (default: qr_contact.png): ").strip() or "qr_contact.png"
        
    elif choice == "6":
        phone = input("Phone Number: ").strip()
        data = f"tel:{phone}"
        filename = input("Output filename (default: qr_phone.png): ").strip() or "qr_phone.png"
        
    elif choice == "7":
        phone = input("Phone Number: ").strip()
        message = input("Message: ").strip()
        data = f"SMSTO:{phone}:{message}"
        filename = input("Output filename (default: qr_sms.png): ").strip() or "qr_sms.png"
        
    else:
        print("❌ Invalid choice")
        return 1
    
    if not data:
        print("❌ Error: No data provided")
        return 1
    
    # Advanced options
    print("\n⚙️  Advanced Options (press Enter for defaults):")
    box_size = input("Box size (default: 10): ").strip()
    box_size = int(box_size) if box_size.isdigit() else 10
    
    border = input("Border size (default: 4): ").strip()
    border = int(border) if border.isdigit() else 4
    
    ec = input("Error correction (L/M/Q/H, default: M): ").strip().upper() or "M"
    
    fg = input("Foreground color (default: black): ").strip() or "black"
    bg = input("Background color (default: white): ").strip() or "white"
    
    logo = input("Logo image path (optional): 