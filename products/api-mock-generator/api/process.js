// Mock API Response Generator
// Generate realistic mock data for REST and GraphQL APIs

const mockGenerators = {
  uuid: () => 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, c => {
    const r = Math.random() * 16 | 0;
    return (c === 'x' ? r : (r & 0x3 | 0x8)).toString(16);
  }),
  nanoId: (len = 21) => {
    const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_';
    return Array(len).fill(0).map(() => chars[Math.random() * chars.length | 0]).join('');
  },
  fullName: () => {
    const first = ['John', 'Jane', 'Alex', 'Sarah', 'Michael', 'Emma', 'David', 'Lisa', 'Chris', 'Anna'][Math.random() * 10 | 0];
    const last = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis', 'Wilson', 'Taylor'][Math.random() * 10 | 0];
    return `${first} ${last}`;
  },
  firstName: () => ['John', 'Jane', 'Alex', 'Sarah', 'Michael', 'Emma', 'David', 'Lisa', 'Chris', 'Anna'][Math.random() * 10 | 0],
  lastName: () => ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis', 'Wilson', 'Taylor'][Math.random() * 10 | 0],
  email: () => {
    const local = ['user', 'admin', 'contact', 'support', 'info', 'sales', 'team', 'hello'][Math.random() * 8 | 0];
    const domains = ['gmail.com', 'yahoo.com', 'outlook.com', 'example.com', 'company.com', 'test.io', 'demo.app'];
    return `${local}${Math.random() * 1000 | 0}@${domains[Math.random() * domains.length | 0]}`;
  },
  phone: () => `+1 (${Math.random() * 900 + 100 | 0}) ${Math.random() * 900 + 100 | 0}-${Math.random() * 9000 + 1000 | 0}`,
  boolean: () => Math.random() > 0.5,
  dateISO: () => new Date(Date.now() - Math.random() * 10000000000).toISOString(),
  date: () => new Date(Date.now() - Math.random() * 10000000000).toLocaleDateString('en-US'),
  timestamp: () => Math.floor(Date.now() / 1000) - Math.floor(Math.random() * 10000000),
  ip: () => `${Math.random() * 256 | 0}.${Math.random() * 256 | 0}.${Math.random() * 256 | 0}.${Math.random() * 256 | 0}`,
  url: () => `https://example.com/${Math.random().toString(36).substring(7)}`,
  domain: () => ['example.com', 'test.io', 'demo.app', 'api.dev', 'mock.net'][Math.random() * 5 | 0],
  hex: (len = 8) => Array(len).fill(0).map(() => (Math.random() * 16 | 0).toString(16)).join(''),
  base64: () => Buffer.from(Math.random().toString(36).substring(7)).toString('base64'),
  number: (min = 0, max = 100) => Math.floor(Math.random() * (max - min + 1)) + min,
  float: (min = 0, max = 100) => (Math.random() * (max - min) + min).toFixed(2),
  price: () => (Math.random() * 1000 + 10).toFixed(2),
  percentage: () => Math.floor(Math.random() * 101),
  color: () => '#' + Math.floor(Math.random() * 16777215).toString(16).padStart(6, '0'),
  avatar: () => `https://api.dicebear.com/7.x/avataaars/svg?seed=${Math.random().toString(36).substring(7)}`,
  company: () => ['Acme Corp', 'Tech Solutions', 'Global Industries', 'Digital Innovations', 'Future Systems', 'NextGen Labs'][Math.random() * 6 | 0],
  jobTitle: () => ['Developer', 'Designer', 'Manager', 'Engineer', 'Analyst', 'Director', 'Lead'][Math.random() * 7 | 0],
  address: () => `${Math.random() * 9999 + 1 | 0} ${['Main', 'Oak', 'Pine', 'Maple', 'Cedar'][Math.random() * 5 | 0]} St`,
  city: () => ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix', 'Philadelphia', 'Seattle', 'Denver'][Math.random() * 8 | 0],
  country: () => ['USA', 'UK', 'Canada', 'Germany', 'France', 'Australia', 'Japan', 'Brazil'][Math.random() * 8 | 0],
  zipCode: () => Math.floor(Math.random() * 90000) + 10000,
  username: () => ['user', 'admin', 'dev', 'test', 'demo'][Math.random() * 5 | 0] + Math.floor(Math.random() * 10000),
  password: () => Math.random().toString(36).substring(2, 10) + Math.random().toString(36).substring(2, 10).toUpperCase() + '!@#',
  gender: () => Math.random() > 0.5 ? 'male' : 'female',
  lorem: (words = 10) => {
    const wordList = ['lorem', 'ipsum', 'dolor', 'sit', 'amet', 'consectetur', 'adipiscing', 'elit', 'sed', 'do', 'eiusmod', 'tempor', 'incididunt', 'ut', 'labore', 'et', 'dolore', 'magna', 'aliqua'];
    return Array(words).fill(0).map(() => wordList[Math.random() * wordList.length | 0]).join(' ');
  }
};

function parseValue(type) {
  if (typeof type !== 'string') return type;

  // Handle random:option1,option2
  if (type.startsWith('random:')) {
    const options = type.slice(7).split(',');
    return options[Math.random() * options.length | 0];
  }

  // Handle number:min,max
  if (type.startsWith('number:')) {
    const [min, max] = type.slice(7).split(',').map(Number);
    return mockGenerators.number(min, max);
  }

  // Handle float:min,max
  if (type.startsWith('float:')) {
    const [min, max] = type.slice(6).split(',').map(Number);
    return Number(mockGenerators.float(min, max));
  }

  // Handle hex:length
  if (type.startsWith('hex:')) {
    return mockGenerators.hex(Number(type.slice(4)));
  }

  // Handle lorem:wordCount
  if (type.startsWith('lorem:')) {
    return mockGenerators.lorem(Number(type.slice(6)));
  }

  // Handle nanoId:length
  if (type.startsWith('nanoId:')) {
    return mockGenerators.nanoId(Number(type.slice(7)));
  }

  // Default generators
  if (mockGenerators[type]) return mockGenerators[type]();

  return type;
}

function generateObject(schema, depth = 0) {
  if (depth > 10) return null;

  const result = {};

  for (const [key, value] of Object.entries(schema)) {
    if (typeof value === 'object' && value !== null) {
      if (value.type === 'array' && value.item) {
        const count = value.count || Math.floor(Math.random() * 5) + 1;
        result[key] = Array(count).fill(0).map(() => generateObject(value.item, depth + 1));
      } else {
        result[key] = generateObject(value, depth + 1);
      }
    } else {
      result[key] = parseValue(value);
    }
  }

  return result;
}

export default async function handler(req, res) {
  // Enable CORS
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization');

  if (req.method === 'OPTIONS') {
    return res.status(200).end();
  }

  // Parse request body
  let body = {};
  if (req.body) {
    try {
      body = typeof req.body === 'string' ? JSON.parse(req.body) : req.body;
    } catch (e) {
      return res.status(400).json({
        success: false,
        error: 'Invalid JSON in request body',
        generated_at: new Date().toISOString()
      });
    }
  }

  const { schema, count = 1, delay = 0 } = body;

  // Simulate network delay if specified
  if (delay > 0 && delay <= 30000) {
    await new Promise(r => setTimeout(r, Math.min(delay, 30000)));
  }

  // If no schema provided, return sample
  if (!schema) {
    return res.status(200).json({
      success: true,
      message: 'API Mock Generator - Provide a schema to generate mock data',
      example: {
        users: {
          id: '550e8400-e29b-41d4-a716-446655440000',
          name: 'John Smith',
          email: 'user123@gmail.com',
          role: 'admin',
          isActive: true,
          createdAt: '2024-01-15T10:30:00.000Z'
        },
        total: 42,
        page: 1
      },
      schema_example: {
        users: {
          type: 'array',
          count: 3,
          item: {
            id: 'uuid',
            name: 'fullName',
            email: 'email',
            role: 'random:admin,editor,user',
            isActive: 'boolean',
            createdAt: 'dateISO'
          }
        },
        total: 'number:50,200',
        page: 1
      },
      available_types: Object.keys(mockGenerators),
      usage: 'POST with JSON body containing "schema" field',
      generated_at: new Date().toISOString()
    });
  }

  try {
    // Generate mock data
    let result;
    if (count > 1) {
      result = Array(Math.min(count, 100)).fill(0).map(() => generateObject(schema));
    } else {
      result = generateObject(schema);
    }

    return res.status(200).json({
      success: true,
      data: result,
      metadata: {
        generated_count: count,
        timestamp: new Date().toISOString(),
        latency_ms: delay
      }
    });

  } catch (error) {
    return res.status(500).json({
      success: false,
      error: 'Failed to generate mock data',
      message: error.message,
      generated_at: new Date().toISOString()
    });
  }
}
