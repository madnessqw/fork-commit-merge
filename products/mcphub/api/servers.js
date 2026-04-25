export default function handler(req, res) {
  const servers = [
    { id: 'filesystem-mcp', name: 'Filesystem MCP', description: 'Read, write, and list files on your system', installs: 15234, rating: 4.8, tools: 5 },
    { id: 'github-mcp', name: 'GitHub MCP', description: 'Manage repositories, issues, and pull requests', installs: 12450, rating: 4.6, tools: 12 },
    { id: 'postgres-mcp', name: 'PostgreSQL MCP', description: 'Query and manage PostgreSQL databases', installs: 8920, rating: 4.5, tools: 6 },
    { id: 'slack-mcp', name: 'Slack MCP', description: 'Send messages and manage Slack channels', installs: 7650, rating: 4.3, tools: 8 },
    { id: 'brave-search-mcp', name: 'Brave Search MCP', description: 'Web search using Brave Search API', installs: 6890, rating: 4.4, tools: 2 },
    { id: 'memory-mcp', name: 'Memory MCP', description: 'Persistent key-value storage for AI agents', installs: 5430, rating: 4.7, tools: 3 },
    { id: 'fetch-mcp', name: 'Fetch MCP', description: 'HTTP requests and web content fetching', installs: 4980, rating: 4.2, tools: 2 },
    { id: 'sentry-mcp', name: 'Sentry MCP', description: 'Monitor errors and performance issues', installs: 3210, rating: 4.1, tools: 5 },
  ];
  res.status(200).json({ servers, total: servers.length });
}
