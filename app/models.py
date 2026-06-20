from sqlalchemy import Column, Integer, String, Float, DateTime, Text, Enum
from sqlalchemy.sql import func
from app.database import Base
import enum

class LeadStatus(str, enum.Enum):
    RAW = "raw"
    QUALIFIED = "qualified"
    CONTACTED = "contacted"
    LOST = "lost"

class Lead(Base):
    __tablename__ = "leads"
    id = Column(Integer, primary_key=True)
    company_name = Column(String(255), nullable=False)
    contact_name = Column(String(255))
    email = Column(String(255), index=True)
    phone = Column(String(50))
    linkedin_url = Column(String(500))
    source_platform = Column(String(50))
    raw_data = Column(Text)
    score = Column(Integer, default=0)
    status = Column(Enum(LeadStatus), default=LeadStatus.RAW, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True)
    agent_name = Column(String(100))
    task_type = Column(String(100))
    payload = Column(Text)
    priority = Column(Integer, default=1)
    status = Column(String(50), default="pending")
    result = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    completed_at = Column(DateTime(timezone=True))

class KPIEvent(Base):
    __tablename__ = "kpi_events"
    id = Column(Integer, primary_key=True)
    agent_name = Column(String(100))
    metric_name = Column(String(100))
    metric_value = Column(Float)
    target_value = Column(Float)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())