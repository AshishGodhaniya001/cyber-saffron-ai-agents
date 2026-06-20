import logging
from abc import ABC, abstractmethod
from typing import Dict, Any

logger = logging.getLogger(__name__)

class BaseAgent(ABC):
    def __init__(self, name: str):
        self.name = name
        self.logger = logger

    @abstractmethod
    async def run(self, task: Dict[str, Any]) -> Dict[str, Any]:
        pass

    async def _log_action(self, action: str, details: Dict[str, Any]):
        self.logger.info(f"[{self.name}] {action}: {details}")