import asyncio
import logging
from datetime import datetime
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger

from app.agents.master_cto import MasterCTOAgent
from app.agents.lead_gen import LeadGenAgent

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

scheduler = AsyncIOScheduler()
cto = MasterCTOAgent()
lead_gen = LeadGenAgent()
cto.active_agents = {"LeadGen": lead_gen}

async def scheduled_lead_discovery():
    logger.info(f"[SCHEDULER] Lead discovery at {datetime.now()}")
    await lead_gen.run({"task_type": "daily_scan"})

async def scheduled_orchestration():
    logger.info(f"[SCHEDULER] Orchestration at {datetime.now()}")
    await cto.run({"action": "orchestrate"})

def start_scheduler():
    scheduler.add_job(scheduled_lead_discovery, trigger=IntervalTrigger(hours=6), id="lead_discovery")
    scheduler.add_job(scheduled_orchestration, trigger=IntervalTrigger(minutes=15), id="orchestration")
    scheduler.start()
    logger.info("Scheduler started")

def stop_scheduler():
    scheduler.shutdown()