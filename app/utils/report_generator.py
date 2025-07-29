from sqlalchemy.orm import Session
from app.models import Project, Phase, Task
from datetime import datetime, timedelta

def get_project_report(db: Session, project_id: int):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        return {"error": "Project not found"}

    today = datetime.now().date()
    one_week_ago = today - timedelta(days=7)

    phases = db.query(Phase).filter(Phase.project_id == project_id).all()

    report_lines = []
    task_lines = []
    phase_lines = []

    finance_section = """
**Finance This Week:**
- ₹20,00,000 requested → ₹5,00,000 approved
- All approvals cleared
"""

    total_tasks = 0
    completed_tasks = 0

    for phase in phases:
        status_emoji = {
            "completed": "✅",
            "in_progress": "🔧",
            "not_started": "⏳"
        }.get(phase.status, "❔")

        phase_lines.append(f"{len(phase_lines)+1}. {status_emoji} {phase.phase_name} - {phase.status.replace('_', ' ').title()}")

        tasks = db.query(Task).filter(Task.phase_id == phase.id).all()

        for task in tasks:
            total_tasks += 1
            if task.status == "COMPLETED":
                completed_tasks += 1

            status_emoji = {
                "COMPLETED": "✅",
                "IN_PROGRESS": "🔧",
                "NOT_STARTED": "⏳"
            }.get(task.status, "❔")

            estimated = f"₹{task.estimated_budget:,}" if task.estimated_budget else "N/A"
            actual = f"₹{task.actual_budget:,}" if task.actual_budget else "N/A"

            if task.status == "COMPLETED":
                task_lines.append(f"- {task.name} → {status_emoji} Completed ({estimated})")
            elif task.status == "IN_PROGRESS":
                task_lines.append(f"- {task.name} → {status_emoji} In Progress ({estimated} estimated, {actual} spent)")
            else:
                task_lines.append(f"- {task.name} → {status_emoji} Not Started")

    report_md = f"""
### 📝 Weekly Project Report (Generated: {today})

#### 📁 Project: {project.project_name}
- Status: {project.status.replace('_', ' ').title()}
- Manager: {project.manager.name}
- Duration: {project.start_date.strftime('%b %d, %Y')} → {project.end_date.strftime('%b %d, %Y')}

**Phases:**
{chr(10).join(phase_lines)}

**Tasks Summary:**
{chr(10).join(task_lines)}

{finance_section}

---
""".strip()

    return {"markdown": report_md}
