from models import *
import hashlib

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


def md5_for_file(f, block_size=2**20):
    md5 = hashlib.md5()
    while True:
        data = f.read(block_size)
        if not data:
            break
        md5.update(data)
    return md5.hexdigest()
