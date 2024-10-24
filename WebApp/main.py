from flask import Flask, request, render_template
from DataAnalyzer.dataAnalyzer import analyzer

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    graph_path = None  # Initialize the path for the graph

    if request.method == "POST":
        prompt = request.form.get("prompt", "")
        analyzer(prompt)  # Call the analyzer function to generate the graph
        graph_path = "static/graphs/generated_graph.png"  # Path to the generated graph

    return render_template('result.html', graph_path=graph_path) 

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)