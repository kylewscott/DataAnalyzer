from flask import Flask, request, send_from_directory
from DataAnalyzer.dataAnalyzer import analyzer
import os

app = Flask(__name__)

@app.route('/graphs/<filename>')
def serve_graph(filename):
    return send_from_directory('../public/graphs', filename)

@app.route('/data')
def getResponse(): 
    prompt = request.args.get('param')
    explanation, graph_path = analyzer(prompt)
    
    return ({
        'explanation': explanation,
        'graphUrl': f"/graphs/{os.path.basename(graph_path)}"  
    })

if __name__ == '__main__':
    app.run(debug=True)