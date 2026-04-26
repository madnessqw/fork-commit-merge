export default async function handler(req, res) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  const { serverName, language, features } = req.body;
  
  if (!serverName || !language) {
    return res.status(400).json({ error: 'serverName and language are required' });
  }

  // Generate boilerplate code based on language
  let code = '';
  let packageJson = {};
  
  if (language === 'typescript') {
    code = generateTypeScriptServer(serverName, features);
    packageJson = {
      name: serverName,
      version: '1.0.0',
      type: 'module',
      scripts: { build: 'tsc', start: 'node dist/index.js' },
      dependencies: {
        '@modelcontextprotocol/sdk': '^0.5.0'
      },
      devDependencies: {
        '@types/node': '^20.0.0',
        typescript: '^5.0.0'
      }
    };
  } else if (language === 'python') {
    code = generatePythonServer(serverName, features);
    packageJson = {
      name: serverName,
      version: '1.0.0',
      dependencies: {
        'mcp': '^1.0.0'
      }
    };
  }

  res.status(200).json({
    success: true,
    serverName,
    language,
    code,
    packageJson,
    readme: generateReadme(serverName, language)
  });
}

function generateTypeScriptServer(name, features) {
  const hasTools = features?.includes('tools');
  const hasResources = features?.includes('resources');
  
  return `import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import { CallToolRequestSchema, ListToolsRequestSchema } from '@modelcontextprotocol/sdk/types.js';

const server = new Server(
  { name: '${name}', version: '1.0.0' },
  { capabilities: { ${hasTools ? 'tools: {}' : ''}${hasResources && hasTools ? ', ' : ''}${hasResources ? 'resources: {}' : ''} } }
);

${hasTools ? `
server.setRequestHandler(ListToolsRequestSchema, async () => ({
  tools: [{
    name: 'example_tool',
    description: 'An example tool',
    inputSchema: { type: 'object', properties: {} }
  }]
}));

server.setRequestHandler(CallToolRequestSchema, async (request) => {
  if (request.params.name === 'example_tool') {
    return { content: [{ type: 'text', text: 'Hello from ${name}!' }] };
  }
  throw new Error('Tool not found');
});` : ''}

async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error('${name} server running on stdio');
}

main().catch(console.error);`;
}

function generatePythonServer(name, features) {
  return `import asyncio
from mcp.server import Server
from mcp.types import TextContent

app = Server('${name}')

@app.tool()
async def example_tool():
    """An example tool"""
    return TextContent(text='Hello from ${name}!')

async def main():
    from mcp.server.stdio import stdio_server
    async with stdio_server() as streams:
        await app.run(streams[0], streams[1])

if __name__ == '__main__':
    asyncio.run(main())`;
}

function generateReadme(name, language) {
  return `# ${name}

A Model Context Protocol server built with ${language === 'typescript' ? 'TypeScript' : 'Python'}.

## Setup

${language === 'typescript' ? `\`\`\`bash\nnpm install\nnpm run build\n\`\`\`` : `\`\`\`bash\npip install -r requirements.txt\n\`\`\``}

## Running

${language === 'typescript' ? `\`\`\`bash\nnpm start\n\`\`\`` : `\`\`\`bash\npython server.py\n\`\`\``}`;
}
