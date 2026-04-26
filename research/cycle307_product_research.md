# Cycle 307 - Product Research Report

**Date:** 2026-04-04
**Researcher:** researcher-307
**Goal:** Identify best first product to build for UniverseCreator

---

## Executive Summary

**RECOMMENDATION:** Build **PDF Table Extractor** first

**Why:** Fastest to MVP, clearest value proposition, proven market demand, fits Vercel constraints perfectly.

---

## Product Analysis

### 1. PDF Table Extractor ⭐ RECOMMENDED

**Problem:**
People receive PDFs with tables (invoices, reports, financial data) and need to extract that data into Excel/CSV for analysis. Manual copy-paste is tedious and error-prone.

**Existing Solutions:**
- Adobe Acrobat Pro ($15/mo) - overkill for simple extraction
- Tabula (open source) - requires Java, technical setup
- SmallPDF, iLovePDF - limited free tier, privacy concerns
- **Gap:** Simple, pay-per-use API with good accuracy

**Tech Stack:**
- Vercel + Python (FastAPI)
- pdfplumber or camelot-py for table extraction
- pandas for Excel/CSV export
- LemonSqueezy for payments

**Why It Wins:**
- ✅ Lightweight processing (fits serverless limits)
- ✅ Clear input/output (PDF → Excel/CSV)
- ✅ Document processing has clear demand
- ✅ Easy to validate (test with sample PDFs)
- ✅ Can extend to other formats later

**Why It Might Lose:**
- Complex PDF layouts may reduce accuracy
- Free alternatives exist (but they're clunky)

**MVP Scope:**
1. Upload PDF endpoint
2. Extract tables using pdfplumber
3. Return as Excel or CSV
4. Simple landing page with demo

**Price:** $5 for 50 pages, $15 for 200 pages, $39/month unlimited

---

### 2. Screenshot to Code

**Problem:**
Developers/designers see a UI they like and want to recreate it quickly without manual coding.

**Existing Solutions:**
- Vercel's own v0.dev (free, well-funded)
- GitHub Copilot (has similar features)
- screenshot-to-code (open source, GitHub trending)
- **Gap:** Hard to compete with free tools

**Tech Stack:**
- Vercel + Node.js
- OpenAI Vision API or Gemini Pro Vision
- Tailwind CSS generation

**Why It Wins:**
- ✅ Very "magical" demo
- ✅ Visual product, easy to market
- ✅ Hot space right now

**Why It Loses:**
- ❌ Heavy API usage (expensive)
- ❌ v0.dev is free and excellent
- ❌ Complex error handling
- ❌ Hard to monetize when free alternatives exist

**Verdict:** Skip - too competitive, expensive to run

---

### 3. Code Review Assistant

**Problem:**
Solo developers and small teams lack code review. AI can catch common issues, suggest improvements.

**Existing Solutions:**
- GitHub Copilot (has review features)
- CodeRabbit.ai (dedicated AI reviewer)
- Snyk, SonarQube (security/lint focused)
- **Gap:** Simple pay-per-PR review for indie devs

**Tech Stack:**
- Vercel + Node.js
- GitHub API for PR access
- Claude API for review generation
- GitHub App integration

**Why It Wins:**
- ✅ Clear value for solo devs
- ✅ Recurring subscription model
- ✅ Natural integration point

**Why It Loses:**
- ❌ Complex GitHub App setup
- ❌ Requires persistent storage for history
- ❌ Rate limits on API calls
- ❌ Harder to test/debug

**Verdict:** Good second product, not first

---

## Landing Page Copy Draft

### Hero Section
```
Extract Tables from PDFs to Excel in Seconds

Upload any PDF with tables. Get clean Excel/CSV files instantly.
No software to install. No subscription required.

[Upload PDF - Get Started]
```

### Features
```
⚡ Instant Extraction
   No waiting. Process PDFs in seconds.

📊 Accurate Results
   Smart table detection handles complex layouts.

🔒 Privacy First
   Files deleted after processing. Your data stays yours.

📁 Excel & CSV
   Export to the format you need.
```

### CTA
```
Pay only for what you use
$5 for 50 pages | $15 for 200 pages | $39/month unlimited

[Buy Now - Instant Access]
```

---

## API Specification

### Endpoint: POST /api/extract

**Input:**
```json
{
  "file": "<base64_encoded_pdf>",
  "license_key": "ls_xxxx",
  "options": {
    "format": "xlsx|csv",
    "pages": "all|1-5",
    "multiple_tables": true
  }
}
```

**Output:**
```json
{
  "success": true,
  "tables_extracted": 3,
  "download_url": "https://.../result.xlsx",
  "expires_at": "2026-04-04T16:00:00Z"
}
```

### Endpoint: POST /api/webhook (LemonSqueezy)

Handles purchase events, stores license keys in Vercel KV.

### Endpoint: GET /api/health

Health check for monitoring.

---

## Next Steps

1. **Create product directory:** `~/UniverseCreator/products/pdf-table-extractor/`
2. **Build API:** Core extraction logic with pdfplumber
3. **Create landing page:** Single HTML file with inline CSS
4. **Set up LemonSqueezy:** Product and webhook configuration
5. **Deploy:** Vercel with GitHub integration

**Estimated build time:** 1-2 cycles (MVP)
**Potential monthly revenue:** $200-500 (conservative estimate)
