module.exports = async (req, res) => {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization');

  if (req.method === 'OPTIONS') {
    return res.status(200).json({ ok: true });
  }

  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  const { prompt, endpoint, method = 'GET', count = 5 } = req.body;

  if (!prompt) {
    return res.status(400).json({ error: 'prompt is required' });
  }

  // AI mock generation based on prompt analysis (no external API needed)
  const promptLower = prompt.toLowerCase();

  // Detect entity type from prompt
  let entityType = 'items';
  const entityPatterns = {
    users: ['user', 'customer', 'person', 'account', 'member', 'admin'],
    products: ['product', 'item', 'good', 'merchandise', 'sku'],
    posts: ['post', 'article', 'blog', 'content', 'entry'],
    comments: ['comment', 'review', 'feedback', 'response'],
    orders: ['order', 'purchase', 'transaction', 'invoice'],
    tasks: ['task', 'todo', 'job', 'assignment', 'ticket'],
    events: ['event', 'meeting', 'appointment', 'schedule'],
    messages: ['message', 'chat', 'conversation', 'dm']
  };

  for (const [type, keywords] of Object.entries(entityPatterns)) {
    if (keywords.some(k => promptLower.includes(k))) {
      entityType = type;
      break;
    }
  }

  // Generate schema based on entity type
  const schemas = {
    users: {
      fields: ['id', 'name', 'email', 'role', 'avatar', 'createdAt'],
      generate: (i) => ({
        id: i + 1,
        name: `User ${i + 1}`,
        email: `user${i + 1}@example.com`,
        role: ['admin', 'user', 'editor'][i % 3],
        avatar: `https://i.pravatar.cc/150?u=${i + 1}`,
        createdAt: new Date(Date.now() - Math.random() * 1e10).toISOString()
      })
    },
    products: {
      fields: ['id', 'name', 'price', 'category', 'inStock', 'rating'],
      generate: (i) => ({
        id: i + 1,
        name: `Product ${i + 1}`,
        price: parseFloat((Math.random() * 100 + 9.99).toFixed(2)),
        category: ['Electronics', 'Clothing', 'Books', 'Home'][i % 4],
        inStock: Math.random() > 0.3,
        rating: parseFloat((Math.random() * 3 + 2).toFixed(1))
      })
    },
    posts: {
      fields: ['id', 'title', 'body', 'author', 'likes', 'published'],
      generate: (i) => ({
        id: i + 1,
        title: `${entityType.charAt(0).toUpperCase() + entityType.slice(1)} ${i + 1}`,
        body: `Generated content for ${entityType} #${i + 1}. ${prompt}`,
        author: `Author ${i + 1}`,
        likes: Math.floor(Math.random() * 500),
        published: Math.random() > 0.3
      })
    },
    orders: {
      fields: ['id', 'customer', 'total', 'status', 'items', 'createdAt'],
      generate: (i) => ({
        id: `ORD-${String(i + 1).padStart(4, '0')}`,
        customer: `Customer ${i + 1}`,
        total: parseFloat((Math.random() * 200 + 10).toFixed(2)),
        status: ['pending', 'shipped', 'delivered', 'cancelled'][i % 4],
        items: Math.floor(Math.random() * 5) + 1,
        createdAt: new Date(Date.now() - Math.random() * 1e10).toISOString()
      })
    },
    tasks: {
      fields: ['id', 'title', 'status', 'priority', 'assignee', 'dueDate'],
      generate: (i) => ({
        id: i + 1,
        title: `Task ${i + 1}`,
        status: ['todo', 'in-progress', 'done', 'blocked'][i % 4],
        priority: ['low', 'medium', 'high', 'critical'][i % 4],
        assignee: `Assignee ${i + 1}`,
        dueDate: new Date(Date.now() + Math.random() * 7 * 86400000).toISOString().split('T')[0]
      })
    }
  };

  const schema = schemas[entityType] || schemas.items || {
    fields: ['id', 'name', 'value'],
    generate: (i) => ({
      id: i + 1,
      name: `${entityType.charAt(0).toUpperCase() + entityType.slice(1)} ${i + 1}`,
      value: `Generated value ${i + 1}`
    })
  };

  const data = Array.from({ length: count }, (_, i) => schema.generate(i));

  // Generate scenario configuration
  const scenario = {
    id: `scn_${Date.now()}`,
    endpoint: endpoint || `/api/${entityType}`,
    method: method.toUpperCase(),
    statusCode: 200,
    contentType: 'application/json',
    schema: schema.fields,
    entityType,
    prompt,
    sampleResponse: data[0],
    generatedAt: new Date().toISOString()
  };

  return res.status(200).json({
    ok: true,
    scenario,
    data,
    count: data.length,
    metadata: {
      entityType,
      detectedFrom: prompt,
      fields: schema.fields,
      generatedAt: new Date().toISOString()
    }
  });
};
