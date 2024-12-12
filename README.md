# Data Analyzer
This application is an AI agent that utilizes LangChain and Chat Ollama to analyze data and generate graphs. It features a backend for processing prompts and a React-based frontend for interactive visualization.

In the app you can upload your own CSV file from your computer and ask questions about the data or ask for specifc graphs to be generated regarding the data.

#### Live App: https://data-analyzer-one.vercel.app

## Setup Locally
* Clone repository ```git clone https://github.com/kylewscott/DataAnalyzer.git```

### Requirements
* Python version 3.9 or greater (https://www.python.org/downloads/)
* Node, version 22 preffered (https://nodejs.org/en/download/package-manager)
  
### Backend
* Inside repository navigate to the backend folder and run ```pip install -r requirements.txt```
* In the backend folder run: ```uvicorn server:app --host 'localhost' --port 8000```
* Navaigate to ```http://localhost:8000/docs``` for the API 
  
### Frontend
* Inside repository navigate to the frontend folder and run: ```npm install```
* Inside src/App.js switch the URL variable at the top to the local development URL
* In the frontend folder run ```npm start``` 
* The frontend app can be found at ```http://localhost:3000```

### Notes
* The backend needs to be running in order for the frontend to function correctly
* Requests may take a long time for systems without a GPU

