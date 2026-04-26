module.exports = async function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type, X-License-Key');

  if (req.method === 'OPTIONS') {
    return res.status(200).end();
  }

  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  const { sql, targetDb, action } = req.body;
  const licenseKey = req.headers['x-license-key'];

  if (!licenseKey && action !== 'preview') {
    return res.status(401).json({
      error: 'License required',
      message: 'Please provide a valid license key'
    });
  }

  try {
    let result;

    switch (action) {
      case 'convert':
        result = convertSQL(sql, targetDb);
        break;
      case 'schema':
        result = suggestSchema(sql, targetDb);
        break;
      case 'preview':
        result = { 
          preview: true, 
          message: 'Preview mode - limited to 3 conversions per day',
          sample: convertSQL('SELECT * FROM users WHERE id = 1', 'mongodb')
        };
        break;
      default:
        return res.status(400).json({
          error: 'Invalid action',
          validActions: ['convert', 'schema', 'preview']
        });
    }

    return res.status(200).json({
      success: true,
      ...result
    });
  } catch (error) {
    console.error('[SQL Converter] Error:', error);
    return res.status(500).json({
      error: 'Conversion failed',
      message: error.message
    });
  }
};

function convertSQL(sql, targetDb) {
  const conversions = {
    mongodb: convertToMongoDB(sql),
    dynamodb: convertToDynamoDB(sql),
    firestore: convertToFirestore(sql)
  };

  return {
    original: sql,
    target: targetDb,
    converted: conversions[targetDb] || conversions.mongodb,
    explanation: getExplanation(targetDb)
  };
}

function convertToMongoDB(sql) {
  // Basic SQL to MongoDB conversion patterns
  if (sql.match(/SELECT \* FROM (\w+) WHERE (\w+) = (\d+|'[^']+')/i)) {
    const match = sql.match(/SELECT \* FROM (\w+) WHERE (\w+) = (\d+|'[^']+')/i);
    const [, collection, field, value] = match;
    const cleanValue = value.startsWith("'") ? value.slice(1, -1) : parseInt(value);
    return `db.${collection}.find({ ${field}: ${JSON.stringify(cleanValue)} })`;
  }
  
  if (sql.match(/SELECT \* FROM (\w+)/i)) {
    const match = sql.match(/SELECT \* FROM (\w+)/i);
    return `db.${match[1]}.find({})`;
  }
  
  if (sql.match(/INSERT INTO (\w+) \(([^)]+)\) VALUES \(([^)]+)\)/i)) {
    const match = sql.match(/INSERT INTO (\w+) \(([^)]+)\) VALUES \(([^)]+)\)/i);
    const [, collection, fields, values] = match;
    const fieldArray = fields.split(',').map(f => f.trim());
    const valueArray = values.split(',').map(v => {
      v = v.trim();
      return v.startsWith("'") ? v.slice(1, -1) : parseInt(v);
    });
    const doc = {};
    fieldArray.forEach((f, i) => doc[f] = valueArray[i]);
    return `db.${collection}.insertOne(${JSON.stringify(doc, null, 2)})`;
  }
  
  return `db.collection.find({ /* Convert: ${sql.substring(0, 50)}... */ })`;
}

function convertToDynamoDB(sql) {
  if (sql.match(/SELECT \* FROM (\w+) WHERE (\w+) = (\d+|'[^']+')/i)) {
    const match = sql.match(/SELECT \* FROM (\w+) WHERE (\w+) = (\d+|'[^']+')/i);
    const [, table, key, value] = match;
    return {
      TableName: table,
      KeyConditionExpression: `${key} = :val`,
      ExpressionAttributeValues: {
        ":val": value.startsWith("'") ? value.slice(1, -1) : parseInt(value)
      }
    };
  }
  return {
    TableName: 'your-table',
    KeyConditionExpression: 'pk = :pk',
    ExpressionAttributeValues: { ':pk': 'value' }
  };
}

function convertToFirestore(sql) {
  if (sql.match(/SELECT \* FROM (\w+) WHERE (\w+) = (\d+|'[^']+')/i)) {
    const match = sql.match(/SELECT \* FROM (\w+) WHERE (\w+) = (\d+|'[^']+')/i);
    const [, collection, field, value] = match;
    const cleanValue = value.startsWith("'") ? value.slice(1, -1) : parseInt(value);
    return `db.collection('${collection}').where('${field}', '==', ${JSON.stringify(cleanValue)}).get()`;
  }
  if (sql.match(/SELECT \* FROM (\w+)/i)) {
    const match = sql.match(/SELECT \* FROM (\w+)/i);
    return `db.collection('${match[1]}').get()`;
  }
  return `db.collection('collection').get()`;
}

function suggestSchema(sql, targetDb) {
  const tableMatch = sql.match(/FROM (\w+)/i) || sql.match(/INTO (\w+)/i);
  const table = tableMatch ? tableMatch[1] : 'unknown';
  
  const schemas = {
    mongodb: {
      collection: table,
      suggestedIndexes: ['_id', 'createdAt'],
      schema: {
        bsonType: 'object',
        required: ['_id'],
        properties: {
          _id: { bsonType: 'objectId' },
          createdAt: { bsonType: 'date' },
          updatedAt: { bsonType: 'date' }
        }
      }
    },
    dynamodb: {
      tableName: table,
      keySchema: [
        { AttributeName: 'pk', KeyType: 'HASH' },
        { AttributeName: 'sk', KeyType: 'RANGE' }
      ],
      attributeDefinitions: [
        { AttributeName: 'pk', AttributeType: 'S' },
        { AttributeName: 'sk', AttributeType: 'S' }
      ]
    },
    firestore: {
      collection: table,
      documentStructure: {
        id: 'auto-generated',
        fields: 'flexible-schema'
      },
      indexing: 'automatic'
    }
  };
  
  return schemas[targetDb] || schemas.mongodb;
}

function getExplanation(targetDb) {
  const explanations = {
    mongodb: 'MongoDB uses a document-based model. SQL tables become collections, rows become documents.',
    dynamodb: 'DynamoDB is a key-value store. Design your partition keys carefully for query patterns.',
    firestore: 'Firestore is a flexible document database with real-time sync capabilities.'
  };
  return explanations[targetDb];
}
