import requests

apiurl = "https://www.thebluealliance.com/api/v3"
apikey = open("tbakey.txt").read()

headers = {
    "Content-Type" : "application/json",
    "X-TBA-Auth-Key" : apikey
}




def request(endpoint):
    return requests.get(url=apiurl+"/"+endpoint, headers=headers)


class Year(object):
    def __init__(self, year):
        if not type(year) == int:
            raise(TypeError("Year should be an integer."))
        self.year = str(year)


    def get_districts(self):
        return request(f"districts/{self.year}").json()

    def get_events(self):
        return request(f"events/{self.year}").json()


class District(object):
    def __init__(self, key):
        if not type(key) == str:
            raise(TypeError("District key should be a string."))
        self.key = key
    

    def get(self):
        return request(f"district/{self.key}").json()

    def get_events(self):
        return request(f"district/{self.key}/events").json()

    def get_rankings(self):
        return request(f"district/{self.key}/rankings").json()
    
    def get_teams(self):
        return request(f"district/{self.key}/teams").json()


class Event(object):
    def __init__(self, key, name):
        if not type(key) == str:
            raise(TypeError("Event key should be a string."))
        self.key = key
        self.name = name

    
    def get_teams(self):
        return request(f"event/{self.key}/teams").json()

    def get_matches(self):
        return request(f"event/{self.key}/matches").json()

    def get_alliances(self):
        return request(f"event/{self.key}/alliances").json()


class Team(object):
    def __init__(self, team_number):
        if not type(team_number) == int:
            raise(TypeError("Team number should be an integer."))
        self.key = "frc" + str(team_number)
    

    def get(self):
        return request(f"team/{self.key}").json()