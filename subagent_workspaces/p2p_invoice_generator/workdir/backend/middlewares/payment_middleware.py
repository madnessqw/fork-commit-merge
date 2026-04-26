from fastapi import HTTPException, Header, Request, status
import json

# A dummy database of user credits (API Key: Credits)
USER_CREDITS = {
    "test-key-valid": 10,
    "test-key-empty": 0,
}

PAYPAL_EMAIL = "chaotikss@gmail.com"
TOPUP_AMOUNT = "5.00"

def verify_payment(x_api_key: str = Header(default="guest")):
    credits = USER_CREDITS.get(x_api_key, 0)
    
    if credits <= 0:
        # Create PayPal Me link or PayPal Checkout link for chaotikss@gmail.com
        paypal_link = f"https://www.paypal.com/cgi-bin/webscr?cmd=_xclick&business={PAYPAL_EMAIL}&item_name=API+Credits+Top-up&amount={TOPUP_AMOUNT}&currency_code=USD"
        
        raise HTTPException(
            status_code=402,
            detail={
                "error": "Payment Required",
                "message": "Your API balance is 0. Please top up to generate invoices.",
                "payment_link": paypal_link
            }
        )
    
    return x_api_key

def deduct_credit(api_key: str):
    if api_key in USER_CREDITS and USER_CREDITS[api_key] > 0:
        USER_CREDITS[api_key] -= 1
