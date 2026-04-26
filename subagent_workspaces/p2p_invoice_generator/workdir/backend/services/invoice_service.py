import uuid

class InvoiceService:
    @staticmethod
    def generate_invoice(invoice_data: dict) -> str:
        # In a real application, this would render HTML/PDF using Jinja2 or ReportLab
        # For now, we simulate the PDF generation and return a dummy URL.
        invoice_id = f"inv_{uuid.uuid4().hex[:8]}"
        dummy_url = f"https://api.domain.com/invoices/{invoice_id}.pdf"
        
        return invoice_id, dummy_url
