from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.utils.report_generator import get_project_report
from app.utils.send_email import send_report_email

router = APIRouter()

# ✅ Route for previewing the weekly report (Markdown format)
@router.get("/weekly-report/{project_id}")
def generate_report(project_id: int, db: Session = Depends(get_db)):
    report = get_project_report(db, project_id)
    if "markdown" not in report:
        return {"error": "Could not generate report"}
    return report

# ✅ Route to send the report via email (Markdown content)
@router.get("/send-weekly-report/{project_id}")
async def send_weekly_report(project_id: int, db: Session = Depends(get_db)):
    report = get_project_report(db, project_id)
    if "markdown" not in report:
        return {"error": "Could not generate report"}

    await send_report_email(report["markdown"])
    return {"message": "Report sent via email"}


from fastapi import APIRouter
from app.utils.send_outlook import send_outlook_email

router = APIRouter()

@router.get("/send-outlook-report")
def send_report():
    subject = "📊 Weekly Project Report"
    body = "Your weekly project report is attached."
    manager_email = "manager@example.com"

    send_outlook_email(subject, body, manager_email)
    return {"message": "Outlook email sent successfully!"}