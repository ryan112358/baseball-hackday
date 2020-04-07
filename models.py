import pickle
from lightgbm import LGBMClassifier
from sklearn.neural_network import MLPClassifier
import pandas as pd
import numpy as np
from scipy import sparse

def train(data, features):
    X = data[features]
    Y = X.copy()
    for col in Y.columns:
        if not col in ['plate_x','plate_z']:
            idx = np.random.rand(Y.shape[0]) < 0.5
            Y.loc[idx, col] = np.nan   
    X = pd.concat([X,Y]).reset_index(drop=True)

    y = data['events'].isin(['single','double','triple','home_run'])
    y = pd.concat([y,y]).reset_index(drop=True)

    #model = LGBMClassifier()
    #model.fit(X, y)

    X1 = X[['plate_x','plate_z']].values
    X2 = pd.get_dummies(X.drop(columns=['plate_x','plate_z']), dummy_na=True, sparse=True)
    XX = sparse.hstack([X1, X2], format='csr')
    print(XX.shape)

    model = MLPClassifier(hidden_layer_sizes=(50,50,50), activation='tanh', verbose=True)
    model.fit(XX, y.values)

    return model

def clean(data):
    data = data[data.events.notnull()].dropna(subset=['plate_x','plate_z'])
    
    data['batter'] = data.batter.astype(str)
    data['pitcher'] = data.pitcher.astype(str)

    batcount = data.batter.value_counts()
    lowfreq = batcount[batcount < 500].index
    data.batter.replace(lowfreq, '-1', inplace=True)

    pitcount = data.pitcher.value_counts()
    lowfreq = pitcount[pitcount < 500].index
    data.pitcher.replace(lowfreq, '-1', inplace=True)

    pitch_types = ['FF', 'SL', 'FT', 'CH', 'SI', 'CU', 'FC', 'KC', 'FS', 'KN',
                  'IN', 'EP', 'FO', 'PO', 'SC', 'UN', 'FA']
    data = data[data.pitch_type.isin(pitch_types)]
    data['in_scoring_pos'] = data.on_3b.astype(bool) | data.on_2b.astype(bool)
    data['on_base'] = data.in_scoring_pos | data.on_1b.astype(bool)
    data['home'] = data.inning_topbot == 'Bot'

    for col,dtype in zip(data.columns, data.dtypes):
        if dtype.name in ['int', 'bool', 'str', 'object', 'category']:
            data[col] = data[col].astype(str).astype('category')

    return data

if __name__ == '__main__':
    data = pickle.load(open('data.pkl','rb'))
    data = clean(data)
    features = ['pitch_type', 'batter', 'pitcher', 'stand', 'p_throws', 'balls', 'strikes', 'in_scoring_pos', 'on_base', 'home', 'plate_x', 'plate_z']
    model = train(data, features) 
    pickle.dump(data[features].dtypes, open('dtypes.pkl','wb'))
    pickle.dump(model, open('nnet.pkl','wb'))

