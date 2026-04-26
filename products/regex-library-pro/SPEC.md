# Regex Library Pro — SPEC.md

## 1. Concept & Vision
Curated collection of 100+ production-ready regex patterns with instant testing. Each pattern includes explanation and battle-tested defaults.

## 2. Design Language
- **Aesthetic**: Developer tool, organized categories, clear pattern cards
- **Colors**: #0a0a0f bg, #8b5cf6 purple accent, #22c55e match highlight
- **Typography**: Inter + JetBrains Mono for regex
- **Motion**: Match highlighting animates on input change

## 3. Layout & Structure
- Top: search bar + category filter chips
- Main: grid of pattern cards (name, pattern, description, match count)
- Right sidebar: selected pattern detail + live tester
- Detail: pattern, test input, match highlights, copy button

## 4. Features & Interactions
- Browse by category (email, URL, credit card, date, phone, etc.)
- Search patterns by name or pattern text
- Live tester: type test string → see matches highlighted
- Pattern detail modal with copy-ready snippet
- Category filtering via chips

## 5. Component Inventory
- Search input (filter as you type)
- Category chips (horizontal scroll)
- Pattern card (name, first-match preview, category tag)
- Tester panel (input + highlighted output)
- Copy button with "Copied!" feedback

## 6. Technical Approach
- Vanilla HTML + Tailwind CDN
- Client-side pattern matching with RegExp
- LocalStorage for favorite patterns
- Category data hardcoded (100+ patterns)
