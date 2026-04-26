from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse
from models.invoice_schema import InvoiceRequest, InvoiceSuccessResponse
from services.invoice_service import InvoiceService
from middlewares.payment_middleware import verify_payment, deduct_credit

class InvoiceController:
    @staticmethod
    async def create_invoice(request: InvoiceRequest, api_key: str = Depends(verify_payment)):
        # Generate the invoice
        invoice_id, invoice_url = InvoiceService.generate_invoice(request.model_dump())
        
        # Deduct 1 credit for successful generation
        deduct_credit(api_key)
        
        return JSONResponse(
            content={
                "status": "success",
                "invoice_url": invoice_url,
                "invoice_id": invoice_id
            },
            status_code=200
        )
