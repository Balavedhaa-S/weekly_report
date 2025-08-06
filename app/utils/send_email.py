import smtplib
import ssl
from email.message import EmailMessage
import os
from dotenv import load_dotenv

load_dotenv()

EMAIL_FROM = os.getenv("EMAIL_FROM")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
EMAIL_TO = os.getenv("EMAIL_TO")
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))


async def send_report_email(markdown_report: str):
    print("📡 Connecting to SMTP server...")
    print(f"📧 EMAIL_FROM: {EMAIL_FROM}")
    print(f"🔐 EMAIL_PASSWORD: {'*' * len(EMAIL_PASSWORD)}")

    if not EMAIL_FROM or not EMAIL_PASSWORD:
        print("❌ EMAIL credentials missing in .env")
        return

    msg = EmailMessage()
    msg["Subject"] = "📊 Weekly Project Report"
    msg["From"] = EMAIL_FROM
    msg["To"] = EMAIL_TO
    msg.set_content("Your weekly project report is attached below.")
    msg.add_alternative(f"<html><body><pre>{markdown_report}</pre></body></html>", subtype="html")
    print(f"📨 Sending TO: {EMAIL_TO}")

    try:
        context = ssl.create_default_context()
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls(context=context)
            server.login(EMAIL_FROM, EMAIL_PASSWORD)
            server.send_message(msg)
        print("✅ Email sent successfully!")
    except Exception as e:
        print(f"❌ Failed to send email: {e}")
