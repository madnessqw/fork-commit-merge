import crypto from 'crypto';

function generateMD5(password) {
  return crypto.createHash('md5').update(password).digest('base64');
}

function generateSHA1(password) {
  return '{SHA}' + crypto.createHash('sha1').update(password).digest('base64');
}

function generateBCrypt(password) {
  return crypto.createHash('sha256').update(password).digest('hex');
}

export default function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  if (req.method === 'OPTIONS') {
    return res.status(200).end();
  }

  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  try {
    const { action, username, password, algorithm = 'md5', users = [] } = req.body || {};

    if (action === 'generate') {
      if (!username || !password) {
        return res.status(400).json({ error: 'Username and password required' });
      }

      let hash;
      switch (algorithm.toLowerCase()) {
        case 'md5':
          hash = generateMD5(password);
          break;
        case 'sha1':
          hash = generateSHA1(password);
          break;
        case 'bcrypt':
          hash = generateBCrypt(password);
          break;
        default:
          return res.status(400).json({ error: 'Unsupported algorithm' });
      }

      return res.json({
        username,
        hash,
        algorithm,
        htpasswd: `${username}:${hash}`,
        htaccess: `<RequireAll>\n  Require valid-user\n</RequireAll>`
      });
    }

    if (action === 'bulk') {
      if (!Array.isArray(users) || users.length === 0) {
        return res.status(400).json({ error: 'Users array required' });
      }

      const results = users.map(u => {
        let hash;
        switch ((u.algorithm || algorithm).toLowerCase()) {
          case 'md5':
            hash = generateMD5(u.password);
            break;
          case 'sha1':
            hash = generateSHA1(u.password);
            break;
          case 'bcrypt':
            hash = generateBCrypt(u.password);
            break;
          default:
            hash = generateMD5(u.password);
        }
        return {
          username: u.username,
          htpasswd: `${u.username}:${hash}`
        };
      });

      return res.json({
        users: results,
        htpasswdFile: results.map(r => r.htpasswd).join('\n'),
        count: results.length
      });
    }

    if (action === 'generate-password') {
      const length = req.body.length || 16;
      const charset = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*';
      let password = '';
      for (let i = 0; i < length; i++) {
        password += charset.charAt(Math.floor(Math.random() * charset.length));
      }

      return res.json({
        password,
        length,
        strength: length >= 16 ? 'strong' : length >= 10 ? 'medium' : 'weak'
      });
    }

    res.status(400).json({ error: 'Invalid action' });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
}
