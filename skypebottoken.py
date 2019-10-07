import os
from common import log

port = os.environ.get('PORT', 8000)

app_id = ""
app_secret = ""

try:
    with open("skypetoken", "r") as f:
        content = f.read().splitlines()

    try:
        app_id = content[0]
        app_secret = content[1]
    except:
        log("skypetoken Empty")
except:
    log("skypetoken not found getting tokens from envvar")

app_id = os.environ.get('app_id', app_id)
app_secret = os.environ.get('app_secret', app_secret)
