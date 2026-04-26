# SPEC.md — Lyra: MCP Client Dashboard

## 1. Concept & Vision

**Lyra** is a visual command center for MCP (Model Context Protocol) agent orchestration. It connects to MCP clients, displays running agents in real-time, lets users trigger tool calls, monitor token usage, and manage agent clusters — all from a sleek dashboard. Inspired by the Reddit post "I built an MCP client that runs 2,700+ agents with one click."

**Tagline:** "Your MCP agents, visualized. Control 2,700+ agents from one dashboard."

**Emotional pitch:** Finally, a way to *see* what your AI agents are doing. Not just logs and terminal output — a real-time mission control for your agent swarm.

---

## 2. Design Language

- **Aesthetic:** Dark command-center with neon accents. Think Bloomberg Terminal meets Warpgate.
- **Colors:**
  - Background: `#0a0a0f` (deep space black)
  - Surface: `#14141f` (dark card)
  - Border: `#2a2a3a` (subtle edges)
  - Primary: `#7c3aed` (violet — agent activity)
  - Accent: `#22d3ee` (cyan — live data)
  - Success: `#10b981` (green — healthy)
  - Warning: `#f59e0b` (amber — throttling)
  - Danger: `#ef4444` (red — errors)
  - Text: `#e2e8f0` (light gray)
  - Muted: `#64748b` (dim text)

- **Typography:**
  - Headings: `JetBrains Mono` (monospace authority)
  - Body: `Inter` fallback to system-ui
  - Data: `JetBrains Mono` for all numbers/IDs

- **Motion:**
  - Agent cards pulse gently (opacity 0.8→1.0, 2s cycle) when active
  - Tool call responses slide in from right (300ms ease-out)
  - Status changes cross-fade (200ms)
  - No jarring animations — this is a monitoring tool

---

## 3. Layout & Structure

```
┌────────────────────────────────────────────────────────────────┐
│  Lyra                                    [Connect] [Settings] │
├──────────────┬─────────────────────────────────────────────────┤
│              │                                                  │
│  AGENT       │  MAIN PANEL                                       │
│  CLUSTER     │  ┌─────────────────────────────────────────┐    │
│              │  │  Agent Detail / Tool Runner / Logs        │    │
│  [list of    │  │                                           │    │
│   agents]     │  │  Real-time output stream                  │    │
│              │  │                                           │    │
│              │  │                                           │    │
│              │  └─────────────────────────────────────────┘    │
│              │                                                  │
│              │  ┌─ TOKEN USAGE ─┐  ┌─ QUICK ACTIONS ─┐         │
│              │  │ 12,450 tokens │  │ [Run Tool]      │         │
│              │  └───────────────┘  └────────────────┘         │
└──────────────┴─────────────────────────────────────────────────┘
```

- **Sidebar** (240px): Scrollable agent list with status indicators
- **Main Panel** (flex): Tabbed — Details | Tools | Logs
- **Bottom Bar** (48px): Aggregate stats — total agents, active, token count

---

## 4. Features & Interactions

### Core Features

1. **MCP Connection Manager**
   - Add connection via URL + auth token
   - Show connected/disconnected status per agent
   - Auto-reconnect on connection drop

2. **Agent Cluster View**
   - Grid of agent cards showing: name, status (idle/running/error), last activity
   - Click to select → populate main panel
   - Multi-select for batch operations

3. **Real-Time Agent Detail**
   - Agent metadata (name, ID, model, MCP server)
   - Live activity feed (last 50 tool calls)
   - Token usage counter (session + total)
   - Status: idle | running | error | throttled

4. **Tool Runner**
   - Dropdown of available MCP tools for selected agent
   - JSON input form for tool parameters
   - Execute button → shows response inline
   - History of tool calls with timestamps

5. **Log Stream**
   - Aggregated log view across all agents
   - Filter by level: debug | info | warn | error
   - Filter by agent
   - Auto-scroll with pause on manual scroll

### Interactions

| Element | Hover | Click | State |
|---------|-------|-------|-------|
| Agent Card | Brighten border | Select agent | Selected = violet border |
| Connect Button | Glow | Open connection modal | Connected = green dot |
| Tool Execute | Brighten | Execute tool | Loading = spinner, result = slide-in |
| Log Entry | Highlight row | Expand full log | Expanded = full JSON visible |

### Edge Cases

- **No agents connected:** Show empty state with "Add your first MCP connection" CTA
- **Agent disconnects mid-stream:** Mark agent as `disconnected`, show reconnect button
- **Tool call fails:** Red border on tool card, error message inline
- **Token limit approaching:** Amber warning bar at top ("Approaching token limit: 80%")

---

## 5. Component Inventory

### AgentCard
- States: idle (dim), active (pulse), error (red border), selected (violet border)
- Shows: avatar circle (initials), name, status badge, last active timestamp

### ConnectionModal
- Fields: MCP endpoint URL, auth token
- Buttons: Connect (primary), Cancel (ghost)

### ToolRunner
- Tool selector dropdown
- JSON textarea (with basic syntax highlight)
- Execute button (loading state while pending)
- Response panel (success=green border, error=red border)

### LogStream
- Virtualized list (renders only visible rows)
- Level badges: DEBUG (gray), INFO (blue), WARN (amber), ERROR (red)
- Timestamp + agent name + message

### TokenCounter
- Circular progress ring
- Large number in center
- Color shifts: green (<60%) → amber (60-85%) → red (>85%)

---

## 6. Technical Approach

- **Stack:** Single HTML file — vanilla JS, no build step
- **MCP Protocol:** Uses `@modelcontextprotocol/sdk` JS client to connect
- **Real-time:** Server-Sent Events (SSE) for live agent updates
- **Storage:** localStorage for connection configs and session state
- **Data model:**
  ```js
  Agent: { id, name, status, model, mcpServer, lastActivity, tokenCount }
  ToolCall: { id, agentId, toolName, params, response, timestamp, duration }
  Connection: { id, url, token, status }
  ```
- **API:** REST endpoints to MCP server for tool listing/execution
- **Error handling:** All async wrapped in try/catch, user-facing error messages

---

## 7. Success Metrics

- [ ] Can connect to an MCP server and list agents
- [ ] Displays agent list with real-time status
- [ ] Can execute a tool and see the response
- [ ] Token usage displays and updates
- [ ] Log stream shows live activity
- [ ] Zero console errors in normal operation
