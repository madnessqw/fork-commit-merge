# JSON Schema Generator — SPEC.md

## 1. Concept & Vision
Generate JSON Schema from sample JSON instantly. Infer types, validation rules, customizable depth. Clean, professional developer tool aesthetic.

## 2. Design Language
- **Aesthetic**: Developer tool, clean lines, monospace accents
- **Colors**: #0a0a0f bg, #6366f1 accent, #22c55e success green
- **Typography**: Inter + JetBrains Mono for code
- **Motion**: Minimal — instant feedback on schema generation

## 3. Layout & Structure  
- Single-page app
- Left: JSON input textarea (large, monospace)
- Right: Generated schema output (read-only, monospace)
- Top bar: title, schema version selector (Draft-07, 2019-09, 2020-12)
- Options: depth control, required field detection, enum extraction

## 4. Features & Interactions
- Paste JSON → instant schema generation (no button needed)
- Schema version selector (dropdown)
- Copy schema button
- Depth slider (1-10)
- Toggle: required fields, enum extraction, pattern recognition
- Export formats: JSON, TypeScript interface

## 5. Component Inventory
- JSON input textarea (monospace, syntax-highlighted bg)
- Schema output textarea (read-only, monospace)
- Version dropdown selector
- Toggle switches for options
- Copy button (clipboard icon, "Copied!" feedback)
- Export dropdown (JSON / TypeScript)

## 6. Technical Approach
- Vanilla HTML + Tailwind CDN
- Client-side schema inference (no backend)
- Schema generation algorithm in vanilla JS
