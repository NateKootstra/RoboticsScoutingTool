# AUTHENTICATION.PY
# Library used by MAIN.PY to handle user authentication.

import os
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

# Return the proper name of an account.
def getName(team, username):
    lowerUser = username.lower()
    try:
        user = open(f"data/{team}/members/{lowerUser}.json")
        userData = json.loads(user.read())
        realUsername = userData["username"]
        realName = userData["name"]
        user.close()
        return realName + f" - {realUsername}"
    except:
        return "Name Not Found"

# Check if an account is an admin account. 
# NOTE: THIS IS NOT USED FOR ACTUAL VALIDATION AS HAVING THE CLIENT HANDLE WHETHER OR NOT IT'S AN ADMIN IS NOT SECURE.
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

# Return a list of accounts for a team.
def getAccounts(team):
    users = []
    for filename in os.listdir(f"data/{team}/members"):
        user = open(f"data/{team}/members/{filename}")
        userData = json.loads(user.read())
        realUsername = userData["username"]
        realName = userData["name"]
        if not userData['admin']:
            users.append({ "name" : realName + f" - {realUsername}", "password" : userData["password"] })
        user.close()
    return users