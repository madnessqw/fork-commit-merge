# CSV Validator Pro

Validate CSV files with auto-detection, schema rules, and detailed error reports.

**Live:** [https://csv-validator-pro.vercel.app](https://csv-validator-pro.vercel.app)

**Price:** $19 (one-time) — [Buy on Polar](https://buy.polar.sh/polar_cl_xfPwLDlKpqDEKLyPzApqOIJRuzBwNrhIPU8I71qUdgV)

---

## Features

### Smart Delimiter Detection
Automatically detects comma (`,`), semicolon (`;`), tab (`\t`), and pipe (`|`) delimiters. Handles quoted fields, escaped quotes, and inconsistent spacing.

### Schema Validation
Define validation rules per column:
- **string** — non-empty value check
- **number** — numeric values (integers, decimals, negatives)
- **date** — valid date parsing
- **email** — RFC-style email validation
- **regex** — custom regular expression patterns

### Data Type Validation
Each cell is validated against its declared type. Invalid values are flagged with precise row/column information.

### Encoding Detection
Automatically detects:
- UTF-8 (with and without BOM)
- UTF-16 (LE and BE)
- ASCII
- Windows-1252
- ISO-8859-1

### Column Count Consistency
Checks every row against the header row (or schema) for consistent column counts. Flags rows with too few or too many columns.

### Row-Level Error Reporting
Every error includes:
- Row number
- Column name
- Error type and severity
- Expected format vs. actual value

### Bulk Processing
Chunked validation for large files (100K+ rows). Real-time progress bar, non-blocking UI, no freezes.

### Export Reports
Download validation results as:
- **JSON** — full structured report
- **CSV** — error list with all metadata

---

## Usage

### 1. Upload File
Drag & drop a CSV file onto the upload zone, or click to browse. Supports `.csv`, `.tsv`, and `.txt` files.

### 2. Configure Schema (Optional)
Click **Auto-detect from header** to auto-generate schema rules based on your column headers. Or manually add rules:

1. Click **Add Rule**
2. Enter the column name (must match header)
3. Select the type (string, number, date, email, regex)
4. For regex: enter the pattern

### 3. Set Options
- **First row is header** — treat the first row as column names
- **Trim whitespace** — ignore leading/trailing spaces
- **Strict column count** — flag rows with mismatched column counts
- **Detect encoding** — auto-detect file encoding

### 4. Validate
Click **Validate CSV** to run the validation. Progress is shown in real-time.

### 5. Review Results
Switch between tabs:
- **Preview** — browse parsed CSV data
- **Errors** — detailed per-error breakdown
- **Statistics** — aggregate metrics and error distribution

### 6. Export
Download the full report (JSON) or just errors (CSV).

---

## Tech Stack

| Component | Technology |
|-----------|-----------|
| Frontend | Vanilla JavaScript (ES6+) |
| Styling | Tailwind CSS (CDN) |
| Font | Inter + JetBrains Mono (Google Fonts) |
| Deployment | Vercel |
| Payments | Polar (one-time $19) |

---

## Architecture

All processing happens **client-side** in the browser. Files are never uploaded to any server.

```
┌─────────────────────────────────────────────┐
│                 Browser                      │
│                                              │
│  File → ArrayBuffer → Encoding Detection    │
│       → Delimiter Detection                  │
│       → CSV Parser                           │
│       → Schema Validator                     │
│       → Error Reporter                       │
│       → JSON/CSV Export                      │
└─────────────────────────────────────────────┘
        (No server involvement)
```

### Key Modules

| Module | Responsibility |
|--------|---------------|
| Encoding Detection | Byte-level analysis for UTF-8/16/Windows-1252/ASCII |
| Delimiter Detection | Statistical scoring across 4 delimiters |
| CSV Parser | RFC-4180 compliant with quote escaping |
| Type Validators | Per-type validation functions (string, number, date, email, regex) |
| Chunked Processor | Async validation with progress reporting |

---

## Privacy

CSV Validator Pro is 100% browser-based. Your files are processed entirely on your device — they never leave your computer.

---

## License

One-time purchase for CSV Validator Pro. Includes lifetime access and all future updates.
