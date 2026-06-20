from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.database import engine, Base
from app.agents.master_cto import MasterCTOAgent
from app.agents.lead_gen import LeadGenAgent
from app.scheduler import start_scheduler, stop_scheduler

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    start_scheduler()
    yield
    stop_scheduler()
    await engine.dispose()

app = FastAPI(title="Cyber Saffron AI OS", lifespan=lifespan)

cto = MasterCTOAgent()
lead_gen = LeadGenAgent()

@app.get("/health")
async def health():
    return {"status": "alive", "agents": list(cto.active_agents.keys())}

@app.post("/orchestrate")
async def orchestrate():
    result = await cto.run({"action": "orchestrate"})
    return {"status": "completed", "result": result}

@app.post("/discover_leads")
async def discover_leads():
    result = await lead_gen.run({"task_type": "daily_scan"})
    return {"status": "completed", "result": result}