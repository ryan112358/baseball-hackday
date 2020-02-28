#from statcast import statcast
from IPython import embed
import urllib
import pandas as pd
from datetime import datetime as dt
import os
import glob
import pickle

def download_day(day):
    url = "https://baseballsavant.mlb.com/statcast_search/csv?all=true&hfPT=&hfAB=&hfBBT=&hfPR=&hfZ=&stadium=&hfBBL=&hfNewZones=&hfGT=R%7CPO%7CS%7C=&hfSea=&hfSit=&player_type=pitcher&hfOuts=&opponent=&pitcher_throws=&batter_stands=&hfSA=&game_date_gt={}&game_date_lt={}&team=&position=&hfRO=&home_road=&hfFlag=&metric_1=&hfInn=&min_pitches=0&min_results=0&group_by=name&sort_col=pitches&player_event_sort=h_launch_speed&sort_order=desc&min_abs=0&type=details&".format(day,day)
    urllib.request.urlretrieve(url,'data/%s.csv'%day)

def download_range(start, end):
    start = dt.strptime(start,'%Y-%m-%d')
    end = dt.strptime(end,'%Y-%m-%d')
    for day in pd.date_range(start, end):
        day = day.strftime('%Y-%m-%d')
        if not os.path.exists('data/%s.csv'%day):
            try:
                download_day(day)
                print('Processed', day)
            except:
                print('Skipping', day)

def aggregate():
    files = glob.glob('data/*.csv')
    dfs = [pd.read_csv(f) for f in files]
    df = pd.concat(dfs)
    df.to_csv('data.csv', index=False)

def compress():
    df = pd.read_csv('data.csv')

    cat_cols = ['pitch_type','game_date','player_name','batter','pitcher','events','description','zone','des','game_type','stand','p_throws','home_team','away_team','type','hit_location','bb_type','balls','strikes','game_year','on_3b','on_2b','on_1b','outs_when_up','inning','inning_topbot','pitch_name','if_fielding_alignment','of_fielding_alignment', 'launch_speed_angle']

    num_cols = ['release_pos_x','release_pos_z','pfx_x','pfx_z','plate_x','plate_z','hc_x','hc_y','vx0','vy0','vz0','ax','ay','az','sz_top','sz_bot','launch_speed','launch_angle','effective_speed','release_extension','release_pos_y','estimated_ba_using_speedangle','estimated_woba_using_speedangle','woba_value','babip_value','iso_value','at_bat_number','pitch_number','bat_score','fld_score']

    df['on_3b'] = df['on_3b'].notnull()
    df['on_2b'] = df['on_2b'].notnull()
    df['on_1b'] = df['on_1b'].notnull()

    types = { col:'category' for col in cat_cols }
    types.update({ col:np.float16 for col in num_cols })
    df = df[cat_cols + num_cols].astype(types)

    pickle.dump(df, open('data.pkl', 'wb'))

   
download_range('2015-01-01', '2019-12-31') 
print('Data Downloaded...')

aggregate()
print('Data Aggregated')

compress()
print('Data Compressed')

embed()


