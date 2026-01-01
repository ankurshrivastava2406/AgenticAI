import json
from pathlib import Path 
from datetime import datetime 


class AppendOnlyMemory:
    def __init__(self, file_path: str):
        self.path = Path(file_path)
        self.path.parent.mkdir(parents=True, exist_ok=True)

        if not self.path.exists():
            self.path.write_text(json.dumps([], indent=2))
    
    def append(self, observation: dict, decision: dict):
        memory = json.loads(self.path.read_text())

        memory.append({
            "timestamp": datetime.utcnow().isoformat(),
            "observation": observation,
            "decision": decision
        })

        self.path.write_text(json.dumps(memory, indent=2))
    
    def read_all(self):
        return json.loads(self.path.read_text())





