import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.asyncio
async def test_upload_and_result():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        with open("tests/sample_invoice.png", "rb") as f:
            files = {"file": ("sample_invoice.png", f, "image/png")}
            response = await ac.post("/upload", files=files)
            assert response.status_code == 200
            assert "task_id" in response.json()
