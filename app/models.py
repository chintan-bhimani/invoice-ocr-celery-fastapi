from sqlalchemy import Column, Integer, String
from app.database import Base

class Invoice(Base):
    __tablename__ = "invoices"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, index=True)
    extracted_text = Column(String)
    task_id = Column(String, unique=True, index=True)
