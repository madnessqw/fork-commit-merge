import smtplib
import csv
import json
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

CONFIG_FILE = "email_config.json"
LEADS_FILE = "leads.csv"

def load_config():
    if not os.path.exists(CONFIG_FILE):
        print(f"Error: Configuration file {CONFIG_FILE} not found.")
        print("Please create it with the following structure:")
        print('{"smtp_server": "smtp.gmail.com", "smtp_port": 587, "sender_email": "...", "sender_password": "..."}')
        return None
    with open(CONFIG_FILE, "r") as f:
        return json.load(f)

def load_leads():
    if not os.path.exists(LEADS_FILE):
        print(f"Error: Leads file {LEADS_FILE} not found.")
        return []
    leads = []
    with open(LEADS_FILE, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if 'email' in row and row['email']:
                leads.append(row)
    return leads

def send_emails():
    config = load_config()
    if not config:
        return

    leads = load_leads()
    if not leads:
        print("No leads found to send emails to.")
        return

    subject = "Scale Your Infrastructure with Our P2P API Stack"
    body_template = """Hi {name},

Are you tired of paying exorbitant cloud fees for simple API hosting? 
Our new P2P API Stack allows you to deploy and scale your backend services directly across a peer-to-peer network, cutting your infrastructure costs by up to 80% while increasing resilience.

Key Benefits:
- Zero Centralized Servers: True P2P architecture.
- Instant Scaling: Automatically utilizes available network nodes.
- Unbeatable Pricing: Pay only for the compute you actually use.

Ready to revolutionize your infrastructure? Reply to this email to get early access.

Best regards,
The P2P API Stack Team
"""

    smtp_server = config.get("smtp_server")
    smtp_port = config.get("smtp_port")
    sender_email = config.get("sender_email")
    sender_password = config.get("sender_password")

    if sender_email == "your_email@gmail.com":
        print("Warning: Please update email_config.json with real credentials to actually send emails. Running in mock mode.")
        mock_mode = True
    else:
        mock_mode = False

    if not mock_mode:
        try:
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()
            server.login(sender_email, sender_password)
            print("Successfully connected to SMTP server.")
        except Exception as e:
            print(f"Failed to connect to SMTP server: {e}")
            return

    for lead in leads:
        name = lead.get('name', 'there')
        email = lead.get('email')
        
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = email
        msg['Subject'] = subject
        
        body = body_template.format(name=name)
        msg.attach(MIMEText(body, 'plain'))
        
        if mock_mode:
            print(f"[MOCK] Sending email to {email} (Name: {name})")
            print(f"[MOCK] Subject: {subject}")
            print("---")
        else:
            try:
                server.send_message(msg)
                print(f"Successfully sent email to {email}")
            except Exception as e:
                print(f"Failed to send email to {email}: {e}")

    if not mock_mode:
        try:
            server.quit()
        except:
            pass

if __name__ == "__main__":
    send_emails()