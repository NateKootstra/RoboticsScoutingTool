# AUTHENTICATION.PY
# Library used by MAIN.PY to handle user authentication.


import json
import string
import random


# Authenticate a user sign in request.
def authenticate(team = "", username = "", password = ""):
    lowerUser = username.lower()
    try:
        user = open(f"data/{team}/members/{lowerUser}.json")
        realPassword = json.loads(user.read())["password"]
        user.close()
    except:
        return False

    
    if password == realPassword:
        return True
    else:
        return False

def getName(team, username):
    lowerUser = username.lower()
    try:
        user = open(f"data/{team}/members/{lowerUser}.json")
        userData = json.loads(user.read())
        realUsername = userData["username"]
        realName = userData["name"]
        user.close()
        return realName + f" ({realUsername})"
    except:
        return "Name Not Found"

def getAdmin(team, username):
    lowerUser = username.lower()
    try:
        user = open(f"data/{team}/members/{lowerUser}.json")
        userData = json.loads(user.read())
        isAdmin = userData["admin"]
        user.close()
        return isAdmin
    except:
        return False