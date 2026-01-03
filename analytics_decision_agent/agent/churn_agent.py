import json
from typing import Dict, Any

from agent.decision_agent import AnalyticsDecisionAgent
from llm.llmclient import LLMClient


class ChurnRiskAgent(AnalyticsDecisionAgent):
    """
    Agent that determines customer churn risk using
    LLM-based reasoning (Groq) with strict guardrails.
    """

    def __init__(self, agent_name: str, memory_path: str = None):
        super().__init__(agent_name=agent_name, memory_path=memory_path)
        self.llm = LLMClient()

    def decide(self):
        if self._observation is None:
            raise ValueError("No observation found. Call observe() before decide().")

        observation = self._observation

    # -----------------------------
    # 1. Attempt LLM-based reasoning
    # -----------------------------
        try:
            recent_history = []
            if self.memory:
                history = self.memory.read_all()
                recent_history = history[-3:]

            prompt = f"""
    You are analyzing customer churn risk.

    Rules:
    - Be conservative
    - Escalate only if repeated high risk is evident
    - Return ONLY valid JSON

    Current observation:
    {json.dumps(observation, indent=2)}

    Recent past decisions:
    {json.dumps(recent_history, indent=2)}

    Return JSON with:
    - decision_value: HIGH | LOW | ESCALATE
    - reason
    """

            llm_output = self.llm.reason(prompt)
            decision_payload = self._extract_json(llm_output)

            decision_value = decision_payload["decision_value"]
            reason = decision_payload["reason"]

            if decision_value not in {"HIGH", "LOW", "ESCALATE"}:
                raise ValueError("Invalid decision_value from LLM")

        # -----------------------------
        # 2. Deterministic fallback
        # -----------------------------
        except Exception as e:

            print("[WARN] LLM reasoning failed. Falling back to deterministic logic.",f"Error: {str(e)}")
            usage_drop = observation.get("usage_drop_percentage", 0)
            tickets = observation.get("support_tickets_last_month", 0)

            if usage_drop >= 30 or tickets >= 3:
                decision_value = "HIGH"
                reason = "Deterministic fallback: usage drop or high support tickets"
            else:
                decision_value = "LOW"
                reason = "Deterministic fallback: stable usage and low tickets"

        # -----------------------------
        # 3. Map decision → action
        # -----------------------------
        if decision_value == "ESCALATE":
            recommended_action = "Immediate human intervention"
        elif decision_value == "HIGH":
            recommended_action = "Proactive retention outreach"
        else:
            recommended_action = "No immediate action"

        return {
            "decision_type": "churn_risk",
            "decision_value": decision_value,
            "reason": reason,
            "recommended_action": recommended_action
        }

    def _extract_json(self, text: str) -> dict:
        """
        Extract the first JSON object found in an LLM response.
        Handles markdown fences and extra text.
        """
        start = text.find("{")
        end = text.rfind("}")

        if start == -1 or end == -1 or end <= start:
            raise ValueError("No JSON object found in LLM output")

        json_str = text[start:end + 1]
        return json.loads(json_str)
