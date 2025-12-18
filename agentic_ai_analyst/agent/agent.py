from tools.analytics_tool import churn_rate, revenue_by_segment
from tools.data_query_tool import load_table,query_table
from tools.metadata_tool import get_metadata
from agent.memory import log_run


class Agentstate:
    def __init__(self,question:str):
        self.question =question
        self.plan= []
        self.results ={}
        self.confidence=1.0
        self.notes=[]

    
class Coreagent:
    def __init__(self):
        pass
    
    def interpret_goal(self,state:Agentstate):
        question =state.question.lower()


        if "churn" in question:
            state.plan.append("analyze_churn")

        if "APAC" in question: 
            state.plan.append("filter_region_apac")
    
    def execute_plan(self,state:Agentstate):

        customers = query_table("customers")
        churn=query_table("churn_events")
        if "filter_region_apac" in state.plan:
            customers = customers[customers["region"] == "APAC"]
        
        if "analyze_churn" in state.plan:
            rate = churn_rate(customers, churn)
            state.results["churn_rate"] = rate

    def reflect(self,state:Agentstate):
        if "churn_rate" in state.results:
            rate=state.results["churn_rate"]

            if rate > 0.5:
                state.notes.append("Churn has been detected and is significant")
            else:
                state.notes.append("Churn has not been detected and is not significant")
            
            state.confidence *=0.9


    def run(self,question:str):
        state =Agentstate(question)
        self.interpret_goal(state)
        self.execute_plan(state)
        self.reflect(state)
        log_run(state)
        return state 



    













