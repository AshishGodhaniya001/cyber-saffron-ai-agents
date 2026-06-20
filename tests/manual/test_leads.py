import asyncio
import sys
sys.path.insert(0, ".")

from app.database import AsyncSessionLocal
from app.models import Lead, Task
from sqlalchemy import select
from app.agents.lead_gen import LeadGenAgent

async def test():
    agent = LeadGenAgent()
    result = await agent.run({"task_type": "daily_scan"})
    print("Result:", result)
    
    async with AsyncSessionLocal() as db:
        leads = (await db.execute(select(Lead))).scalars().all()
        tasks = (await db.execute(select(Task))).scalars().all()
        print(f"\nLeads in DB: {len(leads)}")
        for l in leads:
            print(f"  {l.id}: {l.company_name} ({l.email}) status={l.status.value}")
        print(f"Tasks in DB: {len(tasks)}")
        for t in tasks:
            print(f"  {t.id}: agent={t.agent_name} type={t.task_type} status={t.status}")

asyncio.run(test())
