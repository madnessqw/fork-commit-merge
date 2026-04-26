const https = require('https');

module.exports = async (req, res) => {
    if (req.method !== 'POST') {
        return res.status(405).json({ error: 'Method not allowed' });
    }

    try {
        const { domain } = req.body;

        if (!domain) {
            return res.status(400).json({ error: 'Domain is required' });
        }

        const cleanDomain = domain.replace(/^https?:\/\//, '').replace(/\/.*$/, '').replace(/:\d+$/, '');

        if (!/^[a-zA-Z0-9][a-zA-Z0-9-]{1,61}[a-zA-Z0-9]\.[a-zA-Z]{2,}$/.test(cleanDomain) &&
            !/^[a-zA-Z0-9][a-zA-Z0-9-]{1,61}[a-zA-Z0-9]\.[a-zA-Z0-9][a-zA-Z0-9-]{1,61}[a-zA-Z0-9]\.[a-zA-Z]{2,}$/.test(cleanDomain)) {
            return res.status(400).json({ error: 'Invalid domain format' });
        }

        const certInfo = await getCertificateInfo(cleanDomain);

        return res.status(200).json({
            success: true,
            domain: cleanDomain,
            certificate: certInfo
        });
    } catch (error) {
        return res.status(500).json({
            success: false,
            error: error.message || 'Failed to analyze certificate'
        });
    }
};

function getCertificateInfo(hostname) {
    return new Promise((resolve, reject) => {
        const options = {
            hostname: hostname,
            port: 443,
            method: 'GET',
            timeout: 10000
        };

        const req = https.request(options, (res) => {
            const cert = res.connection.getPeerCertificate(true);

            if (!cert || Object.keys(cert).length === 0) {
                reject(new Error('No certificate found'));
                return;
            }

            const san = cert.subjectaltname ? cert.subjectaltname.replace(/DNS:/g, '').split(', ') : [];

            resolve({
                subject: cert.subject?.CN || cert.subject?.O || hostname,
                issuer: cert.issuer?.CN || cert.issuer?.O || 'Unknown',
                validFrom: cert.valid_from,
                validTo: cert.valid_to,
                serialNumber: cert.serialNumber || 'N/A',
                fingerprint: cert.fingerprint?.replace(/:/g, '').substring(0, 16) + '...' || 'N/A',
                san: san,
                subjectaltname: cert.subjectaltname || '',
                bits: cert.bits,
                modulus: cert.modulus?.substring(0, 32) + '...' || 'N/A',
                exponent: cert.exponent,
                pubkey: cert.pubkey?.substring(0, 64) + '...' || 'N/A'
            });
        });

        req.on('error', (err) => {
            reject(new Error(`Connection failed: ${err.message}`));
        });

        req.on('timeout', () => {
            req.destroy();
            reject(new Error('Connection timeout'));
        });

        req.end();
    });
}
