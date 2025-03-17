import json
import os
import sys
import time
from datetime import datetime

import tbaapi

year = tbaapi.currentYear
yearString = str(year)
year = tbaapi.Year(year)

def cache():
    for district in year.get_districts():
        if district["key"] in sys.argv[1]:
            cacheDistrict(district)
            print(district["display_name"])
            for event in tbaapi.District(district['key']).get_events():
                if not "tempclone" in event["key"]:
                    cacheEvent(district, event)
                    print("  -> " + event["name"])
                    for team in tbaapi.Event(event['key']).get_teams():
                        cacheTeamInEvent(district, event, team)
                    for match in tbaapi.Event(event['key']).get_matches():
                        cacheMatch(district, event, match)
            for team in tbaapi.District(district['key']).get_teams():
                cacheTeamInDistrict(district, team)
            
def cacheDistrict(district):
    key = district['key']
    if not os.path.exists(f'tbacache/{yearString}/districts/{key}'):
        os.makedirs(f'tbacache/{yearString}/districts/{key}')
    districtFile = open(f'tbacache/{yearString}/districts/{key}/info.json', 'w')
    json.dump(district, districtFile)
    districtFile.close()
    return

def cacheEvent(district, event):
    districtKey = district['key']
    eventKey = event['key']
    if not os.path.exists(f'tbacache/{yearString}/districts/{districtKey}/events/{eventKey}'):
        os.makedirs(f'tbacache/{yearString}/districts/{districtKey}/events/{eventKey}')
    eventFile = open(f'tbacache/{yearString}/districts/{districtKey}/events/{eventKey}/info.json', 'w')
    json.dump(event, eventFile)
    eventFile.close()
    return

def cacheTeamInDistrict(district, team):
    team['district'] = district
    districtKey = district['key']
    teamKey = team['key']
    if not os.path.exists(f'tbacache/{yearString}/districts/{districtKey}/teams/{teamKey}'):
        os.makedirs(f'tbacache/{yearString}/districts/{districtKey}/teams/{teamKey}')
    teamFile = open(f'tbacache/{yearString}/districts/{districtKey}/teams/{teamKey}/info.json', 'w')
    json.dump(team, teamFile)
    teamFile.close()
    if not os.path.exists(f'tbacache/{yearString}/teams/{teamKey}'):
        os.makedirs(f'tbacache/{yearString}/teams/{teamKey}')
    teamFile = open(f'tbacache/{yearString}/teams/{teamKey}/info.json', 'w')
    json.dump(team, teamFile)
    teamFile.close()
    return

def cacheTeamInEvent(district, event, team):
    team['district'] = district
    districtKey = district['key']
    eventKey = event['key']
    teamKey = team['key']
    if not os.path.exists(f'tbacache/{yearString}/districts/{districtKey}/events/{eventKey}/teams/{teamKey}'):
        os.makedirs(f'tbacache/{yearString}/districts/{districtKey}/events/{eventKey}/teams/{teamKey}')
    teamFile = open(f'tbacache/{yearString}/districts/{districtKey}/events/{eventKey}/teams/{teamKey}/info.json', 'w')
    json.dump(team, teamFile)
    teamFile.close()
    return

def cacheMatch(district, event, match):
    districtKey = district['key']
    eventKey = event['key']
    matchKey = match['key']
    if not os.path.exists(f'tbacache/{yearString}/districts/{districtKey}/events/{eventKey}/matches/{matchKey}'):
        os.makedirs(f'tbacache/{yearString}/districts/{districtKey}/events/{eventKey}/matches/{matchKey}')
    matchFile = open(f'tbacache/{yearString}/districts/{districtKey}/events/{eventKey}/matches/{matchKey}/info.json', 'w')
    json.dump(match, matchFile)
    matchFile.close()
    return
      
while True:  
    cache()
    time.sleep(120)