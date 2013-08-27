from models import *

def email_exists(email):
    try:
        ThoughtbubbleUser.objects.get(email=email)
        exists = True
    except:
        exists = False
    return exists

def username_exists(username):
    try:
        ThoughtbubbleUser.objects.get(username=username)
        exists = True
    except:
        exists = False
    return exists
