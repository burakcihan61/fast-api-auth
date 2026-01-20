"""API endpoints for background tasks"""

from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status
from celery.result import AsyncResult
from pydantic import BaseModel, EmailStr

from app.api.deps import get_current_active_user
from app.models.user import User
from app.tasks.sample_tasks import send_email_task, generate_report_task

router = APIRouter()

class EmailTaskRequest(BaseModel):
    email: EmailStr
    subject: str = "Test Subject"
    message: str = "This is a test message from background task."

class ReportTaskRequest(BaseModel):
    report_type: str

class TaskStatusResponse(BaseModel):
    task_id: str
    status: str
    result: Any | None = None

@router.post("/email", status_code=status.HTTP_202_ACCEPTED)
async def trigger_email_task(
    request: EmailTaskRequest,
    current_user: User = Depends(get_current_active_user),
) -> dict[str, str]:
    """Trigger a simulated email sending task"""
    task = send_email_task.delay(request.email, request.subject, request.message)
    return {"task_id": task.id, "message": "Email task triggered"}

@router.post("/report", status_code=status.HTTP_202_ACCEPTED)
async def trigger_report_task(
    request: ReportTaskRequest,
    current_user: User = Depends(get_current_active_user),
) -> dict[str, str]:
    """Trigger a simulated report generation task"""
    task = generate_report_task.delay(request.report_type, current_user.id)
    return {"task_id": task.id, "message": "Report generation task triggered"}

@router.get("/{task_id}", response_model=TaskStatusResponse)
async def get_task_status(
    task_id: str,
    current_user: User = Depends(get_current_active_user),
) -> TaskStatusResponse:
    """Get the status and result of a background task"""
    task_result = AsyncResult(task_id)
    
    result = None
    if task_result.ready():
        result = task_result.result
        # If result is an Exception, return it as string
        if isinstance(result, Exception):
            result = str(result)
            
    return TaskStatusResponse(
        task_id=task_id,
        status=task_result.status,
        result=result,
    )
