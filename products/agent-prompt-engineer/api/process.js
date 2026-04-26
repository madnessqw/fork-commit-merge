module.exports = (req, res) => {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  const { prompt, action } = req.body;

  if (!prompt) {
    return res.status(400).json({ error: 'Prompt is required' });
  }

  const tokenCount = Math.ceil(prompt.length / 4);

  let clarity = 50;
  if (prompt.length > 50) clarity += 20;
  if (prompt.includes('?')) clarity += 10;
  if (prompt.includes('step') || prompt.includes('list')) clarity += 10;
  if (prompt.includes('as a') || prompt.includes('act like')) clarity += 10;
  clarity = Math.min(clarity, 100);

  const suggestions = [];
  if (prompt.length < 30) suggestions.push('Add more context to your prompt');
  if (!prompt.includes('?') && !prompt.includes('.')) suggestions.push('Use clear sentences or questions');
  if (!prompt.includes('as a') && !prompt.includes('act like')) suggestions.push('Consider adding a role/persona');
  if (!prompt.includes('step') && !prompt.includes('format')) suggestions.push('Specify desired output format');

  let result = {
    tokenCount,
    clarity,
    suggestions,
    original: prompt
  };

  if (action === 'optimize') {
    result.optimized = `Act as an expert in this domain. ${prompt} Please provide a detailed, step-by-step response with clear formatting.`;
    result.optimizedTokens = Math.ceil(result.optimized.length / 4);
  }

  res.status(200).json(result);
};
