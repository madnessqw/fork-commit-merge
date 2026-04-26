module.exports = (req, res) => {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  const { hex, encoding = 'utf8' } = req.body || {};

  if (!hex) {
    return res.status(400).json({ error: 'No hex data provided' });
  }

  try {
    // Parse hex string
    const hexBytes = hex.replace(/\s/g, '').match(/.{1,2}/g) || [];
    const bytes = hexBytes.map(b => parseInt(b, 16));

    // Generate hex dump
    const lines = [];
    for (let i = 0; i < bytes.length; i += 16) {
      const chunk = bytes.slice(i, i + 16);
      const offset = i.toString(16).padStart(8, '0');

      const hexStr = chunk.map(b => b.toString(16).padStart(2, '0').toUpperCase()).join(' ');
      const ascii = chunk.map(b => {
        return (b >= 32 && b < 127) ? String.fromCharCode(b) : '.';
      }).join('');

      lines.push({
        offset,
        hex: hexStr.padEnd(48, ' '),
        ascii
      });
    }

    // Detect file signature
    const signatures = {
      '89504E47': 'PNG Image',
      'FFD8FF': 'JPEG Image',
      '25504446': 'PDF Document',
      '504B0304': 'ZIP Archive',
      '52617221': 'RAR Archive',
      '7F454C46': 'ELF Executable',
      '4D5A': 'Windows Executable',
      '1F8B08': 'GZIP Compressed'
    };

    let detectedFormat = 'Unknown';
    const hexPrefix = hex.replace(/\s/g, '').substring(0, 8).toUpperCase();
    for (const [sig, format] of Object.entries(signatures)) {
      if (hexPrefix.startsWith(sig)) {
        detectedFormat = format;
        break;
      }
    }

    res.json({
      status: 'success',
      dump: lines,
      summary: {
        totalBytes: bytes.length,
        detectedFormat,
        encoding
      }
    });
  } catch (error) {
    res.status(400).json({ error: 'Invalid hex data', details: error.message });
  }
};
