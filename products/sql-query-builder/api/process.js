module.exports = (req, res) => {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  const { action, tables, fields, conditions, joins } = req.body;

  try {
    let query = '';

    switch (action) {
      case 'SELECT':
        query = buildSelectQuery(tables, fields, conditions, joins);
        break;
      case 'INSERT':
        query = buildInsertQuery(tables, fields);
        break;
      case 'UPDATE':
        query = buildUpdateQuery(tables, fields, conditions);
        break;
      case 'DELETE':
        query = buildDeleteQuery(tables, conditions);
        break;
      default:
        return res.status(400).json({ error: 'Invalid action' });
    }

    res.json({
      success: true,
      query,
      action,
      timestamp: new Date().toISOString()
    });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
};

function buildSelectQuery(tables, fields, conditions, joins) {
  const fieldStr = fields && fields.length > 0 ? fields.join(', ') : '*';
  let query = `SELECT ${fieldStr} FROM ${tables[0]}`;

  if (joins && joins.length > 0) {
    joins.forEach(join => {
      query += ` ${join.type} JOIN ${join.table} ON ${join.condition}`;
    });
  }

  if (conditions && conditions.length > 0) {
    const whereClause = conditions.map(c => `${c.field} ${c.operator} '${c.value}'`).join(' AND ');
    query += ` WHERE ${whereClause}`;
  }

  return query + ';';
}

function buildInsertQuery(table, fields) {
  const columns = Object.keys(fields).join(', ');
  const values = Object.values(fields).map(v => `'${v}'`).join(', ');
  return `INSERT INTO ${table} (${columns}) VALUES (${values});`;
}

function buildUpdateQuery(table, fields, conditions) {
  const setClause = Object.entries(fields).map(([k, v]) => `${k} = '${v}'`).join(', ');
  let query = `UPDATE ${table} SET ${setClause}`;

  if (conditions && conditions.length > 0) {
    const whereClause = conditions.map(c => `${c.field} ${c.operator} '${c.value}'`).join(' AND ');
    query += ` WHERE ${whereClause}`;
  }

  return query + ';';
}

function buildDeleteQuery(table, conditions) {
  let query = `DELETE FROM ${table}`;

  if (conditions && conditions.length > 0) {
    const whereClause = conditions.map(c => `${c.field} ${c.operator} '${c.value}'`).join(' AND ');
    query += ` WHERE ${whereClause}`;
  }

  return query + ';';
}
