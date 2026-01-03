from typing import Dict, Any
from datetime import datetime
from memory.memorystore import AppendOnlyMemory

class AnalyticsDecisionAgent:
    def __init__(self,agent_name: str,memory_path: str):
        self.agent_name =agent_name
        self.created_at = datetime.utcnow()
        self._observation =None 
        self.memory = (AppendOnlyMemory(memory_path) if memory_path else None)

        

    def observe(self, data:Dict[str,Any])-> None:
        self._observation =data
    

    def decide(self) -> Dict[str,Any]:
        raise NotImplementedError("Decision logic not implemented")

    def act(self) -> Dict[str, Any]:
        decision = self.decide()
        decision["agent"] = self.agent_name
        decision["timestamp"] = datetime.utcnow().isoformat()
        self.memory.append(self._observation, decision)
        
        return decision



