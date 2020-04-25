import csv
import json

batters = []
pitchers = []

def addPlayer( id, name, position, team, team_short, bats, throws ):
    player = {
        'id': id,
        'name': name,
        'position': position,
        'team': team,
        'team_short': team_short,
        'bats': bats,
        'throws': throws
    }
    if 'p' in position.lower():
        pitchers.append(player)
    else:
        batters.append(player)

def savePlayers():
    with open('data/batters.json', 'w') as batter_file:
        contents = { 'batters': batters }
        json.dump(contents, batter_file, indent=4)

    with open('data/pitchers.json', 'w') as pitcher_file:
        contents = { 'pitchers': pitchers }
        json.dump(contents, pitcher_file, indent=4)

def getPlayerInfo():
    with open('id_name_map.csv', 'r') as player_info:
        player_reader = csv.DictReader(player_info)
        for row in player_reader:
            print('Adding player ' + row['mlb_name'])
            addPlayer(row['mlb_id'], row['mlb_name'], row['mlb_pos'],
                row['mlb_team_long'], row['mlb_team'], row['bats'], row['throws'])

if __name__ == '__main__':
    getPlayerInfo()
    print('Found ' + str(len(batters)) + ' batters')
    print('Found ' + str(len(pitchers)) + ' pitchers')
    savePlayers()
    print('Done')