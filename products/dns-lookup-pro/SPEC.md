# DNS Lookup Pro — SPEC.md

## 1. Concept & Vision
Professional DNS lookup with multiple record types and global propagation checking. Domain input → comprehensive DNS analysis.

## 2. Design Language
- **Aesthetic**: Network/diagnostic tool, data-dense but clean
- **Colors**: #0a0a0f bg, #06b6d4 cyan accent, #22c55e resolved, #ef4444 error
- **Typography**: Inter + JetBrains Mono for DNS data
- **Motion**: Results fade in as each record type resolves

## 3. Layout & Structure
- Top: domain input field + record type selector + lookup button
- Record types: A, AAAA, MX, TXT, CNAME, NS, SOA, PTR
- Main: results grouped by record type
- Each result: value, TTL, priority (for MX)

## 4. Features & Interactions
- Domain input with validation
- Record type multi-select (checkboxes)
- Batch lookup: run all selected record types
- Results display: value, TTL, class, priority
- Copy individual values
- DNSSEC validation status indicator
- Response time display

## 5. Component Inventory
- Domain input (validated)
- Record type chips (multi-select)
- Lookup button
- Result card (record type header + value list)
- DNSSEC badge (secure/insecure/bogus)
- Copy button per value

## 6. Technical Approach
- Vanilla HTML + Tailwind CDN
- Uses browser's DNS over HTTPS (via fetch to dns.google or cloudflare-dns.com)
- Client-side DNSAPI via fetch() to public DNS-over-HTTPS endpoints
