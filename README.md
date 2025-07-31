# InvoiceOCR Automation Project

## Description

This project lets users upload an invoice image or PDF, extracts text using Tesseract OCR, and stores the result in a SQLite database. It uses:

- **FastAPI** (backend API)
- **Celery** (async task processor)
- **Redis** (Celery broker)
- **Tesseract** (OCR engine)
- **SQLite** (database)

## Features

- Upload invoice file → Async text extraction
- OCR using Tesseract
- Store extracted results in SQLite DB
- Check status using `/result/{task_id}` endpoint
- Dockerized with `Docker Compose`

## How to Run

### 1. Install Docker
Make sure Docker & Docker Compose are installed.

### 2. Build and start containers

```bash
docker-compose up --build
```

### 3. Test API

Use Postman or curl:
```bash
curl -F "file=@invoice.png" http://localhost:8000/upload
```

Check result:
```bash
curl http://localhost:8000/result/{task_id}
```

## Folder Structure

```
app/
  main.py          # FastAPI app
  tasks.py         # Celery task
  ocr.py           # OCR logic
  database.py      # SQLite DB connection
  models.py        # DB Models
tests/
  test_api.py      # Add test cases here
```
