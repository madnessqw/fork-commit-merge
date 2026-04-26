# Binary Converter Pro - Product Spec

## Overview
Convert between Binary, Hex, Decimal, Octal. Support for ASCII/UTF-8 text encoding.

## Features
- Binary ↔ Hex ↔ Decimal ↔ Octal conversion
- Real-time conversion as you type
- Text to binary/hex conversion
- Bitwise operations (AND, OR, XOR, NOT, shift)
- Binary calculator with arithmetic
- Binary display with bit toggles

## API Endpoints
- POST /api/convert/number - Number base conversion
- POST /api/convert/text - Text to binary/hex
- POST /api/calculate/bitwise - Bitwise operations

## Tech Stack
- Frontend: Vanilla HTML + Tailwind CSS
- Backend: Vercel serverless functions
- No external deps - native JS BigInt

## Pricing
$19 one-time

## Target Audience
Developers, students, embedded systems engineers

## Marketing Angle
"Number base conversion made simple"

## Design Notes
- Dark theme with neon accent colors
- Live preview panel
- Binary bit visualizer (32/64 bit)
- Copy buttons for each format
