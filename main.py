from flask import Flask, render_template, send_from_directory, url_for
import os.path
import random

import tbaapi

app = Flask(__name__)

year = tbaapi.Year(2025)

# Public pages:
    
# Home page.
@app.route("/")
def index():
    return render_template('index.html')



# API Endpoints:
    
# Return the districts for the current year.
@app.route("/get/districts")
def get_districts():
    districts = year.get_districts()

    # Remove unnecessary data.
    for district in districts:
        district.pop("year", None)
        district.pop("abbreviation", None)
        district["name"] = district.pop("display_name", None)

    return districts

# Return the teams in a given district. 
@app.route("/teams/<district_key>")
def get_teams_in_district(district_key):
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

    # Re
    return teams2


# Start the application.
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5001)

