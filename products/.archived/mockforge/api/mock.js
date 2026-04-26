// Built-in fake data generators
const fakeData = {
  users: (count = 5) => Array.from({ length: count }, (_, i) => ({
    id: i + 1,
    name: `User ${i + 1}`,
    email: `user${i + 1}@example.com`,
    avatar: `https://i.pravatar.cc/150?u=${i + 1}`,
    role: ['admin', 'user', 'moderator'][i % 3],
    createdAt: new Date(Date.now() - Math.random() * 1e10).toISOString()
  })),
  products: (count = 5) => Array.from({ length: count }, (_, i) => ({
    id: i + 1,
    name: `Product ${i + 1}`,
    price: (Math.random() * 100 + 5).toFixed(2),
    category: ['electronics', 'clothing', 'books', 'food'][i % 4],
    inStock: Math.random() > 0.3,
    rating: (Math.random() * 5).toFixed(1)
  })),
  posts: (count = 5) => Array.from({ length: count }, (_, i) => ({
    id: i + 1,
    title: `Post Title ${i + 1}`,
    body: `Lorem ipsum dolor sit amet, consectetur adipiscing elit. Post ${i + 1}.`,
    author: `Author ${i + 1}`,
    likes: Math.floor(Math.random() * 500),
    comments: Math.floor(Math.random() * 50),
    published: Math.random() > 0.2
  })),
  comments: (count = 5) => Array.from({ length: count }, (_, i) => ({
    id: i + 1,
    postId: Math.floor(Math.random() * 10) + 1,
    author: `Commenter ${i + 1}`,
    text: `This is comment number ${i + 1}. Great post!`,
    createdAt: new Date(Date.now() - Math.random() * 1e10).toISOString()
  })),
  orders: (count = 5) => Array.from({ length: count }, (_, i) => ({
    id: `ORD-${String(i + 1).padStart(4, '0')}`,
    customer: `Customer ${i + 1}`,
    total: parseFloat((Math.random() * 200 + 10).toFixed(2)),
    status: ['pending', 'shipped', 'delivered', 'cancelled'][i % 4],
    items: Math.floor(Math.random() * 5) + 1,
    createdAt: new Date(Date.now() - Math.random() * 1e10).toISOString()
  })),
  tasks: (count = 5) => Array.from({ length: count }, (_, i) => ({
    id: i + 1,
    title: `Task ${i + 1}`,
    status: ['todo', 'in-progress', 'done', 'blocked'][i % 4],
    priority: ['low', 'medium', 'high', 'critical'][i % 4],
    assignee: `Assignee ${i + 1}`,
    dueDate: new Date(Date.now() + Math.random() * 7 * 86400000).toISOString().split('T')[0]
  }))
};

function getFakeData(endpoint) {
  const key = Object.keys(fakeData).find(k => endpoint.toLowerCase().includes(k));
  if (key) return fakeData[key]();
  return { message: `Mock data for ${endpoint}`, timestamp: new Date().toISOString() };
}

module.exports = async (req, res) => {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization');
  res.setHeader('X-MockForge', 'true');

  if (req.method === 'OPTIONS') {
    return res.status(200).json({ ok: true });
  }

  // Extract the endpoint path from the URL
  const url = req.url || '';
  const endpoint = url.replace(/^\/api\/mock\/?/, '') || 'default';

  // Simulate network delay
  const delay = parseInt(req.query?.delay) || Math.floor(Math.random() * 200) + 50;
  await new Promise(resolve => setTimeout(resolve, delay));

  // Return fake data based on endpoint
  const data = getFakeData(endpoint);
  const statusCode = parseInt(req.query?.status) || 200;

  return res.status(statusCode).json({
    _mock: true,
    endpoint: `/${endpoint}`,
    method: req.method,
    delay: `${delay}ms`,
    data
  });
};
