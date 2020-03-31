from flask import Flask, render_template, request
import pickle
import pandas as pd
import numpy as np

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/heatmap', methods=["POST"])
def heatmap():
    features = { 'batter' : request.form['batter'] }
    return generate_heatmap(features)

def generate_heatmap(features):
    """
    Generate HeatMap for given features
    :param features: a dictionary of features. e.g., to get heatmap for Mike Trout
        features = { 'batter' : 545361 }

    :return: the heatmap json object
    """
    model = pickle.load(open('../lgbm.pkl','rb'))
    x = pd.DataFrame(np.linspace(-2, 2), columns=['plate_x'])
    y = pd.DataFrame(np.linspace(0, 5), columns=['plate_z'])
    x['key'] = 0
    y['key'] = 0
    df = pd.merge(x, y, on='key').drop(columns='key')
    for col in features:
        df[col] = features[col]
        if type(features[col]) in [str, int, bool]:
            df[col] = df[col].astype('category')

    p = model.predict_proba(df)[:,1]

    json = {}
    json['zone'] = [-0.75, 1.5, 0.75, 3.5]
    json['x'] = list(df.plate_x)
    json['y'] = list(df.plate_z)
    json['heat'] = list(p)
    return json

