import pytest
from unittest.mock import patch
from httpx import AsyncClient
from httpx import ASGITransport
from app.main import app


@pytest.mark.asyncio
async def test_upload_and_result():
    transport = ASGITransport(app=app)
    with patch("app.worker.process_invoice.delay") as mock_task:
        mock_task.return_value = {"task_id": "dummy123"}

        async with AsyncClient(transport=transport, base_url="http://test") as ac:
            with open("tests/sample_invoice.png", "rb") as f:
                files = {"file": ("sample_invoice.png", f, "image/png")}
                response = await ac.post("/upload", files=files)

            assert response.status_code == 200
            assert "task_id" in response.json()
