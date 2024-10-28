from flask import Flask
from DataAnalyzer.dataAnalyzer import analyzer

app = Flask(__name__)

@app.route('/data')
def getRepsonse(): 
    return({
        'value': "Hello"
    })

if __name__ == '__main__':
    app.run(debug=True)