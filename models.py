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

if __name__ == '__main__':
    data = pickle.load(open('data.pkl','rb'))
    data = data[data.events.notnull()]
    features = ['batter', 'plate_x', 'plate_z']
    model = train(data, features) 
    pickle.dump(model, open('lgbm.pkl','wb'))

