module.exports = (req, res) => {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  try {
    const { left, right } = req.body;

    if (!left || !right) {
      return res.status(400).json({ error: 'Both left and right JSON required' });
    }

    const leftParsed = JSON.parse(left);
    const rightParsed = JSON.parse(right);

    const diff = generateDiff(leftParsed, rightParsed);

    res.status(200).json({
      success: true,
      diff,
      summary: {
        added: diff.filter(d => d.type === 'added').length,
        removed: diff.filter(d => d.type === 'removed').length,
        modified: diff.filter(d => d.type === 'modified').length
      }
    });
  } catch (error) {
    res.status(400).json({ error: error.message });
  }
};

function generateDiff(left, right, path = '') {
  const diff = [];

  for (const key in right) {
    const currentPath = path ? `${path}.${key}` : key;

    if (!(key in left)) {
      diff.push({ path: currentPath, type: 'added', value: right[key] });
    } else if (typeof left[key] !== typeof right[key]) {
      diff.push({
        path: currentPath,
        type: 'modified',
        oldValue: left[key],
        newValue: right[key]
      });
    } else if (typeof right[key] === 'object' && right[key] !== null) {
      if (Array.isArray(right[key])) {
        if (JSON.stringify(left[key]) !== JSON.stringify(right[key])) {
          diff.push({
            path: currentPath,
            type: 'modified',
            oldValue: left[key],
            newValue: right[key]
          });
        }
      } else {
        diff.push(...generateDiff(left[key], right[key], currentPath));
      }
    } else if (left[key] !== right[key]) {
      diff.push({
        path: currentPath,
        type: 'modified',
        oldValue: left[key],
        newValue: right[key]
      });
    }
  }

  for (const key in left) {
    const currentPath = path ? `${path}.${key}` : key;
    if (!(key in right)) {
      diff.push({ path: currentPath, type: 'removed', value: left[key] });
    }
  }

  return diff;
}
