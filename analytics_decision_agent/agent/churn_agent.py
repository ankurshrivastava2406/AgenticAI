import json
from typing import Dict, Any

from agent.decision_agent import AnalyticsDecisionAgent
from llm.llm_client import LLMClient


class ChurnRiskAgent(AnalyticsDecisionAgent):
    """
    Agent that determines customer churn risk using
    LLM-based reasoning (Groq) with strict guardrails.
    """

    def __init__(self, agent_name: str, memory_path: str = None):
        super().__init__(agent_name=agent_name, memory_path=memory_path)
        self.llm = LLMClient()

    def decide(self) -> Dict[str, Any]:
        """
        Uses Groq LLM ONLY to reason.
        Structure, control flow, and memory are enforced by code.
        """

        if self._observation is None:
            raise ValueError("No observation found. Call observe() before decide().")

        # ---- Current observation ----
        observation = self._observation

        # ---- Read recent memory (last 3 entries only) ----
        recent_history = []
        if self.memory:
            history = self.memory.read_all()
            recent_history = history[-3:]

        # ---- Build prompt ----
        prompt = f"""
You are analyzing customer churn risk.

Guidelines:
- Be conservative.
- Escalate ONLY if repeated high churn risk is evident.
- Do NOT invent data.
- Return ONLY valid JSON.

Current observation:
{json.dumps(observation, indent=2)}

Recent past decisions:
{json.dumps(recent_history, indent=2)}

Return a JSON object with EXACTLY:
- decision_value: one of ["HIGH", "LOW", "ESCALATE"]
- reason: a single short sentence
"""

        # ---- Call Groq LLM ----
        llm_output = self.llm.reason(prompt)

        # ---- Parse and validate response ----
        try:
            decision_payload = json.loads(llm_output)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON from LLM: {llm_output}") from e

        decision_value = decision_payload.get("decision_value")
        reason = decision_payload.get("reason")

        if decision_value not in {"HIGH", "LOW", "ESCALATE"}:
            raise ValueError(f"Invalid decision_value from LLM: {decision_value}")

        # ---- Map decision to action ----
        if decision_value == "ESCALATE":
            recommended_action = "Immediate human intervention"
        elif decision_value == "HIGH":
            recommended_action = "Proactive retention outreach"
        else:
            recommended_action = "No immediate action"

        # ---- Final decision ----
        return {
            "decision_type": "churn_risk",
            "decision_value": decision_value,
            "reason": reason,
            "recommended_action": recommended_action
        }
