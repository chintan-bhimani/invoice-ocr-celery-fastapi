# app/worker.py

from celery import Celery

celery_app = Celery("invoice_ocr", broker="redis://redis:6379/0")

@celery_app.task
def process_invoice(file_path):
    # Dummy processing
    return {"status": "success", "file_path": file_path}
