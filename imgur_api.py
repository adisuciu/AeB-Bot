__author__ = 'adrian.suciu'

import urllib.request
import sys
import os
import json
import random
import time
import urllib.parse as urlparse
from common import log
import common
import db
import settings


client_id = 0
client_secret = 0
current_token = {}

def get_token_from_imgur(param):
    json_data = json.dumps(param).encode('utf8')
    global current_token
    try:
        print(json_data)
        req = urllib.request.urlopen("https://api.imgur.com/oauth2/token", data=json_data)
        json_data = json.loads(req.read().decode('utf-8'))
        print(str(json_data))
        current_token = {'access_token': json_data['access_token'], 'refresh_token': json_data['refresh_token'],
                         'timestamp': time.time(), "expires_in": json_data['expires_in'],
                         "account_username": json_data['account_username']}
        return True
    except (urllib.request.URLError, urllib.request.HTTPError):
        print("Token cannot be refreshed due to HTTP Exception: " + (str(sys.exc_info())))
        return False


def get_token_from_pin(pin):
    params = {"client_id": client_id,
              "client_secret": client_secret,
              "grant_type": "pin",
              "pin": pin}

    retval = get_token_from_imgur(params)
    write_token_to_file()
    return retval

def get_token_from_link(link):
    parsed = urlparse.urlparse(link)
    print(urlparse.parse_qs(parsed.query))

    global current_token
    json_data = urlparse.parse_qs(parsed.fragment)

    current_token = {'access_token': json_data['access_token'][0], 'refresh_token': json_data['refresh_token'][0],
                     'timestamp': time.time(), "expires_in": json_data['expires_in'][0],
                     "account_username": json_data['account_username'][0]}
    write_token_to_file()
    return True

def refresh_token():
    params = {"refresh_token": current_token['refresh_token'],
              "client_id": client_id,
              "client_secret": client_secret,
              "grant_type": 'refresh_token'
              }
    retval = get_token_from_imgur(params)
    write_token_to_file()
    return retval


def write_token_to_file():
    output = json.dumps(current_token)
    # with open("token", "w") as f:
    #     f.write(output)
    db.update(settings.imgurtoken_db,"token",output)


def read_token_from_file(filename):
    global current_token
    # with open(filename) as file:
    #     current_token = json.loads(file.read())
    current_token=json.loads(db.select(settings.imgurtoken_db,"token")["token"])


def get_token():
    # we consider token expired if 3/4 of it's expiration time was reached
    if not current_token:
        return False
    token_expiration_timestamp = (int(current_token['timestamp'])) + ((int(current_token['expires_in'])) * 3 / 4)

    if time.time() > token_expiration_timestamp:
        refresh_succesful = refresh_token()
        if refresh_succesful:
            write_token_to_file()
        else:
            return False
    return True


def build_header():
    global current_token
    result = get_token()
    if result:
        # logged in
        return {"Authorization": ("Bearer " + current_token['access_token'])}
    else:
        # not logged in
        return {"Authorization": ("Client-ID " + str(client_id))}


def logged_in():
    return get_token()


def logout():
    try:
        os.remove('token')
        global current_token
        current_token = {}
    except OSError:
        pass


def get_bot_username():
    return current_token['account_username'] if current_token else "not logged in"


def get_bot_imgur_profile():
    return current_token['account_username'] + ".imgur.com/all" if current_token else "not logged in"


def init():
    global client_id, client_secret
    with open("imgurtoken", "r") as f:
        content = f.read().splitlines()

    try:
        client_id = os.environ.get('imgur_id', content[0])
        client_secret = os.environ.get('imgur_secret', content[1])
    except IndexError:
        client_id = os.environ.get('imgur_id', "")
        client_secret = os.environ.get('imgur_secret', "")


    try:
        read_token_from_file("token")
    except FileNotFoundError:
        print("Refresh token not available. Login via bot")


def imgur_pic(request):
    if type(request) == list and len(request) == 2:

        req = urllib.request.Request("https://api.imgur.com/3/gallery/r/" + request[1] + "/top/week",
                                     headers=build_header())
        log("logged in as %s" % get_bot_username())
        response = common.send_http_query(req)  # urllib.request.urlopen(req).read()
        if response:
            json_data = json.loads(response.decode('utf-8'))
            if json_data['data']:  # data is available
                link_id = random.randint(0, len(json_data['data']) - 1)
                retval = (str(json_data['data'][link_id]['title']) + " - "
                          + str(json_data['data'][link_id]['link'] +
                                ("v" if (str(json_data['data'][link_id]['link']).endswith(".gif")) else "")))
                return retval
            else:
                return "images in subreddit '%s' not found in the past day" % request[1]
        else:
            return "internal error. please try again."
    else:
        return "Wrong number of parameters. Usage /getpic [subreddit]"


def login_imgur(request):
    if len(request) == 1:
        return "Go to the following website: \n" \
               "https://api.imgur.com/oauth2/authorize?client_id=%s&response_type=token\n" \
               "use command /login_imgur link" % client_id
    elif len(request) == 2:
        #result = get_token_from_pin(request[1])
        result = get_token_from_link(request[1])

        if result:
            return "Logged in as: " + get_bot_username()
        else:
            return "Login failed. Imgur API might be down, or wrong pin code provided. Please try again"

    else:
        return "Wrong number of parameters. Usage /login_imgur"


# noinspection PyUnusedLocal
def login_status_imgur(request):
    if get_token():
        return "Logged in as: " + get_bot_username() + "\n" + \
               "Full gallery can be viewed at: " + get_bot_imgur_profile()
    else:
        return "Not logged in"


# noinspection PyUnusedLocal
def logout_imgur(request):
    logout()
    return "The bot has successfully logged out of Imgur"
