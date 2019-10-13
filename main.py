import skype_chatbot
import json
from common import log
import shlex
import random
import settings
import imgur_api
import links
import commands
import skypebottoken
import os

import bleach
import db
from bs4 import BeautifulSoup

from flask import Flask, request

app = Flask(__name__)
last_sender = ""
nsfw_tag = False
bot_name=""

bot = skype_chatbot.SkypeBot(skypebottoken.app_id, skypebottoken.app_secret)

switcher = {
    "": commands.dummy,
    "about": commands.about,
    "help": commands.help,
    "uptime": commands.uptime,
    "quote": commands.quote,
    "remember": commands.remember_link,
    "forget": commands.forget_link,
    "recall": commands.recall_link,
    "search": commands.search_link,
    "getpic": commands.imgur_pic,
    "login_imgur": commands.login_imgur,
    "logout_imgur": commands.logout_imgur,
    "imgur_status": commands.login_status_imgur,
    "memegen": commands.meme_gen,
    "search_meme": commands.search_memes,
    "nuke": commands.nuke_db,
}


def remove_ahref(cmd):
    return cmd


def convert_quot(text):
    soup = BeautifulSoup(text).text

    return str(soup)


def convert_skype_format(cmd):
    cmd = remove_ahref(cmd)
    cmd = convert_quot(cmd)
    return cmd


def parse_message(text):
    text = convert_skype_format(text)

    global nsfw_tag

    if not text.startswith(settings.bot_prefix):
        return
    text = text[len(settings.bot_prefix):]  # remove bot_prefix
    cmd = shlex.split(text)
    if cmd[0]=="AeB-Bot":
        cmd.pop(0)
    log("Request - " + str(cmd))
    response = switcher[cmd[0]](cmd) if cmd[0] in switcher else False
    log("Response - " + str(response))
    return response


@app.route('/api/messages', methods=['POST', 'GET'])
def webhook():
    if request.method == 'POST':
        try:
            global last_sender  # hack
            global bot_name
            data = json.loads(request.data)
            bot_id = data['recipient']['id']
            bot_name = data['recipient']['name']
            recipient = data['from']
            service = data['serviceUrl']
            last_sender = data['conversation']['id']
            text = data['text']

            response = parse_message(text)
            text_format = 'plain'

            global nsfw_tag

            bot.send_message(bot_id, bot_name, recipient, service, last_sender, response, text_format)
            if response.endswith(".jpg") and not nsfw_tag:
                bot.send_media(bot_id, bot_name, recipient, service, last_sender, "image/jpg", response)
            if response.endswith(".gif") and not nsfw_tag:
                bot.send_media(bot_id, bot_name, recipient, service, last_sender, "image/gif", response)

            print(data)

        except Exception as e:
            print(e)

    return 'Code: 200'


@app.route('/', methods=['POST', 'GET'])
def webhook_default():
    if request.method == 'POST':
        try:
            data = json.loads(request.data)
            print(data)
        except Exception as e:
            print(e)
    return 'Welcome to AeBBot - Code: 200'


if __name__ == '__main__':
    db.create_if_doesnt_exist(settings.links_db)
    exists = db.create_if_doesnt_exist(settings.imgurtoken_db)
    if not exists:
        db.insert(settings.imgurtoken_db,"token","{}")
    links.load_links_db()
    imgur_api.init()
    random.seed()  # init random number generator
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port, debug=True)  # , ssl_context=context)
