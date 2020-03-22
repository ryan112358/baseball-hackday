from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/heatmap', methods=["POST"])
def heatmap():
    # Ryan, this is where you would plug in your function to generate the heatmap
    with open('../heatmap.json', 'r') as file:
        heatmap = file.read()
        return heatmap
