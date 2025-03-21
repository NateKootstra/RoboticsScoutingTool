# MAIN.PY
# The runnable script that runs the web server.


from flask import Flask, render_template, send_from_directory, url_for, make_response, redirect, request
from datetime import datetime

import tbaapi
import datamanager 
from accounts import authenticate, getName, getAdmin, getAccounts, deleteUser, addUser
from events import getEvents, addEvent, removeEvent, updateEvents


domain = 'http://10.126.59.3:5001'
app = Flask(__name__)
year = tbaapi.Year(tbaapi.currentYear)

# Returns info regarding the current account.
def get_account():
    team = request.cookies["team"]
    return { 'team': team, 'teamname': tbaapi.Team(int(team)).get_cached()['nickname'], 'name': getName(team, request.cookies["username"]), 'district': get_district_for_team(int(team))['name']}
app.jinja_env.globals.update(get_account=get_account)

# Returns a list of accounts.
def get_account_list():
    team = request.cookies["team"]
    if authenticate(team, request.cookies["username"], request.cookies["password"]) and getAdmin(team, request.cookies["username"]):
        return getAccounts(team)
    return []
app.jinja_env.globals.update(get_account_list=get_account_list)

# Returns a list of events.
def get_event_list():
    team = request.cookies["team"]
    if authenticate(team, request.cookies["username"], request.cookies["password"]):
        return getEvents(team)
    return []
app.jinja_env.globals.update(get_event_list=get_event_list)

# Returns a list of events.
def get_match_list():
    team = request.cookies["team"]
    if authenticate(team, request.cookies["username"], request.cookies["password"]):
        return tbaapi.Event(request.cookies["event"]).get_matches_cached()
    return []
app.jinja_env.globals.update(get_match_list=get_match_list)

# Returns the alliances of a given team.
def get_alliances_in_match():
    team = request.cookies["team"]
    if authenticate(team, request.cookies["username"], request.cookies["password"]):
        if "practice" in request.cookies["match"]:
            return { "red" : { "team_keys" : ["frc1", "frc2", "frc3"] }, "blue" : { "team_keys" : ["frc4", "frc5", "frc6"] }}
        for match in tbaapi.Event(request.cookies["event"]).get_matches():
            if match["key"].split("_")[1] == request.cookies["match"]:
                return match["alliances"]
    return []
app.jinja_env.globals.update(get_alliances_in_match=get_alliances_in_match)

# Returns a list of events with all associated data.
def get_full_event_list():
    # Get the team and event list.
    team = request.cookies["team"]
    fullEvents = tbaapi.District(tbaapi.Team(int(team)).get_district_cached()["key"]).get_events_cached()
    # Authenticate the user.
    if authenticate(team, request.cookies["username"], request.cookies["password"]):
        realEvents = []
        events = getEvents(team)
        for event in events:
            if event == "practice":
                realEvents.append({"key": "practice"})
            else:
                for fullEvent in fullEvents:
                    if event == fullEvent['key']:
                        realEvents.append(fullEvent)
        return realEvents    
    return []
app.jinja_env.globals.update(get_full_event_list=get_full_event_list)

# Returns all events in the district.
def get_events_in_district():
    team = request.cookies["team"]
    if authenticate(team, request.cookies["username"], request.cookies["password"]) and getAdmin(team, request.cookies["username"]):
        return tbaapi.District(tbaapi.Team(int(team)).get_district_cached()["key"]).get_events()
    return []
app.jinja_env.globals.update(get_events_in_district=get_events_in_district)

# Get the match lock.
def get_lock():
    if authenticate(request.cookies["team"], request.cookies["username"], request.cookies["password"]):
        return datamanager.getLock(request.cookies["team"], request.cookies["event"], request.cookies["match"])
    return []
app.jinja_env.globals.update(get_lock=get_lock)

# Get the teams in a given event.
def get_teams_in_event():
    team = request.cookies["team"]
    if authenticate(team, request.cookies["username"], request.cookies["password"]):
        teams = tbaapi.Event(request.cookies["pitevent"]).get_teams()
        scouted = datamanager.getTeams(team, request.cookies["pitevent"])
        for team in teams:
            if team["key"] in scouted:
                team["scouted"] = True
            else:
                team["scouted"] = False
        return teams
    return []
app.jinja_env.globals.update(get_teams_in_event=get_teams_in_event)


# Public pages:

# Home page.
@app.route('/')
def index():
    return render_template('index.html')

# Team rankings.
@app.route('/rankings')
def rankings():
    if "team" in request.cookies.keys():
        if authenticate(request.cookies["team"], request.cookies["username"], request.cookies["password"]):
            return render_template('rankings.html')
    return redirect(f'{domain}/signin')

# Sign-in page.
@app.route('/signin')
def signin():
    return render_template('signin.html')

# Account dashboard.
@app.route('/account')
def account():
    if "team" in request.cookies.keys():
        if authenticate(request.cookies["team"], request.cookies["username"], request.cookies["password"]):
            if getAdmin(request.cookies["team"], request.cookies["username"]):
                return render_template('account_admin.html')
            return render_template('account.html')
    return redirect(f'{domain}/signin')

    
# Scout menu.
@app.route('/scout')
def scout():
    if "team" in request.cookies.keys():
        if authenticate(request.cookies["team"], request.cookies["username"], request.cookies["password"]):
            if getAdmin(request.cookies["team"], request.cookies["username"]):
                return render_template('scout_admin.html')
            else:
                if "event" in request.cookies.keys():
                    if "match" in request.cookies.keys():
                        if "teamscout" in request.cookies.keys():
                            if "started" in request.cookies.keys():
                                return render_template('scout_active.html')
                            return render_template('scout_waiting.html')
                        return render_template('select_team.html')
                    else:
                        return render_template('select_match.html')
                else:
                    return render_template('select_event.html')
    return redirect(f'{domain}/signin')

# Pitscout menu.
@app.route('/pitscout')
def pitscout():
    if "team" in request.cookies.keys():
        if authenticate(request.cookies["team"], request.cookies["username"], request.cookies["password"]):
            if getAdmin(request.cookies["team"], request.cookies["username"]):
                return render_template('scout_admin.html')
            else:
                if "pitevent" in request.cookies.keys():
                    if "pitteam" in request.cookies.keys():
                        return render_template('pitscout.html')
                    return render_template('pitscout_select_team.html')
                return render_template('pitscout_select_event.html')
    return redirect(f'{domain}/signin')


# Internally facing:

# Sign in the client.
@app.route('/signin/<team>/<username>/<password>')
def sign_in(team, username, password):
    if authenticate(team, username, password):
        # Redirect user to the home page.
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

# Delete user.
@app.route('/deleteuser/<username>')
def delete_user(username):
    response = make_response(redirect(f'{domain}/account'))
    # Delete user only if the user is verified as an admin.
    if authenticate(request.cookies["team"], request.cookies["username"], request.cookies["password"]) and getAdmin(request.cookies["team"], request.cookies["username"]):
        deleteUser(request.cookies["team"], username)
    # Return response.
    return response

# Add user.
@app.route('/adduser/<username>/<name>/<password>')
def add_user(username, name, password):
    response = make_response(redirect(f'{domain}/account'))
    # Add user only if the user is verified as an admin.
    if authenticate(request.cookies["team"], request.cookies["username"], request.cookies["password"]) and getAdmin(request.cookies["team"], request.cookies["username"]):
        addUser(request.cookies["team"], username, name, password)
    # Return response.
    return response

# Add event.
@app.route('/addevent')
def add_event():
    response = make_response(redirect(f'{domain}/account'))
    # Add event only if the user is verified as an admin.
    if authenticate(request.cookies["team"], request.cookies["username"], request.cookies["password"]) and getAdmin(request.cookies["team"], request.cookies["username"]):
        addEvent(request.cookies["team"])
    # Return response.
    return response

# Remove event.
@app.route('/removeevent')
def remove_event():
    response = make_response(redirect(f'{domain}/account'))
    # Remove event only if the user is verified as an admin.
    if authenticate(request.cookies["team"], request.cookies["username"], request.cookies["password"]) and getAdmin(request.cookies["team"], request.cookies["username"]):
        removeEvent(request.cookies["team"])
    # Return response.
    return response

# Remove event.
@app.route('/updateevents/<events>')
def update_events(events):
    response = make_response(redirect(f'{domain}/account'))
    # Remove event only if the user is verified as an admin.
    if authenticate(request.cookies["team"], request.cookies["username"], request.cookies["password"]) and getAdmin(request.cookies["team"], request.cookies["username"]):
        updateEvents(request.cookies["team"], events)
    # Return response.
    return response

# Select the event you wish to scout.
@app.route('/selectevent/<event>')
def select_event(event):
    response = make_response(redirect(f'{domain}/scout'))
    # Select event only if the user is verified as a non-admin user.
    if authenticate(request.cookies["team"], request.cookies["username"], request.cookies["password"]) and not getAdmin(request.cookies["team"], request.cookies["username"]):
        response.set_cookie('event', event)
    # Return response.
    return response

# Select the event you wish to pitscout.
@app.route('/pitselectevent/<event>')
def pit_select_event(event):
    response = make_response(redirect(f'{domain}/pitscout'))
    # Select event only if the user is verified as a non-admin user.
    if authenticate(request.cookies["team"], request.cookies["username"], request.cookies["password"]) and not getAdmin(request.cookies["team"], request.cookies["username"]):
        response.set_cookie('pitevent', event)
    # Return response.
    return response

# Select the match you wish to scout.
@app.route('/selectmatch/<match>')
def select_match(match):
    response = make_response(redirect(f'{domain}/scout'))
    # Select event only if the user is verified as a non-admin user.
    if authenticate(request.cookies["team"], request.cookies["username"], request.cookies["password"]) and not getAdmin(request.cookies["team"], request.cookies["username"]):
        response.set_cookie('match', match)
    # Return response.
    return response

# Select the team you wish to scout.
@app.route('/selectteam/<team>')
def select_team(team):
    response = make_response(redirect(f'{domain}/scout'))
    # Select event only if the user is verified as a non-admin user.
    if authenticate(request.cookies["team"], request.cookies["username"], request.cookies["password"]) and not getAdmin(request.cookies["team"], request.cookies["username"]):
        if not team in get_lock():
            response.set_cookie('teamscout', team)
            datamanager.lock(request.cookies["team"], request.cookies["event"], request.cookies["match"], team)
    # Return response.
    return response

# Select the team you wish to scout.
@app.route('/pitselectteam/<team>')
def pit_select_team(team):
    response = make_response(redirect(f'{domain}/pitscout'))
    # Select event only if the user is verified as a non-admin user.
    if authenticate(request.cookies["team"], request.cookies["username"], request.cookies["password"]) and not getAdmin(request.cookies["team"], request.cookies["username"]):
        if not team in datamanager.getTeams(request.cookies["team"], request.cookies["pitevent"]):
            response.set_cookie('pitteam', team)
    # Return response.
    return response

# Go back in scouting menu.
@app.route('/unscout/<level>')
def unscout(level):
    response = make_response(redirect(f'{domain}/scout'))
    # Authenticate.
    if authenticate(request.cookies["team"], request.cookies["username"], request.cookies["password"]) and not getAdmin(request.cookies["team"], request.cookies["username"]):
        response.delete_cookie(level)
        if level == "teamscout":
            try:
                datamanager.unlock(request.cookies["team"], request.cookies["event"], request.cookies["match"], request.cookies["teamscout"])
            except:
                pass
    # Return response.
    return response

# Go back in pit scouting menu.
@app.route('/pitunscout/<level>')
def pitunscout(level):
    response = make_response(redirect(f'{domain}/pitscout'))
    # Authenticate.
    if authenticate(request.cookies["team"], request.cookies["username"], request.cookies["password"]) and not getAdmin(request.cookies["team"], request.cookies["username"]):
        response.delete_cookie("pit" + level)
    # Return response.
    return response

# Start scouting.
@app.route('/startscout')
def startscout():
    response = make_response(redirect(f'{domain}/scout'))
    # Authenticate.
    if authenticate(request.cookies["team"], request.cookies["username"], request.cookies["password"]) and not getAdmin(request.cookies["team"], request.cookies["username"]):
        response.set_cookie('started', 'true')
    # Return response.
    return response

# Submit data.
@app.route('/submit/<data>')
def submitdata(data):
    response = make_response(redirect(f'{domain}/scout'))
    # Authenticate.
    if authenticate(request.cookies["team"], request.cookies["username"], request.cookies["password"]) and not getAdmin(request.cookies["team"], request.cookies["username"]):
        response.delete_cookie('match')
        response.delete_cookie('teamscout')
        response.delete_cookie('started')
    datamanager.save(request.cookies["team"], request.cookies["event"], request.cookies["match"], request.cookies["teamscout"], request.cookies["username"], data)
    # Return response.
    return response

# Submit data.
@app.route('/pitsubmit/<data>')
def pitsubmitdata(data):
    response = make_response(redirect(f'{domain}/pitscout'))
    # Authenticate.
    if authenticate(request.cookies["team"], request.cookies["username"], request.cookies["password"]) and not getAdmin(request.cookies["team"], request.cookies["username"]):
        response.delete_cookie('pitteam')
    datamanager.save(request.cookies["team"], request.cookies["pitevent"], "pitscout", request.cookies["pitteam"], request.cookies["username"], data)
    # Return response.
    return response


# API Endpoints:


# Return the districts for the current year.
@app.route('/endpoint/districts')
def get_districts():
    # Get districts.
    districts = year.get_districts_cached()

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
    district = tbaapi.Team(int(team_number)).get_district_cached()
    return { 'key' : district['key'], 'name' : district['display_name'] }

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
    return rankings2


app.jinja_env.globals.update(get_rankings_in_district=get_rankings_in_district)

# Return the teams at a given event.
@app.route('/endpoint/teams/event/<event_key>')
def get_teams_in_event_endpoint(event_key):
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
    app.run(debug=True, host='0.0.0.0', port=5001, threaded=True)