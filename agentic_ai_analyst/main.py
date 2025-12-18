from agent.agent import Coreagent

agent = Coreagent()
state = agent.run("Why did churn increase in APAC?")

print("Question:", state.question)
print("Plan:", state.plan)
print("Results:", state.results)
print("Notes:", state.notes)
print("Confidence:", round(state.confidence, 2))
