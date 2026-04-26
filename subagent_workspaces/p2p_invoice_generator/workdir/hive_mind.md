# Hive Mind: P2P Invoice Generator API - Data Contract

Bu dosya `backend-engineer` ve `frontend-engineer` arasındaki sözleşmeyi (API Spesifikasyonunu) tanımlar.

## Endpoint: POST /api/v1/invoice/generate

### İstek (Request Body)
```json
{
  "sender": {
    "name": "Jane Doe",
    "address": "123 Main St",
    "tax_id": "1234567890"
  },
  "recipient": {
    "name": "Acme Corp",
    "address": "456 Corp Blvd"
  },
  "items": [
    {
      "description": "Web Development",
      "quantity": 1,
      "price": 1000.00
    }
  ],
  "currency": "USD",
  "payment_methods": {
    "paypal_email": "jane.doe@paypal.com",
    "akbank_iban": "TR120000000000000000000000"
  }
}
```

### Yanıt (Başarılı - 200 OK)
```json
{
  "status": "success",
  "invoice_url": "https://api.domain.com/invoices/inv_12345.pdf",
  "invoice_id": "inv_12345"
}
```

### Yanıt (Ödeme Gerekli - 402 Payment Required)
```json
{
  "error": "Payment Required",
  "message": "Your API balance is 0. Please top up to generate invoices.",
  "payment_link": "https://api.domain.com/pay?amount=5.00&currency=USD"
}
```

Frontend, bu sözleşmeye (Data Contract) uygun olarak HTTP istekleri yapacak ve yanıtları işleyecektir. Backend, bu uç noktayı ve payload yapısını tam olarak uygulayacaktır.
