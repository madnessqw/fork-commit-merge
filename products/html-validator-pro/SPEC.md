# HTML Validator Pro — SPEC.md

## 1. Concept & Vision
W3C standards HTML validation with accessibility checks and SEO analysis. Paste HTML → get detailed validation report.

## 2. Design Language
- **Aesthetic**: Professional audit tool, clean report format
- **Colors**: #0a0a0f bg, #ef4444 error red, #22c55e pass green, #f59e0b warning amber
- **Typography**: Inter + monospace for HTML snippets
- **Motion**: Report items fade in sequentially

## 3. Layout & Structure
- Top: title + "Paste HTML" textarea
- Main: validation report with sections
  - Errors (red) — critical issues
  - Warnings (amber) — recommendations
  - Info (blue) — suggestions
- Each item: line number, snippet, rule reference

## 4. Features & Interactions
- Paste HTML → instant validation (no button needed after paste)
- W3C HTML5 standard checks
- WCAG 2.1 accessibility audit
- SEO meta tag analysis
- Broken link detection
- Report sections collapsible
- Copy individual snippets

## 5. Component Inventory
- HTML input textarea (large)
- Section accordion (Errors/Warnings/Info)
- Issue card (severity icon, line#, snippet, message)
- Snippet block (monospace, highlighted line)
- Fix suggestion tooltip

## 6. Technical Approach
- Vanilla HTML + Tailwind CDN
- Client-side HTML parsing (DOMParser)
- Validation rules as vanilla JS functions
- No external API calls
