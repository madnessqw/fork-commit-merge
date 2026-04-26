# MCP Server Builder - Product Spec

## Metadata
- **slug:** mcp-server-builder
- **name:** MCP Server Builder
- **price:** $19
- **category:** Developer Tools
- **status:** spec_ready

## Description
Build Model Context Protocol (MCP) servers visually. Scaffold TypeScript MCP servers with custom tools, resources, and prompts. Generated code follows MCP SDK best practices with proper error handling.

## Problem
MCP (Model Context Protocol) is becoming the standard for AI agent extensibility, but building MCP servers requires deep protocol knowledge. Developers struggle with:
- Understanding MCP protocol architecture
- Proper tool/resource/prompt structure
- Error handling and type safety
- Server configuration (stdio vs SSE)

## Solution
Visual MCP server builder that:
1. Scaffolds server structure
2. Generates TypeScript code
3. Includes proper error handling
4. Provides testing UI
5. Exports ready-to-publish packages

## Key Features
1. **Visual Server Designer**
   - Tool definition builder (name, schema, handler)
   - Resource template editor
   - Prompt template creator
   - Server metadata config

2. **Code Generation**
   - TypeScript MCP SDK code
   - Proper Zod schemas
   - Error handling patterns
   - Transport configuration (stdio/SSE)

3. **Testing Interface**
   - Local test runner
   - Tool invocation simulator
   - Resource request tester
   - JSON-RPC message inspector

4. **Export Options**
   - Download as ZIP
   - GitHub repo structure
   - npm publish ready
   - Docker container option

5. **Template Library**
   - Weather API server
   - File system server
   - Database query server
   - REST API wrapper

## Technical Stack
- **Frontend:** Vanilla HTML + Tailwind CSS
- **Backend:** Vercel Serverless Functions
- **Code Gen:** Template-based TypeScript generation
- **Testing:** Browser-based MCP client simulation

## API Structure
```
/api/health - Health check
/api/webhook - LemonSqueezy webhook
/api/generate - Generate MCP server code
/api/validate - Validate MCP schema
/api/test-invoke - Test tool invocation
```

## UI Components
1. **Server Config Panel**
   - Name, version, description
   - Transport selection
   - Authentication options

2. **Tools Builder**
   - Tool name and description
   - Input schema editor (Zod)
   - Handler code template
   - Tool list manager

3. **Resources Editor**
   - URI template input
   - MIME type selector
   - Resource handler code

4. **Prompts Designer**
   - Prompt name and description
   - Arguments schema
   - Message template builder

5. **Code Preview**
   - Syntax highlighted TypeScript
   - File tree explorer
   - Copy/download buttons

6. **Landing Page**
   - MCP protocol explanation
   - Demo video
   - Template showcase
   - Pricing

## Differentiation
- First visual MCP server builder
- Follows official MCP SDK patterns
- Includes testing interface
- No AI required - pure code generation

## Pricing Strategy
- $19 one-time
- All templates included
- Unlimited generations
- Free updates

## Target Audience
- AI application developers
- Agent builders
- Tool integrators
- Enterprise developers adopting MCP

## SEO Keywords
mcp server generator, model context protocol builder, mcp typescript scaffold, ai agent tools, mcp sdk generator

## Context
MCP (Model Context Protocol) is Anthropic's open standard for connecting AI assistants to data sources and tools. Growing adoption across Claude, Cursor, and other AI coding tools.
