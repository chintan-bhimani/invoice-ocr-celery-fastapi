from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi import Request
from app.tasks import process_invoice
from app.database import SessionLocal, engine
from app import models
from app.models import Invoice
import shutil
import uuid
import os

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="app/templates")

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/upload")
async def upload_invoice(file: UploadFile = File(...)):
    if not file.filename.endswith((".png", ".jpg", ".jpeg", ".pdf")):
        raise HTTPException(status_code=400,
                            detail="Only image or PDF files are allowed.")
    task_id = str(uuid.uuid4())
    filename = f"uploaded_{task_id}_{file.filename}"
    file_path = os.path.join("uploads", filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    process_invoice.delay(file_path, task_id)
    return {"task_id": task_id, "msg": "File received, processing started"}


@app.get("/result/{task_id}")
async def get_result(task_id: str):
    db = SessionLocal()
    invoice = db.query(Invoice).filter(Invoice.task_id == task_id).first()
    db.close()
    if invoice:
        return {"filename": invoice.filename, "text": invoice.extracted_text}
    raise HTTPException(status_code=404, detail="Result not found")
