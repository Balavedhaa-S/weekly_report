import smtplib
import ssl
from email.message import EmailMessage
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

OUTLOOK_USER = os.getenv("OUTLOOK_USER")
OUTLOOK_PASSWORD = os.getenv("OUTLOOK_PASSWORD")
SMTP_SERVER = os.getenv("OUTLOOK_SMTP_SERVER", "smtp.office365.com")
SMTP_PORT = int(os.getenv("OUTLOOK_SMTP_PORT", 587))

def send_outlook_email(subject: str, body: str, to_email: str):
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = OUTLOOK_USER
    msg['To'] = to_email
    msg.set_content(body)

    try:
        context = ssl.create_default_context()
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls(context=context)
            server.login(OUTLOOK_USER, OUTLOOK_PASSWORD)
            server.send_message(msg)
        print("✅ Outlook Email Sent Successfully!")
    except Exception as e:
        print(f"❌ Outlook Email Failed: {e}")

# Example Usage
send_outlook_email("📊 Weekly Project Report", "Your weekly project report is attached.", "manager@example.com")
