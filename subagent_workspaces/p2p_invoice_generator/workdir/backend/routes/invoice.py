from fastapi import APIRouter
from controllers.invoice_controller import InvoiceController

router = APIRouter(prefix="/api/v1/invoice", tags=["Invoice"])

router.post("/generate")(InvoiceController.create_invoice)
