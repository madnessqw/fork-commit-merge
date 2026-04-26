module.exports = async (req, res) => {
    if (req.method !== 'POST') {
        return res.status(405).json({ error: 'Method not allowed' });
    }

    try {
        const event = req.body?.meta?.event_name;

        if (event === 'order_created' || event === 'subscription_created') {
            console.log('License activated:', req.body);
            return res.status(200).json({
                success: true,
                message: 'Webhook received'
            });
        }

        return res.status(200).json({
            success: true,
            message: 'Webhook received'
        });
    } catch (error) {
        console.error('Webhook error:', error);
        return res.status(500).json({
            success: false,
            error: 'Webhook processing failed'
        });
    }
};
