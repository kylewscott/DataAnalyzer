from fastapi import FastAPI
from dataAnalyzer import clear_graph_directory, analyzer
from pydantic import BaseModel

app = FastAPI(
    title="API for Data Analyzer App",
    version="1.0",
    decription="query for data analysis services"
)

class PromptRequest(BaseModel):
    prompt: str

@app.post(path="/analyze")
def run_prompt (prompt: PromptRequest):
    response = analyzer(prompt.prompt)
    return {"status": "success", "response": response}

@app.get("/cleanup")
def run_prompt ():
    clear_graph_directory()
    return {"status": "success", "response": "cleaned up"}
