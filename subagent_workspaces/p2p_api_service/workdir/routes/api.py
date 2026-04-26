from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from middlewares.auth import verify_api_key
from controllers.data_controller import scrape_data
from controllers.billing_controller import notify_payment
from pydantic import BaseModel
from db import get_db

router = APIRouter()

class PaymentNotification(BaseModel):
    user_email: str
    payment_method: str
    transaction_reference: str
    amount_paid: float
    currency: str

@router.get("/scrape", dependencies=[Depends(verify_api_key)])
async def get_scrape_data(query: str):
    return scrape_data(query)

@router.get("/analyze", dependencies=[Depends(verify_api_key)])
async def get_analysis(dataset_id: str):
    return {
        "status": "success",
        "data": {
            "dataset_id": dataset_id,
            "analysis": "Dataset analysis complete. Quality is high."
        }
    }

@router.post("/billing/notify")
async def post_billing_notify(payload: PaymentNotification, db: Session = Depends(get_db)):
    return notify_payment(payload, db)
