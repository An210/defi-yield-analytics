from fastapi import APIRouter, BackgroundTasks, Form
from services.email_service import send_alert
from services.db_service import register_email, check_apy_changes

router = APIRouter()

@router.post("/api/alerts")
async def register_alert(background_tasks: BackgroundTasks, email: str = Form(...)):
    try:
        register_email(email)
        changes = check_apy_changes()
        for change in changes:
            background_tasks.add_task(send_alert, email, change["name"], change["apy_change"])
        return {"message": "Alert registered"}
    except Exception as e:
        return {"error": str(e)}
