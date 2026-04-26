# P2P API Service

This is a FastAPI-based data scraping and analysis service.

## Monetization and API Key Procurement
We use a **Direct P2P Monetization** model. In order to access the protected endpoints, you must obtain a valid `X-API-Key` by making a direct payment.

### Payment Methods
1. **PayPal:** `chaotikss@gmail.com`
2. **Akbank IBAN:** `TR38 0004 6002 0088 8000 1791 88`

### How to get an API Key
1. Make a manual payment via PayPal or Akbank IBAN using the details provided above.
2. Note your transaction ID or reference number.
3. Submit your transaction reference via our `/billing/notify` endpoint:

```bash
curl -X POST "http://localhost:8000/billing/notify" \\
     -H "Content-Type: application/json" \\
     -d '{
           "user_email": "your_email@example.com",
           "payment_method": "paypal",
           "transaction_reference": "YOUR_TRANSACTION_ID",
           "amount_paid": 10.00,
           "currency": "USD"
         }'
```

4. Once your payment is verified by our system, your API key will be provisioned.

## Using the API
Include your API Key in the headers of your requests:
`X-API-Key: your_provided_api_key`

If your API key is missing or invalid, the API will respond with `402 Payment Required` and provide the payment instructions.

### Run locally
```bash
pip install -r requirements.txt
uvicorn app:app --reload
```
