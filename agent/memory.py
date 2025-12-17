import json
from pathlib import Path
from datetime import datetime

MEMORY_FILE = Path("memory/agent_memory.json")

def load_memory():
    if not MEMORY_FILE.exists():
        return {"past_runs": []}
    return json.loads(MEMORY_FILE.read_text())

def save_memory(memory):
    MEMORY_FILE.write_text(json.dumps(memory, indent=2))

def log_run(state):
    memory = load_memory()
    memory["past_runs"].append({
        "question": state.question,
        "plan": state.plan,
        "results": state.results,
        "confidence": state.confidence,
        "timestamp": datetime.utcnow().isoformat()
    })
    save_memory(memory)
