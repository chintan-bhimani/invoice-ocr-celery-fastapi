import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app

@pytest.mark.asyncio
async def test_upload_and_result():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        with open("tests/sample_invoice.png", "rb") as f:
            files = {"file": ("sample_invoice.png", f, "image/png")}
            response = await ac.post("/upload", files=files)
            assert response.status_code == 200
            assert "task_id" in response.json()
