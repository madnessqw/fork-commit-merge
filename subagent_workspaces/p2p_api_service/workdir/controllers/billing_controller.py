from models import Transaction
from sqlalchemy.orm import Session

def notify_payment(payload, db: Session):
    # Log the payment payload to database
    new_tx = Transaction(
        user_email=payload.user_email,
        payment_method=payload.payment_method,
        reference=payload.transaction_reference,
        amount=payload.amount_paid,
        currency=payload.currency,
        status="pending"
    )
    db.add(new_tx)
    db.commit()
    db.refresh(new_tx)
    
    return {
        "status": "success",
        "data": {
            "transaction_reference": new_tx.reference,
            "status": "pending_verification"
        },
        "message": "Payment notification received. Your API key will be provisioned to your email upon verification."
    }
