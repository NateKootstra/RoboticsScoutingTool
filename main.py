from flask import Flask, render_template, send_from_directory, url_for
import os.path
import random

import tbaapi

app = Flask(__name__)

year = tbaapi.Year(2024)



# Public pages:
    
# Home page.
@app.route("/")
def index():
    return render_template('index.html')




# API Endpoints:
    

# Return the districts for the current year.
@app.route("/endpoint/districts")
def get_districts():
    # Get districts.
    districts = year.get_districts()

    # Remove unnecessary data.
    for district in districts:
        district.pop("year", None)
        district.pop("abbreviation", None)
        district["name"] = district.pop("display_name", None)

    # Return all of the district data.
    return districts
    

# Return the events in a given district.
@app.route("/endpoint/events/district/<district_key>")
def get_events_in_district(district_key):
    # Get events.
    events = tbaapi.District(district_key).get_events()

    # Save the wanted data from 'events' to 'events2'.
    events2 = []
    for event in events:
        newevent = {}
        newevent["name"] = event["name"]
        newevent["website"] = event["website"]
        newevent["location"] = event["address"]
        newevent["gmaps"] = event["gmaps_url"]
        newevent["start"] = event["start_date"]
        newevent["end"] = event["end_date"]
        newevent["event"] = event["event_type"]
        newevent["playoff"] = event["playoff_type"]

        # Append the simplified event data.
        events2.append(newevent)

    # Return all of the simplified events data.
    return events2


# Return the matches in a given event.
@app.route("/endpoint/matches/event/<event_key>")
def get_matches_in_event(event_key):
    # Get matches.
    matches = tbaapi.Event(event_key).get_matches()

    # Save the wanted data from 'matches' to 'matches2'.
    matches2 = []
    for match in matches:
        newmatch = {}

        newmatch["alliances"] = { "blue" : match["alliances"]["blue"]["team_keys"], "red" : match["alliances"]["blue"]["team_keys"] }
        newmatch["key"] = match["key"]
        newmatch["winner"] = match["winning_alliance"]

        # Append the simplified match data.
        matches2.append(newmatch)

    # Return all of the simplified match data.
    return matches2


# Return the teams in a given district. 
@app.route("/endpoint/teams/district/<district_key>")
def get_teams_in_district(district_key):
    # Get teams.
    teams = tbaapi.District(district_key).get_teams()

    # Save the wanted data from 'teams' to 'teams2'.
    teams2 = []
    for team in teams:
        newteam = {}
        newteam["name"] = team["nickname"]
        newteam["number"] = team["team_number"]
        # Add the website if it's listed.
        if not team["website"] == None:
            newteam["website"] = team["website"]
        # Properly format the postal codes and make sure the site doesn't crash if the team hasn't listed theirs, merging all of the location data (except address) into 'location'.
        if team["country"] == "Canada":
            if not team["postal_code"] == None:
                if len(team["postal_code"]) == 6:
                    team["postal_code"] = team["postal_code"][:3] + " " + team["postal_code"][3:]
                newteam["location"] = team["city"] + ", " + team["state_prov"] + ", " + team["country"] + " | " + team["postal_code"]
            else:
                newteam["location"] = team["city"] + ", " + team["state_prov"] + ", " + team["country"]
        # Append the simplified team data.
        teams2.append(newteam)

    # Return all of the simplified team data.
    return teams2


# Return the teams at a given event.
@app.route("/endpoint/teams/event/<event_key>")
def get_teams_in_event(event_key):
    # Get teams.
    teams = tbaapi.Event(event_key).get_teams()

    # Save the wanted data from 'teams' to 'teams2'.
    teams2 = []
    for team in teams:
        newteam = {}
        newteam["name"] = team["nickname"]
        newteam["number"] = team["team_number"]
        # Add the website if it's listed.
        if not team["website"] == None:
            newteam["website"] = team["website"]
        # Properly format the postal codes and make sure the site doesn't crash if the team hasn't listed theirs, merging all of the location data (except address) into 'location'.
        if team["country"] == "Canada":
            if not team["postal_code"] == None:
                if len(team["postal_code"]) == 6:
                    team["postal_code"] = team["postal_code"][:3] + " " + team["postal_code"][3:]
                newteam["location"] = team["city"] + ", " + team["state_prov"] + ", " + team["country"] + " | " + team["postal_code"]
            else:
                newteam["location"] = team["city"] + ", " + team["state_prov"] + ", " + team["country"]
        # Append the simplified team data.
        teams2.append(newteam)

    # Return all of the simplified team data.
    return teams2


# Start the application.
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5001)