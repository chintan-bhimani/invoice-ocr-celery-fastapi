from celery import Celery
from app.ocr import extract_text
from app.database import SessionLocal
from app.models import Invoice
import os

celery = Celery(__name__, broker="redis://redis:6379/0")


@celery.task(name="process_invoice")
def process_invoice(file_path: str, task_id: str):
    extracted_text = extract_text(file_path)
    db = SessionLocal()
    invoice = Invoice(filename=os.path.basename(file_path),
                      extracted_text=extracted_text,
                      task_id=task_id)
    db.add(invoice)
    db.commit()
    db.close()
