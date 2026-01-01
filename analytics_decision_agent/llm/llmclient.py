import os 
from groq import Groq

class LLMClient:
    def __init__(self, model: str = "llama3-70b-8192"):
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        self.model = model

    def reason(self,prompt:str)-> str:
        response =self.client.chat.completions.create(
            model=self.model,
            messages= [
                {"role":"system","content":"You are a careful business decision analyst."},
                {"role":"user","content":prompt}
            ],temperature=0.2
        )

        return response.choices[0].messages.content


    


