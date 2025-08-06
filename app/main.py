from fastapi import FastAPI
from app.routers import report
from app.utils.report_generator import get_project_report
from app.utils.send_email import send_report_email
from app.utils.send_whatsapp_sms import send_whatsapp_report, send_sms_report
from app.utils.send_outlook import send_outlook_email

from app.database import SessionLocal
import asyncio
import schedule
import time
import threading
import datetime

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Welcome to Weekly Report Generator"}

app.include_router(report.router)


# 🕒 Background job function
def schedule_job():
    db = SessionLocal()
    try:
        # Example: Send report for project_id 1
        report = get_project_report(db, project_id=1)
        markdown = report["markdown"]
        print(f"🕒 Running scheduled report job... ({datetime.datetime.now()})")

        asyncio.run(send_report_email(markdown))
        send_whatsapp_report(markdown)
        send_sms_report(markdown)

        print("✅ All channels sent!")
    except Exception as e:
        print(f"❌ Scheduled job failed: {e}")
    finally:
        db.close()


# 🌀 Thread to keep schedule running
def run_scheduler():
    #schedule.every().friday.at("11:35").do(schedule_job)
    # For testing only (remove after)
    schedule.every(1).minutes.do(schedule_job)

    while True:
        schedule.run_pending()
        time.sleep(10)


# 🔁 Start scheduler in background
threading.Thread(target=run_scheduler, daemon=True).start()

def schedule_job():
    # Your logic to fetch the report
    report_content = "Your weekly project report is attached."
    subject = "📊 Weekly Project Report"
    manager_email = "manager@example.com"

    # Send the email via Outlook
    send_outlook_email(subject, report_content, manager_email)