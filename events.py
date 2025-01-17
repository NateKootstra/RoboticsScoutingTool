# AUTHENTICATION.PY
# Library used by MAIN.PY to manage event data.

import os
import json
import string

# Return a list of events for a team.
def getEvents(team):
    info = open(f"data/{team}/info.json")
    events = json.loads(info.read())["events"]
    info.close()
    return events

# Add an event slot.
def addEvent(team):
    info = open(f"data/{team}/info.json", 'r')
    newInfo = json.loads(info.read())
    newInfo["events"].append("None")
    info.close()
    info = open(f"data/{team}/info.json", 'w')
    json.dump(newInfo, info)
    info.close()
    return

# Remove an event slot.
def removeEvent(team):
    info = open(f"data/{team}/info.json", 'r')
    newInfo = json.loads(info.read())
    newInfo["events"].pop()
    info.close()
    info = open(f"data/{team}/info.json", 'w')
    json.dump(newInfo, info)
    info.close()
    return

def updateEvents(team, events):
    info = open(f"data/{team}/info.json", 'r')
    newInfo = json.loads(info.read())
    print(events.split(','))
    newInfo["events"] = events.split(',')
    info.close()
    info = open(f"data/{team}/info.json", 'w')
    json.dump(newInfo, info)
    info.close()
    return