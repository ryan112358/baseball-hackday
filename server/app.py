from flask import Flask, render_template, request
import pickle
import pandas as pd
import numpy as np
from scipy import sparse
import json

app = Flask(__name__)

@app.route('/')
def index():
    with open('../domain.json', 'r') as domain_file:
        domain = json.load(domain_file)
        return render_template('index.html', domain = domain)

@app.route('/heatmap', methods=["POST"])
def heatmap():
    features = { }
    for f in ['pitch_type','batter','pitcher','stand','p_throws','balls','strikes','in_scoring_pos','on_base','home']:
        try:
            features[f] = request.form[f]
        except:
            features[f] = '' 

    print(features)

    return generate_heatmap(features)

def generate_heatmap(features):
    """
    Generate HeatMap for given features
    :param features: a dictionary of features. e.g., to get heatmap for Mike Trout
        features = { 'batter' : 545361 }

    :return: the heatmap json object
    """

    #model = pickle.load(open('../lgbm.pkl','rb'))
    model = pickle.load(open('../nnet.pkl','rb'))
    dtypes = pickle.load(open('../dtypes.pkl','rb'))
    x = pd.DataFrame(np.linspace(-2, 2), columns=['plate_x'])
    y = pd.DataFrame(np.linspace(0, 5), columns=['plate_z'])
    x['key'] = 0
    y['key'] = 0
    df = pd.merge(x, y, on='key').drop(columns='key')
    for col in features:
        df[col] = features[col]
        df[col] = df[col]

    features = ['pitch_type', 'batter', 'pitcher', 'stand', 'p_throws', 'balls', 'strikes', 'in_scoring_pos', 'on_base', 'home', 'plate_x', 'plate_z']
    X = df.astype(dtypes)[features]
    X1 = X[['plate_x','plate_z']].values
    X2 = pd.get_dummies(X.drop(columns=['plate_x','plate_z']), dummy_na=True, sparse=True)
    XX = sparse.hstack([X1, X2], format='csr')
    #print(XX.shape)

    #p = model.predict_proba(df)[:,1]
    p = model.predict_proba(XX)[:,1]

    json = {}
    json['zone'] = [-0.75, 1.5, 0.75, 3.5]
    json['x'] = list(df.plate_x)
    json['y'] = list(df.plate_z)
    json['heat'] = list(p)
    return json

if __name__ == '__main__':
    features = ['pitch_type', 'batter', 'pitcher', 'stand', 'p_throws', 'balls', 'strikes', 'in_scoring_pos', 'on_base', 'home']
    entry = { f : '' for f in features }
    entry['batter'] = '605141'
    #ans = generate_heatmap(entry)
