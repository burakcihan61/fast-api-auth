"""Tests for background tasks"""

import pytest
from unittest.mock import patch
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_trigger_email_task_success(client: AsyncClient, normal_user_token_headers: dict[str, str]):
    """Test triggering an email task successfully"""
    # Mock celery task .delay() method
    with patch("app.tasks.sample_tasks.send_email_task.delay") as mock_delay:
        mock_delay.return_value.id = "test-task-id"
        
        response = await client.post(
            "/api/v1/tasks/email",
            json={
                "email": "test@example.com",
                "subject": "Test Subject",
                "message": "Hello World"
            },
            headers=normal_user_token_headers
        )
        
        assert response.status_code == 202
        assert response.json()["task_id"] == "test-task-id"
        mock_delay.assert_called_once_with("test@example.com", "Test Subject", "Hello World")

@pytest.mark.asyncio
async def test_trigger_report_task_success(client: AsyncClient, normal_user_token_headers: dict[str, str]):
    """Test triggering a report task successfully"""
    with patch("app.tasks.sample_tasks.generate_report_task.delay") as mock_delay:
        mock_delay.return_value.id = "report-task-id"
        
        response = await client.post(
            "/api/v1/tasks/report",
            json={"report_type": "monthly"},
            headers=normal_user_token_headers
        )
        
        assert response.status_code == 202
        assert response.json()["task_id"] == "report-task-id"
        # We don't check user_id precisely here but ensure it was called
        assert mock_delay.called

@pytest.mark.asyncio
async def test_get_task_status(client: AsyncClient, normal_user_token_headers: dict[str, str]):
    """Test getting status of a task"""
    with patch("app.api.v1.tasks.AsyncResult") as mock_result:
        mock_result.return_value.status = "SUCCESS"
        mock_result.return_value.ready.return_value = True
        mock_result.return_value.result = {"status": "completed"}
        
        response = await client.get(
            "/api/v1/tasks/test-task-id",
            headers=normal_user_token_headers
        )
        
        assert response.status_code == 200
        assert response.json()["status"] == "SUCCESS"
        assert response.json()["result"] == {"status": "completed"}

@pytest.mark.asyncio
async def test_tasks_require_auth(client: AsyncClient):
    """Test that task endpoints require authentication"""
    response = await client.post("/api/v1/tasks/email", json={})
    assert response.status_code == 401
