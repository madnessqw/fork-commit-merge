# Hash Compare Pro - Product Spec

## Overview
File hash comparison tool for integrity verification. Compare MD5, SHA1, SHA256, SHA512 hashes.

## Features
- Calculate hashes for files and text
- Compare two hashes for equality
- Batch file hash verification
- Hash history and bookmarks
- Visual diff highlighting
- Support: MD5, SHA1, SHA256, SHA384, SHA512

## API Endpoints
- POST /api/hash/calculate - Calculate file/text hash
- POST /api/hash/compare - Compare two hashes
- POST /api/hash/verify - Verify file against known hash

## Tech Stack
- Frontend: Vanilla HTML + Tailwind CSS
- Backend: Vercel serverless functions
- Hash: Web Crypto API

## Pricing
$19 one-time

## Target Audience
Developers, security auditors, file integrity checkers

## Marketing Angle
"Verify file integrity instantly"

## Design Notes
- Dark theme with gradient accents
- Drag-drop file upload
- Side-by-side hash comparison
- Green/red match indicator
