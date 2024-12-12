from fastapi import FastAPI, File, UploadFile
from dataAnalyzer import clear_graph_directory, analyzer
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
import shutil

app = FastAPI(
    title="API for Data Analyzer App",
    version="1.0",
    decription="query for data analysis services"
)
#Will be needed when deployed
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://dataanalyzer-hkhn.onrender.com"],  # Replace with frontend origin in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

base_directory = os.path.abspath("../public")
graph_directory = os.path.join(base_directory, "graphs")
upload_directory = os.path.join(base_directory, "data")

os.makedirs(graph_directory, exist_ok=True)
os.makedirs(upload_directory, exist_ok=True)

app.mount("/graphs", StaticFiles(directory=graph_directory), name="graphs")

class PromptRequest(BaseModel):
    prompt: str
    file_name: str 

@app.post(path="/analyze")
def run_prompt (prompt: PromptRequest):
    response = analyzer(prompt.prompt, prompt.file_name)
    return {"status": "success", "response": response}

@app.get("/cleanup")
def clean_up ():
    clear_graph_directory()
    return {"status": "success", "response": "cleaned up"}

@app.post('/upload')
async def upload_file(file: UploadFile = File(...)):
    file_path = os.path.join(upload_directory, file.filename)
    with open(file_path, 'wb') as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {"status": "success", "file_name": file.filename}
