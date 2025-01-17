import json
import os

import tbaapi

year = tbaapi.Year(2025)

def cache():
    for district in year.get_districts():
        cacheDistrict(district)
        for event in tbaapi.District(district['key']).get_events():
            cacheEvent(district, event)
        for team in tbaapi.District(district['key']).get_teams():
            cacheTeamInDistrict(district, team)
            
def cacheDistrict(district):
    key = district['key']
    if not os.path.exists(f'tbacache/districts/{key}'):
        os.makedirs(f'tbacache/districts/{key}')
    districtFile = open(f'tbacache/districts/{key}/info.json', 'w')
    json.dump(district, districtFile)
    districtFile.close()
    return

def cacheEvent(district, event):
    districtKey = district['key']
    eventKey = event['key']
    if not os.path.exists(f'tbacache/districts/{districtKey}/events/{eventKey}'):
        os.makedirs(f'tbacache/districts/{districtKey}/events/{eventKey}')
    eventFile = open(f'tbacache/districts/{districtKey}/events/{eventKey}/info.json', 'w')
    json.dump(event, eventFile)
    eventFile.close()
    return

def cacheTeamInDistrict(district, team):
    districtKey = district['key']
    teamKey = team['key']
    if not os.path.exists(f'tbacache/districts/{districtKey}/teams/{teamKey}'):
        os.makedirs(f'tbacache/districts/{districtKey}/teams/{teamKey}')
    teamFile = open(f'tbacache/districts/{districtKey}/teams/{teamKey}/info.json', 'w')
    json.dump(team, teamFile)
    teamFile.close()
    return
        
cache()