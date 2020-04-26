import json

def getPlayers(type = None):
    players = {}
    with open('../data/players.json', 'r') as players_file:
        players = json.load(players_file)
        
    if type is not None:
        return players.get(type, [])
    
    return players

def getBatters(name_prefix = None):
    batters = getPlayers('batters')
    if name_prefix is not None:
        return findByNamePrefix(batters, name_prefix)

    return batters

def getPitchers(name_prefix = None):
    pitchers = getPlayers('pitchers')
    if name_prefix is not None:
        return findByNamePrefix(pitchers, name_prefix)

    return pitchers

def findByNamePrefix(players, name_prefix):
    return filter(lambda player: name_prefix.lower() in player.name.lower(), players)
