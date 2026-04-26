import json
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    print("Health check passed")

def test_generate_invoice_no_credit():
    payload = {
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
    
    # Empty credit
    response = client.post(
        "/api/v1/invoice/generate",
        json=payload,
        headers={"x-api-key": "test-key-empty"}
    )
    
    print(f"402 Response Status: {response.status_code}")
    print(f"402 Response Body: {json.dumps(response.json(), indent=2)}")
    
    assert response.status_code == 402
    assert "error" in response.json()
    assert "payment_link" in response.json()
    assert "chaotikss@gmail.com" in response.json()["payment_link"]

def test_generate_invoice_with_credit():
    payload = {
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
    
    # Valid credit
    response = client.post(
        "/api/v1/invoice/generate",
        json=payload,
        headers={"x-api-key": "test-key-valid"}
    )
    
    print(f"200 Response Status: {response.status_code}")
    print(f"200 Response Body: {json.dumps(response.json(), indent=2)}")
    
    assert response.status_code == 200
    assert response.json()["status"] == "success"
    assert "invoice_url" in response.json()

if __name__ == "__main__":
    test_health()
    test_generate_invoice_no_credit()
    test_generate_invoice_with_credit()
    print("ALL TESTS PASSED")
