# UniverseCreator MCP Server — SPEC.md

## 1. Concept & Vision

**UniverseCreator MCP Server**, geliştiricilerin 182+ UniverseCreator ürününe MCP protokolü üzerinden erişmesini sağlayan bir API gateway. Lyra'nın 2700+ MCP bağlantısı gibi, bu sunucu da tek bir endpoint'ten UniverseCreator'ın tüm ürünlerini expose eder — JSON config, kurulum, deployment gerektirmez.

**Temel değer önerisi:** "MCP protocol ile UniverseCreator ürünlerine 5 saniyede bağlan, hiçbir şey yüklemeye gerek yok."

**Hedef kitle:** Claude Desktop, Cursor, VS Code + Claude Ext, veya herhangi bir MCP client kullanıcıları.

## 2. Design Language

### Aesthetic Direction
Dark terminal aesthetic — tıpkı bir developer tool gibi. Markdown/terminal çıktıları, monospace font, minimal UI.

### Color Palette
- Background: `#0d1117` (GitHub dark)
- Primary: `#58a6ff` (blue link)
- Accent: `#7ee787` (green success)
- Text: `#c9d1d9` (light gray)
- Border: `#30363d`

### Typography
- `JetBrains Mono` — code/terminal output
- `Inter` — UI labels
- Fallback: `monospace`, `system-ui`

### Motion
- Minimal — loading spinner only for async operations
- Tool output appears instantly

## 3. Layout & Structure

### Server Architecture
```
MCP Client (Claude Desktop, Cursor, VS Code)
    ↓
UniverseCreator MCP Server (this)
    ↓
UniverseCreator REST API endpoints
    ↓
182+ Products
```

### Single HTML Interface
Hem MCP protocol endpoint'i (JSON-RPC) hem de insan-beklenen bir web arayüzü — aynı portta.

**URL:** `universe-mcp-server.vercel.app` (Vercel serverless)

**Routing:**
- `GET /` — Web arayüzü (tool list, test panel)
- `POST /mcp` — MCP JSON-RPC handler
- `GET /health` — Health check

## 4. Features & Interactions

### MCP Protocol Support (SPDY/gRPC equivalent for HTTP)
**Tools (第一批 — 20 core tools):**

| Tool | Description | Parameters |
|------|-------------|------------|
| `base64_encode` | Encode text to base64 | `text: string` |
| `base64_decode` | Decode base64 to text | `encoded: string` |
| `url_encode` | URL-encode text | `text: string` |
| `url_decode` | URL-decode text | `encoded: string` |
| `html_encode` | HTML-encode text | `text: string` |
| `html_decode` | HTML-decode text | `encoded: string` |
| `json_format` | Pretty-print JSON | `json: string` |
| `json_minify` | Minify JSON | `json: string` |
| `uuid_generate` | Generate UUID v4 | `(none)` |
| `hash_generate` | Generate hashes (md5, sha1, sha256) | `text: string, algorithm: "md5"\|"sha1"\|"sha256"` |
| `cron_validate` | Validate cron expression | `expression: string` |
| `cron_next` | Get next N cron run times | `expression: string, count?: number` |
| `jwt_decode` | Decode JWT without verification | `token: string` |
| `jwt_generate` | Generate JWT (HS256) | `payload: object, secret: string` |
| `color_convert` | Convert between color formats | `color: string, from: string, to: string` |
| `csv_to_json` | Convert CSV to JSON | `csv: string` |
| `xml_format` | Pretty-print XML | `xml: string` |
| `yaml_validate` | Validate YAML syntax | `yaml: string` |
| `timestamp_now` | Get current timestamp | `format?: "unix"\|"iso"\|"date"` |
| `unit_convert` | Convert between units | `value: number, from: string, to: string` |

### Web Interface
- Tool listesi (kategorize edilmiş)
- Her tool için "Test" paneli — input gir, çıktıyı gör
- MCP endpoint bilgisi — "How to connect" rehberi

### Error Handling
- Invalid JSON → `{"error": "Invalid JSON input"}`
- Tool not found → `{"error": "Unknown tool: <tool_name>"}`
- Tool execution error → `{"error": "<tool_error_message>"}`

## 5. Component Inventory

### MCP JSON-RPC Handler
**Request:**
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "base64_encode",
    "arguments": { "text": "hello world" }
  }
}
```

**Response:**
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "content": [
      { "type": "text", "text": "aGVsbG8gd29ybGQ=" }
    ]
  }
}
```

### Tool Registry
In-memory registry of tool definitions. Each tool: name, description, parameter schema (JSON Schema), handler function.

## 6. Technical Approach

### Stack
- **Runtime:** Node.js (serverless-compatible)
- **Framework:** None — vanilla Node.js http module (Vercel serverless uyumlu)
- **Deployment:** Vercel (`vercel --prod`)
- **NPM packages:** None (pure vanilla — minimal cold start)

### File Structure
```
products/universe-mcp-server/
├── SPEC.md
├── index.js          ← Main server (MCP + web UI)
├── package.json
├── public/
│   └── index.html   ← Minimal web UI (served as static)
```

### MCP Protocol
MCP spec: https://modelcontextprotocol.io

UniverseCreator MCP Server implements the **"Tools" capability**:
- `tools/list` — Returns all available tools
- `tools/call` — Executes a named tool with arguments

### Key Implementation Notes
1. Pure HTTP POST endpoint — no WebSocket (Vercel serverless compatible)
2. No external npm packages — vanilla Node.js only
3. All 20 tools implemented as pure functions
4. Static `public/index.html` for web UI

## 7. Success Metrics

- MCP endpoint returns 200 for valid JSON-RPC requests
- All 20 tools execute correctly
- Web UI loads and tool test panel works
- Can connect from Claude Desktop MCP client
