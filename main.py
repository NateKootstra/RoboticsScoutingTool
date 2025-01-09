# MAIN.PY
# The runnable script that runs the web server.


from flask import Flask, render_template, send_from_directory, url_for, make_response, redirect, request
import os.path
import random
from datetime import datetime

import tbaapi
from authentication import authenticate, getName, getAdmin


domain = 'http://127.0.0.1:5001'
app = Flask(__name__)
year = tbaapi.Year(datetime.now().year)

# Returns info regarding the current account.
def get_account():
    team = request.cookies["team"]
    return { 'team': team, 'teamname': tbaapi.Team(int(team)).get()['nickname'], 'name': getName(team, request.cookies["username"]), 'district': get_district_for_team(int(team))['name']}

app.jinja_env.globals.update(get_account=get_account)

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

# Admin Account dashboard.
@app.route('/account_admin')
def account_admin():
    return render_template('account_admin.html')


# Internally facing:
    
# Sign in the client.
@app.route('/signin/<team>/<username>/<password>')
def sign_in(team, username, password):
    if authenticate(team, username, password):
        # Redirect user to the home page.
        if getAdmin(team, username):
            response = make_response(redirect(f'{domain}/account_admin'))
        else:
            response = make_response(redirect(f'{domain}/account'))
        # Set cookies.
        response.set_cookie('team', team)
        response.set_cookie('username', username)
        response.set_cookie('password', password)
        # Return response.
        return response
    else:
        # Redirect client if the credentials are invalid.
        return redirect(f'{domain}/signin?failed=true')

# Sign out the client.
@app.route('/signout')
def sign_out():
    response = make_response(redirect(f'{domain}/signin'))
    # Set cookies.
    response.delete_cookie('team')
    response.delete_cookie('username')
    response.delete_cookie('password')
    # Return response.
    return response


# API Endpoints:



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

# Return the district a team is competing in.
@app.route('/endpoint/team_district/<team_number>')
def get_district_for_team(team_number):
    districts = tbaapi.Team(int(team_number)).getDistrict()
    for district in districts:
            if district['year'] == 2025:
                return { 'key' : district['key'],
                         'name' : district['display_name'] }

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
def get_rankings_in_district():
    district_key = get_district_for_team(request.cookies["team"])['key']
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
            rank2['number'] = team['number']
            rankings2.append(rank2)
    # Return all of the rankings data.
    rankings3 = []
    loop = True
    i = 0
    i3 = 1
    while loop:
        try:
            pointCount = rankings2[i]['points']
        except:
            loop = False

        section = []

        loop2 = True
        i2 = 0
        while loop2:
            if rankings2[i + i2]['points'] == pointCount:
                section.append({ 'points' : rankings2[i + i2]['points'], 'rank' : i3, 'team' : rankings2[i + i2]['team'] })
            else:
                loop2 = False
            i2 += 1
            if (i + i2) >= len(rankings2):
                loop2 = False
                loop = False
            
        section = sorted(section, key=lambda d: d['team']['number'])
        for team in section:
            rankings3.append(team)

        i += i2
        i3 += 1


    numbers = []
    for ranking in rankings2:
        numbers.append(ranking['team']['number'])
    for ranking in rankings3:
        if not ranking['team']['number'] in numbers:
            print(ranking)
    return rankings3


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