module.exports = (req, res) => {
    res.status(200).json({
        status: 'healthy',
        service: 'ssl-cert-checker',
        timestamp: new Date().toISOString()
    });
};
