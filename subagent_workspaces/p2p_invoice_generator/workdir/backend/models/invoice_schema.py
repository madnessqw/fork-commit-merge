from typing import List, Optional
from pydantic import BaseModel

class PersonInfo(BaseModel):
    name: str
    address: str
    tax_id: Optional[str] = None

class InvoiceItem(BaseModel):
    description: str
    quantity: int
    price: float

class PaymentMethods(BaseModel):
    paypal_email: Optional[str] = None
    akbank_iban: Optional[str] = None

class InvoiceRequest(BaseModel):
    sender: PersonInfo
    recipient: PersonInfo
    items: List[InvoiceItem]
    currency: str
    payment_methods: PaymentMethods

class InvoiceSuccessResponse(BaseModel):
    status: str
    invoice_url: str
    invoice_id: str

class PaymentRequiredResponse(BaseModel):
    error: str
    message: str
    payment_link: str
