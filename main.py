# MAIN.PY
# The runnable script that runs the web server.


from flask import Flask, render_template, send_from_directory, url_for, make_response, redirect
import os.path
import random
from datetime import datetime

import tbaapi
from authentication import authenticate


app = Flask(__name__)

year = tbaapi.Year(datetime.now().year)

# Public pages:
    
# Home page.
@app.route('/')
def index():
    return render_template('index.html')

# Team rankings.
@app.route('/rankings')
def rankings():
    return render_template('rankings.html')

# Sign-in page.
@app.route('/signin')
def signin():
    return render_template('signin.html')

# Account dashboard.
@app.route('/account')
def account():
    return render_template('account.html')




# API Endpoints:
    

# Sign in the client.
@app.route('/endpoint/signin/<team>/<username>/<password>')
def sign_in(team, username, password):
    if authenticate(team, username, password):
        # Redirect user to the home page.
        response = make_response(redirect("http://127.0.0.1:5001/"))
        # Set cookies.
        response.set_cookie('team', team)
        response.set_cookie('username', username)
        response.set_cookie('password', password)
        # Return response.
        return response
    else:
        return redirect("http://127.0.0.1:5001/signin?failed=true")


# Return the districts for the current year.
@app.route('/endpoint/districts')
def get_districts():
    # Get districts.
    districts = year.get_districts()

    # Remove unnecessary data.
    for district in districts:
        district.pop('year', None)
        district.pop('abbreviation', None)
        district['name'] = district.pop('display_name', None)

    # Return all of the district data.
    return districts
    

# Return the events in a given district.
@app.route('/endpoint/events/district/<district_key>')
def get_events_in_district(district_key):
    # Get events.
    events = tbaapi.District(district_key).get_events()

    # Save the wanted data from 'events' to 'events2'.
    events2 = []
    for event in events:
        newevent = {}
        newevent['name'] = event['name']
        newevent['website'] = event['website']
        newevent['location'] = event['address']
        newevent['gmaps'] = event['gmaps_url']
        newevent['start'] = event['start_date']
        newevent['end'] = event['end_date']
        newevent['event'] = event['event_type']
        newevent['playoff'] = event['playoff_type']

        # Append the simplified event data.
        events2.append(newevent)

    # Return all of the simplified events data.
    return events2


# Return the matches in a given event.
@app.route('/endpoint/matches/event/<event_key>')
def get_matches_in_event(event_key):
    # Get matches.
    matches = tbaapi.Event(event_key).get_matches()

    # Save the wanted data from 'matches' to 'matches2'.
    matches2 = []
    for match in matches:
        newmatch = {}

        newmatch['alliances'] = { 'blue' : match['alliances']['blue']['team_keys'], 'red' : match['alliances']['blue']['team_keys'] }
        newmatch['key'] = match['key']
        newmatch['winner'] = match['winning_alliance']

        # Append the simplified match data.
        matches2.append(newmatch)

    # Return all of the simplified match data.
    return matches2


# Return the teams in a given district. 
@app.route('/endpoint/teams/district/<district_key>')
def get_teams_in_district(district_key):
    # Get teams.
    teams = tbaapi.District(district_key).get_teams()

    # Save the wanted data from 'teams' to 'teams2'.
    teams2 = []
    for team in teams:
        newteam = {}
        newteam['name'] = team['nickname']
        newteam['number'] = team['team_number']
        # Add the website if it's listed.
        if not team['website'] == None:
            newteam['website'] = team['website'].lower().split(' ')[0].removesuffix('/')
        # Properly format the postal codes and make sure the site doesn't crash if the team hasn't listed theirs, merging all of the location data (except address) into 'location'.
        if team['country'] == 'Canada':
            if not team['postal_code'] == None:
                if len(team['postal_code']) == 6:
                    team['postal_code'] = team['postal_code'][:3] + ' ' + team['postal_code'][3:]
                newteam['location'] = team['city'] + ', ' + team['state_prov'] + ', ' + team['country'] + ' | ' + team['postal_code']
            else:
                newteam['location'] = team['city'] + ', ' + team['state_prov'] + ', ' + team['country']
        # Append the simplified team data.
        teams2.append(newteam)

    # Return all of the simplified team data.
    return sorted(teams2, key=lambda d: d['number'])


# Return the rankings in a given district. 
@app.route('/endpoint/rankings/district/<district_key>')
def get_rankings_in_district(district_key):
    # Get rankings and teams.
    rankings = tbaapi.District(district_key).get_rankings()
    teams = get_teams_in_district(district_key)
    # Handle what to do when rankings haven't been posted.
    if rankings == None:
        rankings2 = []
        for team in teams:
            team2 = {'points' : 0, 'rank' : 1}
            team2['team'] = team
            rankings2.append(team2)
        return rankings2

    # Save the wanted data from rankings to rankings2.
    rankings2 = []
    for rank in rankings:
        rank2 = {}
        rank2['points'] = rank['point_total']
        rank2['rank'] = rank['rank']
        # Find the team from the team key.
        team = None;
        for team2 in teams:
            if 'frc' + str(team2['number']) == rank['team_key']:
                team = team2
        # Only add the ranking if the team could be found.
        if not team == None:
            rank2['team'] = team
            rankings2.append(rank2)
    # Return all of the rankings data.
    return rankings2

        
app.jinja_env.globals.update(get_rankings_in_district=get_rankings_in_district)

# Return the teams at a given event.
@app.route('/endpoint/teams/event/<event_key>')
def get_teams_in_event(event_key):
    # Get teams.
    teams = tbaapi.Event(event_key).get_teams()

    # Save the wanted data from 'teams' to 'teams2'.
    teams2 = []
    for team in teams:
        newteam = {}
        newteam['name'] = team['nickname']
        newteam['number'] = team['team_number']
        # Add the website if it's listed.
        if not team['website'] == None:
            newteam['website'] = team['website'].lower().split(' ')[0].removesuffix('/')
        # Properly format the postal codes and make sure the site doesn't crash if the team hasn't listed theirs, merging all of the location data (except address) into 'location'.
        if team['country'] == 'Canada':
            if not team['postal_code'] == None:
                if len(team['postal_code']) == 6:
                    team['postal_code'] = team['postal_code'][:3] + ' ' + team['postal_code'][3:]
                newteam['location'] = team['city'] + ', ' + team['state_prov'] + ', ' + team['country'] + ' | ' + team['postal_code']
            else:
                newteam['location'] = team['city'] + ', ' + team['state_prov'] + ', ' + team['country']
        # Append the simplified team data.
        teams2.append(newteam)

    # Return all of the simplified team data.
    return teams2


# Start the application.
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)