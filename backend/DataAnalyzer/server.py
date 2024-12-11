from fastapi import FastAPI
from dataAnalyzer import clear_graph_directory, analyzer
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os

app = FastAPI(
    title="API for Data Analyzer App",
    version="1.0",
    decription="query for data analysis services"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Replace with frontend origin in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

static_directory = os.path.abspath("../../public/graphs")
app.mount("/graphs", StaticFiles(directory=static_directory), name="graphs")

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
