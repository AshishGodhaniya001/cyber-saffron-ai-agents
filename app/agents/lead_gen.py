import json
from typing import Dict, Any
from sqlalchemy import select
from app.agents.base import BaseAgent
from app.models import Lead, LeadStatus, Task
from app.database import AsyncSessionLocal
from app.tools.scrapers import scrape_all_platforms
from app.tools.scoring import score_lead

class LeadGenAgent(BaseAgent):
    def __init__(self):
        super().__init__("LeadGen")

    async def run(self, task: Dict[str, Any]) -> Dict[str, Any]:
        task_type = task.get("task_type")
        payload = task.get("payload", {})
        if task_type == "daily_scan":
            return await self._discover_leads()
        elif task_type == "score_and_qualify":
            lead_id = payload.get("lead_id")
            return await self._score_and_qualify(lead_id)
        return {"error": "unknown task_type"}

    async def _discover_leads(self) -> Dict[str, Any]:
        try:
            raw_leads = await scrape_all_platforms()
        except Exception as e:
            self.logger.exception(f"Scraping failed: {e}")
            return {"error": str(e)}
        self.logger.info(f"Raw leads from scrapers: {len(raw_leads)}")
        saved_ids = []
        async with AsyncSessionLocal() as db:
            for lead_data in raw_leads:
                if lead_data.get("email"):
                    existing = await db.execute(
                        select(Lead).where(Lead.email == lead_data["email"])
                    )
                    if existing.scalar():
                        self.logger.info(f"Skipping duplicate: {lead_data['email']}")
                        continue
                self.logger.info(f"Inserting lead: {lead_data.get('company_name')}")
                lead = Lead(
                    company_name=lead_data.get("company_name", "Unknown"),
                    contact_name=lead_data.get("contact_name"),
                    email=lead_data.get("email"),
                    phone=lead_data.get("phone"),
                    source_platform=lead_data.get("source_platform", "unknown"),
                    raw_data=json.dumps(lead_data),
                    status=LeadStatus.RAW
                )
                db.add(lead)
                await db.flush()
                saved_ids.append(lead.id)
            for lid in saved_ids:
                task = Task(
                    agent_name="LeadGen",
                    task_type="score_and_qualify",
                    payload=json.dumps({"lead_id": lid}),
                    priority=2
                )
                db.add(task)
            await db.commit()
        return {"discovered": len(saved_ids)}

    async def _score_and_qualify(self, lead_id: int) -> Dict[str, Any]:
        async with AsyncSessionLocal() as db:
            lead = await db.get(Lead, lead_id)
            if not lead:
                return {"error": "Lead not found"}
            try:
                score = await score_lead(lead.raw_data)
            except Exception as e:
                self.logger.exception(f"Scoring lead {lead_id} failed: {e}")
                score = 0
            lead.score = score
            if score >= 70:
                lead.status = LeadStatus.QUALIFIED
                sales_task = Task(
                    agent_name="Sales",
                    task_type="contact_lead",
                    payload=json.dumps({"lead_id": lead.id}),
                    priority=5
                )
                db.add(sales_task)
            else:
                lead.status = LeadStatus.LOST
            await db.commit()
            return {"lead_id": lead_id, "score": score, "qualified": score >= 70}