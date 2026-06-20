import asyncio
import json
from typing import Dict, Any
from datetime import datetime
from sqlalchemy import select, update
from app.agents.base import BaseAgent
from app.agents.lead_gen import LeadGenAgent
from app.agents.sales_agent import SalesAgent
from app.models import Task
from app.database import AsyncSessionLocal
import google.generativeai as genai
from app.config import settings

genai.configure(api_key=settings.gemini_api_key)
gemini_model = genai.GenerativeModel(settings.gemini_model)

class MasterCTOAgent(BaseAgent):
    def __init__(self):
        super().__init__("MasterCTO")
        self.active_agents = {
            "LeadGen": LeadGenAgent(),
            "Sales": SalesAgent()
        }
        self.logger.info(f"Loaded agents: {list(self.active_agents.keys())}")

    async def run(self, task: Dict[str, Any]) -> Dict[str, Any]:
        action = task.get("action", "orchestrate")
        if action == "orchestrate":
            return await self._orchestrate()
        elif action == "reconfigure_agent":
            return await self._reconfigure_agent(task.get("agent_name"))
        elif action == "escalate_to_owner":
            return await self._escalate(task.get("message"))
        return {"status": "unknown_action"}

    async def _orchestrate(self) -> Dict[str, Any]:
        async with AsyncSessionLocal() as db:
            pending = await db.execute(
                select(Task).where(Task.status == "pending").order_by(Task.priority.desc()).limit(20)
            )
            tasks = pending.scalars().all()
            assigned = 0
            for t in tasks:
                agent = self.active_agents.get(t.agent_name)
                if agent:
                    asyncio.create_task(self._execute_task(agent, t))
                    assigned += 1
            return {"status": "orchestrated", "tasks_assigned": assigned}

    async def _execute_task(self, agent: BaseAgent, task: Task):
        async with AsyncSessionLocal() as db:
            try:
                await db.execute(update(Task).where(Task.id == task.id).values(status="running"))
                await db.commit()
            except Exception as e:
                self.logger.exception(f"Database error setting task {task.id} to running: {e}")
                return
            try:
                payload = json.loads(task.payload) if task.payload else {}
                result = await agent.run({"task_type": task.task_type, "payload": payload})
                await db.execute(
                    update(Task).where(Task.id == task.id).values(
                        status="done",
                        result=json.dumps(result),
                        completed_at=datetime.utcnow()
                    )
                )
            except Exception as e:
                self.logger.exception(f"Task {task.id} failed: {e}")
                await db.execute(
                    update(Task).where(Task.id == task.id).values(
                        status="failed",
                        result=str(e)
                    )
                )
            await db.commit()

    async def _reconfigure_agent(self, agent_name: str) -> Dict[str, Any]:
        prompt = f"You are the Master CTO Agent. Agent '{agent_name}' is underperforming. Suggest 3 actionable improvements in JSON format: {{\"recommendations\": [\"improve X by doing Y\", ...]}}"
        response = await asyncio.to_thread(gemini_model.generate_content, prompt)
        text = response.text.strip()
        try:
            if "```json" in text:
                text = text.split("```json")[1].split("```")[0]
            suggestions = json.loads(text)
        except:
            suggestions = {"recommendations": ["Check logs", "Reduce load", "Review credentials"]}
        return {"status": "reconfigured", "agent": agent_name, "suggestions": suggestions}

    async def _escalate(self, message: str) -> Dict[str, Any]:
        self.logger.error(f"ESCALATION: {message}")
        return {"status": "escalated", "message": message}