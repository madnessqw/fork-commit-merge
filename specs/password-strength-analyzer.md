# Password Strength Analyzer Pro - Product Spec

## Overview
Advanced password security analysis tool for developers and security teams. Evaluate password strength, check breach databases, and get actionable recommendations for stronger credentials.

## Features
1. **Strength Analysis**
   - Entropy calculation
   - Brute-force time estimate
   - Pattern detection
   - Dictionary word check
   - Sequential character detection

2. **Breach Checking**
   - Have I Been Pwned API integration
   - Known breach database check
   - Hash-based secure lookup
   - Breach count display

3. **Password Generator**
   - Customizable length
   - Character type selection
   - Memorable passphrase mode
   - Pronounceable passwords
   - Copy to clipboard

4. **Security Reports**
   - Visual strength meter
   - Improvement suggestions
   - Security score
   - Export report as PDF

## Technical Spec
- HTML/JS frontend
- zxcvbn library for strength analysis
- SHA-1 hash for breach checking (k-anon)
- Crypto API for generation
- Dark theme default
- Mobile responsive

## Monetization
- Free: Basic strength check, 5 breach lookups/day
- Pro ($19): Unlimited checks, bulk analysis, API access, team reports, password policy config

## Landing Page Sections
1. Hero: Animated password strength visualization
2. Interactive analyzer demo
3. Breach check feature
4. Password generator
5. Security best practices
6. Pricing
7. FAQ

## Files Structure
```
password-strength-analyzer/
├── index.html (600+ lines)
├── api/
│   ├── health.js
│   └── webhook.js
├── package.json
└── vercel.json
```

## Keywords
password strength, password checker, security analyzer, breach checker, password generator, credential security, zxcvbn, entropy calculator

## SEO Title
Password Strength Analyzer — Check Security & Breach Status

## SEO Description
Analyze password strength with entropy calculation and breach database checking. Generate secure passwords. Professional security tool for developers and teams.
