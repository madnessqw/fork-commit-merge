from fastapi import Header, HTTPException, status, Depends
from typing import Optional
from sqlalchemy.orm import Session
from db import get_db
from models import APIKey

PAYPAL_EMAIL = "chaotikss@gmail.com"
AKBANK_IBAN = "TR38 0004 6002 0088 8000 1791 88"

async def verify_api_key(
    x_api_key: Optional[str] = Header(None, alias="X-API-Key"),
    db: Session = Depends(get_db)
):
    if not x_api_key:
        _raise_payment_required()

    api_key = db.query(APIKey).filter(APIKey.key_hash == x_api_key, APIKey.is_active == True).first()
    if not api_key:
        _raise_payment_required()
    return x_api_key

def _raise_payment_required():
    raise HTTPException(
        status_code=status.HTTP_402_PAYMENT_REQUIRED,
        detail={
            "status": "error",
            "message": "Valid API Key is missing or invalid. To obtain an API key, please make a payment.",
            "data": {
                "payment_methods": {
                    "paypal": PAYPAL_EMAIL,
                    "akbank_iban": AKBANK_IBAN
                },
                "instructions": "After payment, submit your transaction reference to /billing/notify to receive your API key."
            }
        }
    )
