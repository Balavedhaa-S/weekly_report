from twilio.rest import Client
import os
from dotenv import load_dotenv

load_dotenv()

TWILIO_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH = os.getenv("TWILIO_AUTH_TOKEN")
FROM_SMS = os.getenv("TWILIO_FROM_SMS")
TO_SMS = os.getenv("TWILIO_TO_SMS")
FROM_WA = os.getenv("TWILIO_FROM_WHATSAPP")
TO_WA = os.getenv("TWILIO_TO_WHATSAPP")

client = Client(TWILIO_SID, TWILIO_AUTH)


def send_whatsapp_report(report: str):
    try:
        print("📨 Sending WhatsApp message...")
        client.messages.create(
            body=f"📊 Weekly Report:\n\n{report}",
            from_=FROM_WA,
            to=TO_WA
        )
        print("✅ WhatsApp report sent.")
    except Exception as e:
        print(f"❌ WhatsApp failed: {e}")


def send_sms_report(report: str):
    try:
        print("📨 Sending SMS message...")
        client.messages.create(
            body=f"📊 Weekly Report:\n{report[:100]}...",
            from_=FROM_SMS,
            to=TO_SMS
        )
        print("✅ SMS report sent.")
    except Exception as e:
        print(f"❌ SMS failed: {e}")
