from app.models import KPIEvent
from app.database import AsyncSessionLocal

async def record_kpi(agent_name: str, metric_name: str, value: float, target: float):
    async with AsyncSessionLocal() as db:
        event = KPIEvent(
            agent_name=agent_name,
            metric_name=metric_name,
            metric_value=value,
            target_value=target
        )
        db.add(event)
        await db.commit()