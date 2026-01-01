from agent.churn_agent import ChurnRiskAgent
def main():
    # 1. Create sample observation data
    observation = {
        "customer_id": "CUST_001",
        "usage_drop_percentage": 67,
        "support_tickets_last_month": 4
    }

    # 2. Instantiate the agent
    agent = agent = ChurnRiskAgent(agent_name="ChurnRiskAgent",memory_path="memory/churn_agent_memory.json")


    # 3. Observe
    agent.observe(observation)


    # 4. Decide + Act
    result = agent.act()

    # 5. Output result
    print("Agent Decision Output:")
    print(result)


if __name__ == "__main__":
    main()
