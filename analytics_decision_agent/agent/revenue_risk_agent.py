import json
from agent.decision_agent import AnalyticsDecisionAgent
from llm.llmclient import LLMClient


class RevenueRiskAgent(AnalyticsDecisionAgent):
    """
    Agent that evaluates customer revenue risk using LLM reasoning.
    """

    def __init__(self, agent_name: str, memory_path: str):
        super().__init__(agent_name=agent_name, memory_path=memory_path)
        self.llm = LLMClient()

    def decide(self):
        if self._observation is None:
            raise ValueError("No observation found. Call observe() before decide().")

        observation = self._observation

        try:
            recent_history = []

            if self.memory:
                history = self.memory.read_all()
                recent_history = history[-3:]

            prompt = f"""
You are a revenue risk analysis agent.

Rules:
- If revenue drop percentage is greater than 25%, classify risk as HIGH.
- Otherwise classify risk as LOW.
- Be conservative.
- Return ONLY valid JSON.

Current observation:
{json.dumps(observation, indent=2)}

Recent past decisions:
{json.dumps(recent_history, indent=2)}

Return JSON with:
- decision_value: HIGH | LOW
- reason
"""

            llm_output = self.llm.reason(prompt)
            decision_payload = self._extract_json(llm_output)

            decision_value = decision_payload["decision_value"]
            reason = decision_payload["reason"]

            if decision_value not in {"HIGH", "LOW"}:
                raise ValueError("Invalid decision_value from LLM")

        except Exception as e:
            print(
                "[WARN] LLM reasoning failed. Falling back to deterministic logic.",
                f"Error: {str(e)}"
            )

            revenue_drop = observation.get("revenue_drop_percentage", 0)

            if revenue_drop >= 25:
                decision_value = "HIGH"
                reason = "Deterministic fallback: revenue drop exceeds 25%"
            else:
                decision_value = "LOW"
                reason = "Deterministic fallback: revenue drop within acceptable range"

        if decision_value == "HIGH":
            recommended_action = "Immediate human intervention to stabilize revenue"
        else:
            recommended_action = "Monitor revenue trend"

        return {
            "decision_type": "revenue_risk",
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
