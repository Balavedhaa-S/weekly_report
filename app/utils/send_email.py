import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

load_dotenv()

EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
TO_EMAIL = os.getenv("TO_EMAIL", EMAIL_USER)  # fallback to self if no TO_EMAIL in .env

async def send_report_email(markdown_content: str):
    try:
        print("📡 Connecting to SMTP server...")

        # Construct the message
        message = MIMEMultipart("alternative")
        message["Subject"] = "📊 Weekly Project Report"
        message["From"] = EMAIL_USER
        message["To"] = TO_EMAIL

        # Convert Markdown to HTML
        from markdown2 import markdown
        html_content = markdown(markdown_content)
        message.attach(MIMEText(html_content, "html"))
        print("📧 EMAIL_USER:", EMAIL_USER)
        print("🔐 EMAIL_PASSWORD:", EMAIL_PASSWORD)

        
        # Connect and login
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(EMAIL_USER, EMAIL_PASSWORD)
            server.send_message(message)

        print("✅ Email sent successfully!")

    except Exception as e:
        print(f"❌ Failed to send email: {e}")
