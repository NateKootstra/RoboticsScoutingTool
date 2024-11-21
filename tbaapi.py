# TBAAPI.PY
# Library used by MAIN.PY to make requests to The Blue Alliance.


import requests


# NOTE: You need a TheBlueAlliance Read API v3 key to use this. Set the below variable to it was a string, or create a file to store it in.
apikey = open("tbakey.txt").read()

# Set up the basic API info.
apiurl = "https://www.thebluealliance.com/api/v3"
headers = {
    "Content-Type" : "application/json",
    "X-TBA-Auth-Key" : apikey
}



# General request function.
def request(endpoint):
    return requests.get(url=apiurl+"/"+endpoint, headers=headers)


# Class to retrieve API data for a specific year.
class Year(object):
    def __init__(self, year):
        if not type(year) == int:
            raise(TypeError("Year should be an integer."))
        self.year = str(year)


    def get_districts(self):
        return request(f"districts/{self.year}").json()

    def get_events(self):
        return request(f"events/{self.year}").json()


# Class to retrieve API data for a specific district.
class District(object):
    def __init__(self, key):
        if not type(key) == str:
            raise(TypeError("District key should be a string."))
        self.key = key
    

    def get(self):
        return request(f"district/{self.key}/events").json()[0]["district"]

    def get_events(self):
        return request(f"district/{self.key}/events").json()

    def get_rankings(self):
        return request(f"district/{self.key}/rankings").json()
    
    def get_teams(self):
        return request(f"district/{self.key}/teams").json()


# Class to retrieve API data for a specific event.
class Event(object):
    def __init__(self, key):
        if not type(key) == str:
            raise(TypeError("Event key should be a string."))
        self.key = key

    
    def get_teams(self):
        return request(f"event/{self.key}/teams").json()

    def get_matches(self):
        return request(f"event/{self.key}/matches").json()

    def get_alliances(self):
        return request(f"event/{self.key}/alliances").json()


# Class to retrieve API data for a specific team.
class Team(object):
    def __init__(self, team_number):
        if not type(team_number) == int:
            raise(TypeError("Team number should be an integer."))
        self.key = "frc" + str(team_number)
    

    def get(self):
        return request(f"team/{self.key}").json()