const scenarios = new Map();

module.exports = async (req, res) => {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization');

  if (req.method === 'OPTIONS') {
    return res.status(200).json({ ok: true });
  }

  if (req.method === 'GET') {
    const all = Array.from(scenarios.entries()).map(([key, val]) => ({ id: key, ...val }));
    return res.status(200).json({ scenarios: all, count: all.length });
  }

  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  const { id, name, endpoint, method, statusCode, response, delay, conditions } = req.body;

  if (!name || !endpoint) {
    return res.status(400).json({ error: 'name and endpoint are required' });
  }

  const scenarioId = id || `scn_${Date.now()}_${Math.random().toString(36).slice(2, 8)}`;
  const scenario = {
    name,
    endpoint,
    method: method || 'GET',
    statusCode: statusCode || 200,
    response: response || { message: 'Mock response' },
    delay: delay || 0,
    conditions: conditions || [],
    createdAt: new Date().toISOString(),
    updatedAt: new Date().toISOString()
  };

  scenarios.set(scenarioId, scenario);

  return res.status(201).json({
    ok: true,
    scenario: { id: scenarioId, ...scenario }
  });
};
