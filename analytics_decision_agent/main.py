from agent.churn_agent import ChurnRiskAgent
from agent.revenue_risk_agent import RevenueRiskAgent
from dotenv import load_dotenv
load_dotenv()

def main():
    # 1. Create sample observation data
    observation = {
        "customer_id": "CUST_123",
        "usage_drop_percentage": 74,
        "support_tickets_last_month": 6,
        "revenue_drop_percentage":35
    }

    # 2. Instantiate the agent
    agent = ChurnRiskAgent(agent_name="ChurnRiskAgent",memory_path="memory/churn_agent_memory.json")
    revenue_agent =RevenueRiskAgent(agent_name="RevenueRiskAgent",memory_path ="memory/revenue_agent_memory.json")

    # 3. Observe
    agent.observe(observation)
    revenue_agent.observe(observation)


    # 4. Decide + Act
    result_Churnrisk = agent.act()
    result_revenue_risk = revenue_agent.act()

    # 5. Output result
    print("Agent Decision Output:")
    print(result_Churnrisk)
    print(result_revenue_risk)



if __name__ == "__main__":
    main()
