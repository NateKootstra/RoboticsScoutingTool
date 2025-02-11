# TBAAPI.PY
# Library used by MAIN.PY to make requests to The Blue Alliance.


import os
import json
import requests
from datetime import datetime


# NOTE: You need a TheBlueAlliance Read API v3 key to use this. Set the below variable to it was a string, or create a file to store it in.
apikey = open("tbakey.txt").read()

# Set up the basic API info.
apiurl = "https://www.thebluealliance.com/api/v3"
headers = {
    "Content-Type" : "application/json",
    "X-TBA-Auth-Key" : apikey
}

currentYear = datetime.now().year
currentYear = 2024

# General request function.
def request(endpoint):
    return requests.get(url=apiurl+"/"+endpoint, headers=headers)


# Class to retrieve API data for a specific year.
class Year(object):
    def __init__(self, year=currentYear):
        if not type(year) == int:
            raise(TypeError("Year should be an integer."))
        self.year = str(year)


    def get_districts(self):
        return request(f"districts/{self.year}").json()
    
    def get_districts_cached(self):
        districts = []
        for district in os.listdir(f"tbacache/{self.year}/districts"):
            district = open(f"tbacache/{self.year}/districts/{district}/info.json")
            districtInfo = json.loads(district.read())
            districts.append(districtInfo)
            district.close()
        return districts


# Class to retrieve API data for a specific district.
class District(object):
    def __init__(self, key, year=currentYear):
        if not type(key) == str:
            raise(TypeError("District key should be a string."))
        if not type(year) == int:
            raise(TypeError("Year should be an integer."))
        self.key = key
        self.year = year
    

    def get(self):
        return request(f"district/{self.key}/events").json()[0]["district"]
    
    def get_events(self):
        return request(f"district/{self.key}/events").json()
    
    def get_events_cached(self):
        events = []
        for event in os.listdir(f"tbacache/{self.year}/districts/{self.key}/events"):
            event = open(f"tbacache/{self.year}/districts/{self.key}/events/{event}/info.json")
            eventInfo = json.loads(event.read())
            events.append(eventInfo)
            event.close()
        return events

    def get_rankings(self):
        return request(f"district/{self.key}/rankings").json()
    
    def get_teams(self):
        return request(f"district/{self.key}/teams").json()


# Class to retrieve API data for a specific event.
class Event(object):
    def __init__(self, key, year=currentYear):
        if not type(key) == str:
            raise(TypeError("Event key should be a string."))
        if not type(year) == int:
            raise(TypeError("Year should be an integer."))
        self.key = key
        self.year = str(year)

    
    def get_teams(self):
        return request(f"event/{self.key}/teams").json()

    def get_matches(self):
        return request(f"event/{self.key}/matches").json()
    
    def get_matches_cached(self):
        matches = []
        for district in os.listdir(f"tbacache/{self.year}/districts"):
            for event in os.listdir(f"tbacache/{self.year}/districts/{district}/events"):
                eventInfo = open(f"tbacache/{self.year}/districts/{district}/events/{event}/info.json")
                eventInfoJSON = json.loads(eventInfo.read())
                eventInfo.close()
                if eventInfoJSON['key'] == self.key:
                    matches1 = []
                    matches2 = []
                    matches3 = []
                    matches4 = []
                    matches5 = []
                    matches6 = []
                    for match in os.listdir(f"tbacache/{self.year}/districts/{district}/events/{self.key}/matches"):
                        match = match.split('_')
                        if 'qm' in match[1]:
                            if len(match[1]) < 4:
                                matchName = "Qualifier " + match[1].removeprefix('qm')
                                matches1.append({ "key" : match[1], "name" : matchName })
                            else:
                                matchName = "Qualifier " + match[1].removeprefix('qm')
                                matches2.append({ "key" : match[1], "name" : matchName })
                        elif "sf" in match[1]:
                            if len(match[1]) < 6:
                                matchName = "Playoffs " + match[1].removeprefix("sf").split("m")[0]
                                matches3.append({ "key" : match[1], "name" : matchName })
                            else:
                                matchName = "Playoffs " + match[1].removeprefix("sf").split("m")[0]
                                matches4.append({ "key" : match[1], "name" : matchName })
                        elif "f" in match[1]:
                            matchName = "Finals - Match " + match[1].removeprefix("f").split("m")[1]
                            matches5.append({ "key" : match[1], "name" : matchName })
                        else:
                            matches6.append({ "key" : match[1], "name" : matchName })
                    matches1 = sorted(matches1, key=lambda d: d["key"])
                    matches2 = sorted(matches2, key=lambda d: d["key"])
                    matches3 = sorted(matches3, key=lambda d: d["key"])
                    matches4 = sorted(matches4, key=lambda d: d["key"])
                    matches5 = sorted(matches5, key=lambda d: d["key"])
                    matches6 = sorted(matches6, key=lambda d: d["key"])
                    matches = matches1 + matches2 + matches3 + matches4 + matches5 + matches6
        return matches

    def get_alliances(self):
        return request(f"event/{self.key}/alliances").json()


# Class to retrieve API data for a specific team.
class Team(object):
    def __init__(self, team_number, year=currentYear):
        if not type(team_number) == int:
            raise(TypeError("Team number should be an integer.")).sort()
        if not type(year) == int:
            raise(TypeError("Year should be an integer."))
        self.key = key
        self.year = str(year)
    
    def get_cached(self):
        team = open(f"tbacache/{self.year}/teams/{self.key}/info.json")
        teamInfo = json.loads(team.read())
        team.close()
        return teamInfo

    def get_district(self):
        districts = request(f"/team/{self.key}/districts").json()
        return districts[len(districts) - 1]
    
    def get_district_cached(self):
        team = open(f"tbacache/{self.year}/teams/{self.key}/info.json")
        teamInfo = json.loads(team.read())
        team.close()
        return teamInfo['district']