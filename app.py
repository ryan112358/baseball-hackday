from flask import Flask, render_template, request, jsonify
from flask_cachebuster import CacheBuster
import pickle
import pandas as pd
import numpy as np
from scipy import sparse
import json

from services.player_service import getBatters, getPitchers

app = Flask(__name__)

# Generate a unique hash for static files based on their content. This hash
# will be sent as a query parameter on requests for the file, ensuring that
# the browser always gets the most up to date version
cache_bust_config = { 'extensions': ['.js', '.css'], 'hash_size': 5 }
cache_buster = CacheBuster(config=cache_bust_config)
cache_buster.init_app(app)

@app.route('/')
def index():
    domain = {}
    with open('./data/domain.json', 'r') as domain_file:
        domain = json.load(domain_file)
    
    return render_template('index.html', domain = domain)

@app.route('/heatmap', methods=['POST'])
def heatmap():
    features = { }
    for f in ['pitch_type','batter','pitcher','stand','p_throws','balls','strikes','in_scoring_pos','on_base','home']:
        try:
            features[f] = request.form[f]
        except:
            features[f] = ''

    return generate_heatmap(features)

@app.route('/batters', methods=['GET'])
def batters():
    name_prefix = request.args.get('name_prefix')
    batters = getBatters(name_prefix)
    return jsonify(batters)

@app.route('/pitchers', methods=['GET'])
def pitchers():
    name_prefix = request.args.get('name_prefix')
    pitchers = getPitchers(name_prefix)
    return jsonify(pitchers)

def generate_heatmap(features):
    """
    Generate HeatMap for given features
    :param features: a dictionary of features. e.g., to get heatmap for Mike Trout
        features = { 'batter' : 545361 }

    :return: the heatmap json object
    """
    name_id_map = json.load(open('./name_id_map.json','r'))
    strikezones = json.load(open('./data/strikezone.json','r'))
    if features['batter'] != '':
        features['stand'] = ''
    if features['pitcher'] != '':
        features['p_throws'] = ''

    #model = pickle.load(open('../lgbm.pkl','rb'))
    model = pickle.load(open('./data/nnet.pkl','rb'))
    dtypes = pickle.load(open('./data/dtypes.pkl','rb'))
    x = pd.DataFrame(np.linspace(-2, 2), columns=['plate_x'])
    y = pd.DataFrame(np.linspace(0, 5), columns=['plate_z'])
    x['key'] = 0
    y['key'] = 0
    df = pd.merge(x, y, on='key').drop(columns='key')
    for col in features:
        df[col] = features[col]
        df[col] = df[col]

    b = features['batter']
    features = ['pitch_type', 'batter', 'pitcher', 'stand', 'p_throws', 'balls', 'strikes', 'in_scoring_pos', 'on_base', 'home', 'plate_x', 'plate_z']
    #df['batter'] = df.batter.map(name_id_map)
    #df['pitcher'] = df.pitcher.map(name_id_map)

    X = df.astype(dtypes)[features]
    X1 = X[['plate_x','plate_z']].values
    X2 = pd.get_dummies(X.drop(columns=['plate_x','plate_z']), dummy_na=True, sparse=True)
    X1 = sparse.csr_matrix(X1)
    X2 = sparse.csr_matrix(X2.values)
    XX = sparse.hstack([X1, X2], format='csr')
    #print(XX.shape)

    #p = model.predict_proba(df)[:,1]
    v = np.array([0,1,2,3,4])
    p = model.predict_proba(XX) @ v

    z = strikezones[b] if b in strikezones else [1.5, 3.5]
    ans = {}
    ans['zone'] = [-0.75, z[0], 0.75, z[1]]
    ans['x'] = list(df.plate_x)
    ans['y'] = list(df.plate_z)
    ans['heat'] = list(p)
    return ans

if __name__ == '__main__':
    app.run()
