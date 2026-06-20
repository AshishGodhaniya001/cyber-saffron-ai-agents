from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Dict, Any

class LeadBase(BaseModel):
    company_name: str
    contact_name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    source_platform: str

class LeadCreate(LeadBase):
    pass

class LeadOut(LeadBase):
    id: int
    score: int
    status: str
    created_at: datetime

    class Config:
        from_attributes = True

class TaskCreate(BaseModel):
    agent_name: str
    task_type: str
    payload: Dict[str, Any]
    priority: int = 1

class TaskOut(TaskCreate):
    id: int
    status: str
    created_at: datetime
    completed_at: Optional[datetime]