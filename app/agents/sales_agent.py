import json
from typing import Dict, Any
from app.agents.base import BaseAgent
from app.models import Lead, LeadStatus
from app.database import AsyncSessionLocal
from app.tools.email import send_email

class SalesAgent(BaseAgent):
    def __init__(self):
        super().__init__("Sales")

    async def run(self, task: Dict[str, Any]) -> Dict[str, Any]:
        task_type = task.get("task_type")
        payload = task.get("payload", {})
        if task_type == "contact_lead":
            lead_id = payload.get("lead_id")
            return await self._contact_lead(lead_id)
        return {"error": "unknown task_type"}

    async def _contact_lead(self, lead_id: int) -> Dict[str, Any]:
        async with AsyncSessionLocal() as db:
            lead = await db.get(Lead, lead_id)
            if not lead:
                return {"error": "Lead not found"}
            if not lead.email:
                lead.status = LeadStatus.LOST
                await db.commit()
                return {"error": "No email available", "lead_id": lead_id}
            email_body = f"""
            <h2>Hello {lead.contact_name or lead.company_name},</h2>
            <p>We noticed your company <strong>{lead.company_name}</strong> could benefit from our digital services including websites, AI automation, marketing, SEO, and cybersecurity solutions.</p>
            <p>Would you be available for a quick call this week?</p>
            <br>
            <p>Best regards,<br>Cyber Saffron Team</p>
            """
            result = await send_email(
                to=lead.email,
                subject=f"Digital solutions for {lead.company_name}",
                body=email_body
            )
            success = "error" not in result
            if success:
                lead.status = LeadStatus.CONTACTED
            await db.commit()
            return {"lead_id": lead_id, "email_sent": success, "to": lead.email}
