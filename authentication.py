# AUTHENTICATION.PY
# Library used by MAIN.PY to handle user authentication.


import json
import string
import random


# Authenticate a user sign in request.
def authenticate(team = "", username = "", password = ""):
    try:
        user = open(f"data/{team}/members/{username}.json")
        realPassword = json.loads(user.read())["password"]
        user.close()
    except:
        return False

    
    if password == realPassword:
        return True
    else:
        return False