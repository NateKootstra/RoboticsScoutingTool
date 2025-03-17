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
        teams = request(f"event/{self.key}/teams").json()
        one = []
        two = []
        three = []
        four = []
        five = []
        for team in teams:
            if len(team["key"]) == 4:
                one.append(team)
            elif len(team["key"]) == 5:
                two.append(team)
            elif len(team["key"]) == 6:
                three.append(team)
            elif len(team["key"]) == 7:
                four.append(team)
            elif len(team["key"]) == 8:
                five.append(team)
        finalTeams = one + two + three + four + five
        return finalTeams

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
        matchesFull = self.get_matches()
        if self.key == "practice":
            matches.append({ "key" : "example1", "name" : "Blue Victory Example", "winner" : "blue", "started" : True })
            matches.append({ "key" : "example2", "name" : "Red Victory Example", "winner" : "red", "started" : True })
            matches.append({ "key" : "example3", "name" : "Started Match Example", "winner" : "none", "started" : True })
            matches.append({ "key" : "divider1", "name" : "---------------------", "winner" : "divider", "started" : True })
            matches.append({ "key" : "practice1", "name" : "Practice Match 1", "winner" : "none", "started" : False })
            matches.append({ "key" : "practice2", "name" : "Practice Match 2", "winner" : "none", "started" : False })
            matches.append({ "key" : "practice3", "name" : "Practice Match 3", "winner" : "none", "started" : False })
            matches.append({ "key" : "practice4", "name" : "Practice Match 4", "winner" : "none", "started" : False })
            matches.append({ "key" : "practice5", "name" : "Practice Match 5", "winner" : "none", "started" : False })
            matches.append({ "key" : "practice6", "name" : "Practice Match 6", "winner" : "none", "started" : False })
            matches.append({ "key" : "practice7", "name" : "Practice Match 7", "winner" : "none", "started" : False })
            matches.append({ "key" : "practice8", "name" : "Practice Match 8", "winner" : "none", "started" : False })
            matches.append({ "key" : "practice9", "name" : "Practice Match 9", "winner" : "none", "started" : False })
            matches.append({ "key" : "practice10", "name" : "Practice Match 10", "winner" : "none", "started" : False })
        else:
            for match in matches:
                match["winner"] = "none"
                match["started"] = False
                for match2 in matchesFull:
                    if match["key"] == match2["key"].split("_")[1]:
                        match["winner"] = match2["winning_alliance"]
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
        self.key = "frc" + str(team_number)
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