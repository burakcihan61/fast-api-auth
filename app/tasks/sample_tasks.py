"""Sample background tasks"""

import time

from app.core.celery_app import celery_app
from app.core.logging import logger


@celery_app.task(name="send_email_task")
def send_email_task(email: str, subject: str, message: str) -> dict:
    """Simulate sending an email"""
    logger.info(f"Starting email task for {email}")
    # Simulate work
    time.sleep(5)
    logger.info(f"Finished email task for {email}")
    return {"status": "success", "recipient": email, "subject": subject}

@celery_app.task(name="generate_report_task")
def generate_report_task(report_type: str, user_id: int) -> dict:
    """Simulate generating a report"""
    logger.info(f"Starting report generation for user {user_id} (type: {report_type})")
    # Simulate heavy work
    time.sleep(10)
    logger.info(f"Finished report generation for user {user_id}")
    return {
        "status": "completed",
        "report_type": report_type,
        "user_id": user_id,
        "download_url": f"https://example.com/reports/{report_type}_{user_id}.pdf"
    }
