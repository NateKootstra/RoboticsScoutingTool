# AUTHENTICATION.PY
# Library used by MAIN.PY to manage event data.

import os
import json
import string

# Return a list of events for a team.
def save(team, event, match, scoutedTeam, username, data):
    try:
        os.makedirs(f"data/{team}/data/{event}/{scoutedTeam}/")
    except:
        pass
    file = open(f"data/{team}/data/{event}/{scoutedTeam}/{match}.json", "w")
    data = json.loads(data)
    data["scouter"] = username
    json.dump(data, file)
    file.close()
    if match == "pitscout":
        file = open(f"data/{team}/pitscouting.json", "r")
        try:
            data2 = json.loads(file.read())
            if not event in data2.keys():
                data2[event] = []
        except:
            data2 = {event : []}
        data2[event].append(scoutedTeam)
        file.close()
        file = open(f"data/{team}/pitscouting.json", "w")
        json.dump(data2, file)
        file.close()
    
def lock(team, event, match, lockedTeam):
    file = open(f"data/{team}/lock.json", "r")
    try:
        lock = json.loads(file.read())
    except:
        lock = {}
    file.close()
    file = open(f"data/{team}/lock.json", "w")
    try:
        lock[event].append(f"{match}/{lockedTeam}")
    except:
        lock[event] = [f"{match}/{lockedTeam}"]
    json.dump(lock, file)
    file.close()
    
def getLock(team, event, match):
    file = open(f"data/{team}/lock.json", "r")
    try:
        lock = json.loads(file.read())
        lockedTeams = []
        file.close()
        for lockedTeam in lock[event]:
            if lockedTeam.split("/")[0] == match:
                lockedTeams.append(lockedTeam.split("/")[1])
        return lockedTeams
    except:
        file.close()
        return []
    
def unlock(team, event, match, unlockedTeam):
    file = open(f"data/{team}/lock.json", "r")
    try:
        lock = json.loads(file.read())
        file.close()
        lock[event].remove(match + "/" + unlockedTeam)
        file = open(f"data/{team}/lock.json", "w")
        json.dump(lock, file)
    except:
        file.close()
        
def getTeams(team, event):
    file = open(f"data/{team}/pitscouting.json", "r")
    try:
        pitscouting = json.loads(file.read())
        scoutedTeams = pitscouting[event]
        file.close()
        return scoutedTeams
    except:
        file.close()
        return []