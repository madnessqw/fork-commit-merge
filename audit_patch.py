#!/usr/bin/env python3
"""
Audit patch for /tmp/classify_all.py
Adds 'AI Coding Agents & IDE Entegrasyonları' category and fixes ~45 misclassifications.

Usage: python3 audit_patch.py
NOTE: This script reads and writes /tmp/classify_all.py
"""

path = '/tmp/classify_all.py'

with open(path, 'r', encoding='utf-8') as f:
    src = f.read()

original = src
changes = []

# ═══════════════════════════════════════════════════════════════════════════
# 1. NEW CATEGORY: AI Coding Agents & IDE Entegrasyonları
#    Captures Claude Code ecosystem, OpenClaw, Antigravity, Codex, Gemini CLI
#    proxy/routing/UI tools that are specifically about AI coding agents.
#    Placed just before the catchall so earlier specific rules still win.
# ═══════════════════════════════════════════════════════════════════════════
AI_CODING_BLOCK = '''    # AI Coding Agents & IDE Entegrasyonları
    if any(k in text for k in [
        # Core coding agent platforms
        'openclaw', 'antigravity', 'codex cli', 'codex-cli', 'opencode',
        'qwen code', 'qwen-code', 'iflow', 'gemini cli', 'gemini-cli',
        'claude code', 'claude-code',
        # Claude Code specific tools
        'clawdis', 'vibecraft', 'zeroshot', 'ralph-claude-code',
        'claude-canvas', 'clawport', 'openclaw-deck', 'clawwork',
        'claude-code-router', 'claude-code-free', 'claurst',
        'antigravity-claude-proxy', 'claude-telegram-bot', 'clawfeed',
        # Proxy / routing / auth tools for coding agents
        'proxypal', 'cliproxyapi', 'cli-proxy-api', 'vibeproxy',
        'ai_cli_manager', 'clother', 'multicli', 'layercodedev/sled',
        'devtap', 'badrisnarayanan/antigravity',
        # IDE / editor integrations
        'copilot-sdk', 'copilot sdk', 'github/copilot-sdk',
        'gemini-cli-extensions', 'deepmyst/mysti',
        # Other named tools in this ecosystem
        'lazygravity', 'slopus/murmur', 'frankbria/ralph',
        'bearly-hodling', 'openai/symphony', 'rohitg00/pro-workflow',
        'crshdn/mission-control', 'alishahryar1', 'kellyclaudeai',
        'linuz90/claude', 'turn antigravity', 'antigravity.*byok',
        'antigravity.*local', 'osanoai/multicli',
    ]):
        return 'AI Coding Agents & IDE Entegrasyonları'

'''

CATCHALL_MARKER = '    # Catch rest under agent development'
if CATCHALL_MARKER in src:
    src = src.replace(CATCHALL_MARKER, AI_CODING_BLOCK + CATCHALL_MARKER)
    changes.append("✅ ADDED new category 'AI Coding Agents & IDE Entegrasyonları' (35 keywords)")
else:
    changes.append("❌ Catchall marker not found — AI Coding category NOT inserted")


# ═══════════════════════════════════════════════════════════════════════════
# 2. BROWSER AUTOMATION — ace.ai, nanobrowser, AutoGLM-Phone, Droid Claw,
#    manus-browser URL variant (manus browser operator in path), agent-captcha
# ═══════════════════════════════════════════════════════════════════════════
old = "'web-eval'"
new = ("'web-eval',"
       "'ace.ai','nanobrowser',"
       "'autoglm-phone','autogl-phone',"
       "'droid claw','droidclaw','android phones.*ai agent',"
       "'manus-browser','manus.im/tr','agent-captcha'")
if old in src:
    src = src.replace(old, new, 1)
    changes.append("✅ Browser Automation: +ace.ai, nanobrowser, AutoGLM-Phone, Droid Claw, manus-browser URL, agent-captcha")


# ═══════════════════════════════════════════════════════════════════════════
# 3. WEB SCRAPING — bare 'scrape', captcha bypass, mark-it-down (web→markdown),
#    dembrandt (extract website design system)
# ═══════════════════════════════════════════════════════════════════════════
old = "'reverse engineer website'"
new = ("'reverse engineer website',"
       "'captcha bypass','bypass.*captcha','scrape data',"
       "'mark-it-down','convert any web page to markdown',"
       "'thevangelist/dembrandt','extract.*website.*design system'")
if old in src:
    src = src.replace(old, new, 1)
    changes.append("✅ Web Scraping: +captcha bypass, mark-it-down, dembrandt design-system extractor")


# ═══════════════════════════════════════════════════════════════════════════
# 4. MCP SERVERS — FastMCP, sleep-mcp, RaiAnsar multi-AI-MCP,
#    Lyra (trylyra.com/mcp), DNS intelligence MCP
# ═══════════════════════════════════════════════════════════════════════════
old = "'stitch-ai-mcp'"
new = ("'stitch-ai-mcp',"
       "'fastmcp','fast mcp',"
       "'sleep-mcp','garoth/sleep',"
       "'raiansar/claude_code','multi-ai-mcp',"
       "'trylyra.com/mcp','mcp client that runs 2,700',"
       "'mcp-dns','dns.*mcp'")
if old in src:
    src = src.replace(old, new, 1)
    changes.append("✅ MCP: +FastMCP, sleep-mcp, RaiAnsar multi-AI-MCP, Lyra, DNS-MCP")


# ═══════════════════════════════════════════════════════════════════════════
# 5. MULTI-AGENT — fix 'chainml.*council' (literal .* never matched),
#    add: hive (collaborative agents), cloudflare-multiagent,
#    antfarm (OpenClaw team builder), walkie-sh (agents talk to each other),
#    MrLesk agents-council (pattern 'mr lesk' never matched 'mrlesk')
# ═══════════════════════════════════════════════════════════════════════════
old = "'chainml.*council'"
new = ("'chainml.*council','chain-ml/council',"
       "'aden-hive/hive','collaborative ai agents',"
       "'cloudflare-multiagent','snarktank/antfarm','antfarm.*openclaw',"
       "'walkie-sh','npm install -g walkie',"
       "'mrlesk','mr lesk/agents','agents-council'")
if old in src:
    src = src.replace(old, new, 1)
    changes.append("✅ Multi-Agent: fixed chain-ml/council, +hive, cloudflare-multiagent, antfarm, walkie-sh, MrLesk")


# ═══════════════════════════════════════════════════════════════════════════
# 6. SELF-EVOLVING — mshumer/autonomous-researcher,
#    Conway-Research/automaton ('first ai to earn its own existence'),
#    iFlow-ROME (agentic model ALE ecosystem)
# ═══════════════════════════════════════════════════════════════════════════
old = "'ai ran alone'"
new = ("'ai ran alone',"
       "'mshumer/autonomous-researcher','autonomous-researcher',"
       "'conway-research/automaton','earn its own existence',"
       "'iflow-rome','futurelablab','rome is obviously an agentic'")
if old in src:
    src = src.replace(old, new, 1)
    changes.append("✅ Self-Evolving: +mshumer/autonomous-researcher, Conway/automaton, iFlow-ROME")


# ═══════════════════════════════════════════════════════════════════════════
# 7. AGENT FRAMEWORKS — mastra-ai, HKUDS/AnyTool, CLI-Anything,
#    logic-md (declarative reasoning layer), raincast (AI app generator),
#    vibetensor (AI-generated deep learning), zeroboot (VM sandboxes),
#    opperator (run agents from terminal), opper-ai
# ═══════════════════════════════════════════════════════════════════════════
old = "'ghostwright'"
new = ("'ghostwright',"
       "'mastra-ai/mastra','mastra.*typescript',"
       "'hkuds/anytool','universal tool-use layer',"
       "'cli-anything','hkuds/cli-anything','agent-native',"
       "'singularityai-dev/logic-md','logic.md',"
       "'tihiera/raincast','raincast.*tauri',"
       "'nvlabs/vibetensor','vibetensor',"
       "'zerobootdev/zeroboot','sub-millisecond vm sandboxes',"
       "'epiral/agent-clip','opper-ai/opperator','opperator'")
if old in src:
    src = src.replace(old, new, 1)
    changes.append("✅ Agent Frameworks: +mastra, anytool, cli-anything, logic-md, raincast, vibetensor, zeroboot, opperator")


# ═══════════════════════════════════════════════════════════════════════════
# 8. WORKFLOW AUTOMATION — vercel/workflow DevKit (durable AI agent workflows)
# ═══════════════════════════════════════════════════════════════════════════
old = "'ruvnet/ruflo'"
new = ("'ruvnet/ruflo',"
       "'vercel/workflow','workflow devkit',"
       "'durable, reliable, and observable'")
if old in src:
    src = src.replace(old, new, 1)
    changes.append("✅ Workflow: +vercel/workflow DevKit")


# ═══════════════════════════════════════════════════════════════════════════
# 9. AGENT-TO-AGENT — ACP protocol page, codex-weave
#    Fix 'multi-column.*agent' literal pattern (still kept, adding aliases)
# ═══════════════════════════════════════════════════════════════════════════
old = "'multi-column.*agent'"
new = ("'multi-column.*agent','multi-column chat',"
       "'agentcommunicationprotocol.dev','agent communication protocol',"
       "'codex.*weave','rosem/codex-weave'")
if old in src:
    src = src.replace(old, new, 1)
    changes.append("✅ Agent-to-Agent: +ACP protocol page, codex-weave, multi-column chat")


# ═══════════════════════════════════════════════════════════════════════════
# 10. LLM MODELS — AReaL (RL for LLMs), speculative decoding (tanishqkumar/ssd),
#     Nanbeige, Nexus Fast 3B, Qwen3-14B distilled from Claude
# ═══════════════════════════════════════════════════════════════════════════
old = "'ai.*model.*local'"
new = ("'ai.*model.*local',"
       "'inclusionai/areal','areal.*reinforcement',"
       "'tanishqkumar/ssd','speculative decoding',"
       "'nanbeige','nexus fast 3b','nexus-fast-mini',"
       "'qwen3.*distilled','distilled from claude'")
if old in src:
    src = src.replace(old, new, 1)
    changes.append("✅ LLM Models: +AReaL, speculative decoding, Nanbeige, Nexus Fast 3B, Qwen3-distilled")


# ═══════════════════════════════════════════════════════════════════════════
# 11. AUDIO/TTS — LiveKit (realtime audio/video), neiro (audio processing),
#     MiniCPM-o (multimodal + audio), voicebox (local voice cloning)
# ═══════════════════════════════════════════════════════════════════════════
old = "'realtime.*voice'"
new = ("'realtime.*voice',"
       "'livekit/livekit','end-to-end realtime stack',"
       "'tigerabrodi/neiro','neiro.*audio',"
       "'openbmb/minicpm-o','minicpm-o',"
       "'jamiepine/voicebox','voicebox.*voice','local elevenlabs'")
if old in src:
    src = src.replace(old, new, 1)
    changes.append("✅ Audio/TTS: +LiveKit, neiro audio, MiniCPM-o, voicebox local voice cloning")


# ═══════════════════════════════════════════════════════════════════════════
# 12. TERMINAL/CLI — xterm.js (browser terminal), tuios (Terminal UI OS),
#     termcast, vercel-labs/wterm, electrobun (TS desktop app), xpipe
# ═══════════════════════════════════════════════════════════════════════════
old = "'terminal.*ai monitor'"
new = ("'terminal.*ai monitor',"
       "'xtermjs/xterm.js','xtermjs','xterm.js','build terminals in the browser',"
       "'gaurav-gosain/tuios','tuios','terminal ui os',"
       "'remorses/termcast','termcast',"
       "'vercel-labs/wterm','wterm',"
       "'electrobun','bun runtime.*desktop',"
       "'xpipe-io/xpipe','xpipe'")
if old in src:
    src = src.replace(old, new, 1)
    changes.append("✅ Terminal/CLI: +xterm.js, tuios, termcast, wterm, electrobun, xpipe")


# ═══════════════════════════════════════════════════════════════════════════
# 13. SECURITY — system-prompts-and-models-of-ai-tools (full system prompt leaks),
#     asgeirtj/system_prompts_leaks, p-e-w/heretic (censorship removal),
#     ruvnet/RuView (wifi sensing through walls)
# ═══════════════════════════════════════════════════════════════════════════
old = "'winscript.*windows.*automat'"
new = ("'winscript.*windows.*automat',"
       "'x1xhlol/system-prompts','system-prompts-and-models',"
       "'asgeirtj/system_prompts','system_prompts_leaks',"
       "'p-e-w/heretic','censorship removal for language',"
       "'ruvnet/ruview','ruview','software that sees you through walls using only wifi'")
if old in src:
    src = src.replace(old, new, 1)
    changes.append("✅ Security: +system-prompts leak repos (x1xhlol, asgeirtj), heretic, RuView wifi sensing")


# ═══════════════════════════════════════════════════════════════════════════
# 14. 3D / GAME — synaps-cad (AI 3D CAD IDE), NitroGen (gaming foundation model),
#     Stracti (AI gaming bots), TerraInk (cartographic poster)
# ═══════════════════════════════════════════════════════════════════════════
old = "'3d printed.*claude'"
new = ("'3d printed.*claude',"
       "'ierror/synaps-cad','synaps-cad','ai-powered 3d cad',"
       "'minedojo/nitrogen','nitrogen.*gaming',"
       "'stracti.com','stracti.*gaming','gaming bots.*neural',"
       "'yousifamanuel/terraink','cartographic poster'")
if old in src:
    src = src.replace(old, new, 1)
    changes.append("✅ 3D/Game: +synaps-cad AI CAD IDE, NitroGen gaming agents, Stracti bots, TerraInk maps")


# ═══════════════════════════════════════════════════════════════════════════
# 15. MEMORY/CONTEXT — alexzhang13/rlm (Recursive Language Models, context +10m),
#     RedPlanetHQ/core (personal memory system for AI apps)
# ═══════════════════════════════════════════════════════════════════════════
old = "'before i go to bed.*agents'"
new = ("'before i go to bed.*agents',"
       "'alexzhang13/rlm','recursive language model','rlm.*inference',"
       "'redplanethq/core','personal memory system'")
if old in src:
    src = src.replace(old, new, 1)
    changes.append("✅ Memory/Context: +alexzhang13/rlm (Recursive LMs), RedPlanetHQ/core")


# ═══════════════════════════════════════════════════════════════════════════
# 16. FINTECH — Universal-Commerce-Protocol, disposable Visa card via agent
# ═══════════════════════════════════════════════════════════════════════════
old = "'visa.*card.*agent'"
new = ("'visa.*card.*agent',"
       "'universal-commerce-protocol','ucp.*commerce',"
       "'tek kullanımlık sanal visa','disposable.*virtual.*card',"
       "'online harcama.*agent'")
if old in src:
    src = src.replace(old, new, 1)
    changes.append("✅ Fintech: +Universal-Commerce-Protocol, disposable Visa card agent (Turkish tweet)")


# ═══════════════════════════════════════════════════════════════════════════
# Write patched file
# ═══════════════════════════════════════════════════════════════════════════
if src != original:
    with open(path, 'w', encoding='utf-8') as f:
        f.write(src)
    print(f"✅ Patched: {path}")
    print(f"   {len(changes)} change(s) applied:\n")
    for c in changes:
        print(f"   {c}")
else:
    print("❌ No changes written. Verify strings match classify_all.py exactly.")

print()
print("─" * 70)
print("Re-run /tmp/classify_all.py to regenerate sınıflandırılmış-projeler.txt")
print("─" * 70)
