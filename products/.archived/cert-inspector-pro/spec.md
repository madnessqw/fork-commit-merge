# Certificate Inspector Pro - Product Spec

## Overview
SSL/TLS certificate analyzer. Decode certificates, check expiration, validate chains.

## Features
- Paste certificate PEM or connect to domain
- Decode certificate details (subject, issuer, validity)
- Check expiration dates with countdown
- Validate certificate chain
- Security recommendations (weak algorithms, expiry alerts)
- Export certificate info

## API Endpoints
- POST /api/cert/decode - Decode certificate PEM
- POST /api/cert/check - Check domain certificate
- POST /api/cert/validate - Validate certificate chain

## Tech Stack
- Frontend: Vanilla HTML + Tailwind CSS
- Backend: Vercel serverless functions
- Certificate parsing: node-forge or Web Crypto

## Pricing
$19 one-time

## Target Audience
DevOps engineers, security professionals, developers

## Marketing Angle
"Inspect SSL certificates in seconds"

## Design Notes
- Dark theme with security-focused colors
- Certificate tree visualization
- Expiry warning badges
- PEM text area with syntax highlighting
