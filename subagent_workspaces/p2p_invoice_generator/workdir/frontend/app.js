document.getElementById('invoiceForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const submitBtn = document.getElementById('submitBtn');
    const resultArea = document.getElementById('resultArea');
    
    submitBtn.disabled = true;
    submitBtn.textContent = 'Generating...';
    resultArea.classList.add('hidden');
    
    // Construct payload according to Data Contract
    const payload = {
        sender: {
            name: document.getElementById('senderName').value,
            address: document.getElementById('senderAddress').value,
            tax_id: document.getElementById('senderTaxId').value
        },
        recipient: {
            name: document.getElementById('recipientName').value,
            address: document.getElementById('recipientAddress').value
        },
        items: [
            {
                description: document.getElementById('itemDescription').value,
                quantity: parseFloat(document.getElementById('itemQuantity').value),
                price: parseFloat(document.getElementById('itemPrice').value)
            }
        ],
        currency: document.getElementById('currency').value,
        payment_methods: {
            paypal_email: document.getElementById('paypalEmail').value,
            akbank_iban: document.getElementById('akbankIban').value
        }
    };

    try {
        // Assume API is on same origin or handled via CORS
        const response = await fetch('/api/v1/invoice/generate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(payload)
        });

        // Backend returns 402 for Payment Required
        if (response.status === 402) {
            const data = await response.json();
            showResult('error', data.message || 'Payment Required to generate invoice.', data.payment_link, 'Top up API Balance');
        } else if (response.ok) {
            const data = await response.json();
            showResult('success', 'Invoice generated successfully!', data.invoice_url, 'Download Invoice');
        } else {
            const errorText = await response.text();
            showResult('error', `An error occurred: ${response.status} ${errorText}`);
        }
    } catch (error) {
        showResult('error', `Network error: ${error.message}. Is the backend running?`);
    } finally {
        submitBtn.disabled = false;
        submitBtn.textContent = 'Generate Invoice';
    }
});

function showResult(type, message, linkUrl = null, linkText = null) {
    const resultArea = document.getElementById('resultArea');
    resultArea.innerHTML = '';
    resultArea.classList.remove('hidden');

    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type}`;
    alertDiv.textContent = message;
    resultArea.appendChild(alertDiv);

    if (linkUrl && linkText) {
        const actionLink = document.createElement('a');
        actionLink.href = linkUrl;
        actionLink.className = 'btn-link';
        actionLink.textContent = linkText;
        actionLink.target = '_blank'; // Open in new tab
        resultArea.appendChild(actionLink);
    }
}