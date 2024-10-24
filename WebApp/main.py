from flask import Flask, request, render_template
from DataAnalyzer.dataAnalyzer import analyzer

app = Flask(__name__)

@app.route("/")
def index():
    return(
        """<form action="/analyze" method="get">
                <input type="text" name="prompt" />
                <input type="submit" value="ask" />
            </form>"""
    )

@app.route("/analyze")
def analyze():
    prompt = request.args.get("prompt", "")
    analyzer(prompt)
    graph_path = "static/graphs/generated_graph.png"
    return render_template('result.html', graph_path=graph_path)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)