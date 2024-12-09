from langcorn import create_service
from dataAnalyzer import clear_graph_directory

app = create_service("dataAnalyzer:analyzer")

@app.post("/clear_graphs")
async def clear_graphs():
    try:
        # Call the function to clear the directory
        clear_graph_directory()
        return {"message": "Graph directory cleared successfully."}, 200
    except Exception as e:
        return {"message": f"Failed to clear graph directory: {str(e)}"}, 500