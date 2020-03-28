import pickle
from lightgbm import LGBMClassifier
import pandas as pd
import numpy as np

def train(data, features):
    X = data[['plate_x', 'plate_z', 'batter']]
    y = data['events'].isin(['single','double','triple','home_run'])

    model = LGBMClassifier()
    model.fit(X, y)
    return model

def generate_heatmap(features):
    """
    Generate HeatMap for given features
    :param features: a dictionary of features. e.g., to get heatmap for Mike Trout
        features = { 'batter' : 545361 }

    :return: the heatmap json object
    """
    model = pickle.load(open('lgbm.pkl','rb'))
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
    
if __name__ == '__main__':
    data = pickle.load(open('data.pkl','rb'))
    data = data[data.events.notnull()]
    features = ['batter', 'plate_x', 'plate_z']
    model = train(data, features) 
    pickle.dump(model, open('lgbm.pkl','wb'))

