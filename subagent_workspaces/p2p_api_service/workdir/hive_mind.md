# P2P API Service - Hive Mind & Data Contract

## 1. Project Overview
A Python FastAPI service providing specialized data scraping and analysis endpoints for developers. The monetization is Direct P2P: users pay via PayPal or Akbank IBAN to receive a valid API key.

## 2. Direct P2P Monetization Details
- **PayPal:** chaotikss@gmail.com
- **Akbank IBAN:** TR38 0004 6002 0088 8000 1791 88
- **Billing Logic:** Users must make a manual transfer and provide proof of payment (e.g., transaction ID/reference) via a specific endpoint or manual onboarding process. Once verified, an API Key is provisioned.
- **README Requirements:** Must explicitly instruct users on how to pay via these methods to get an API key.

## 3. Data Contracts
### API Key Header
- **Header:** `X-API-Key`
- **Validation:** Must be validated against a database of active keys.

### Payment Notification Payload (Backend -> DB)
```json
{
  "user_email": "string",
  "payment_method": "paypal | akbank",
  "transaction_reference": "string",
  "amount_paid": "float",
  "currency": "string"
}
```

### API Response Format (Standard)
```json
{
  "status": "success | error",
  "data": {},
  "message": "string (optional, usually for errors or warnings)"
}
```

## 4. Architecture Plan
- **Backend (FastAPI):** Expose scraping endpoints, validate `X-API-Key`, handle rate limiting, and provide a `/billing/notify` endpoint for users to submit transaction references.
- **Database (SQLite):** `db.py` handles SQLAlchemy connections. `models.py` contains:
  - `APIKey`: key_hash, user_email, credits, is_active.
  - `Transaction`: api_key_id, reference, payment_method, amount, status ('pending', 'verified', 'rejected').
  - `UsageLog`: api_key_id, endpoint, credits_used, timestamp.
- **DevOps:** Dockerize the FastAPI app, set up `docker-compose.yml` including the database, and provide a clear deployment script.