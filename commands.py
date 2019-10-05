import settings
import common
import random
import links
import imgur_api
import meme

def about(request=0):
    return settings.about_message


# noinspection PyUnusedLocal
def uptime(request=0):
    d = common.get_uptime()
    return "Uptime: %d days, %02d:%02d:%02d " % (d.day - 1, d.hour, d.minute, d.second)


# noinspection PyUnusedLocal
def dummy(request=0):
    return False


def help(request=0):
    return "--help - this help\n" \
           "--about - about this bot\n" \
           "--quote <bug/ciuraru> - requests random BUG MAFIA/Ciuraru quote\n" \
           "--uptime - shows the uptime of the bot\n" \
           "--remember <name> <phrase> - maps <phrase> to a <name>. if name contains nsfw, no preview will be shown on recall\n" \
           "--forget <name> - forgets <name> and attached <phrase>\n" \
           "--recall <name> [hide/nsfw] - recalls the <phrase> with name <name> - [hide][nsfw] - hides preview\n" \
           "--search [phrase] - search all names that begin with [phrase]. [phrase] can be empty - lists all names \n" \
           "--getpic [subreddit] - gets a random picture from the subreddit. The picture is taken from today's top 60\n" \
           "--memegen <meme> '<top>' '<bottom>' - on the fly meme generator\n" \
           "--search_meme [phrase] - search all the available memes that begin with phrase\n" \
           "--imgur_status - returns the login status of the imgur account\n"


def quote(request):
    if len(request) == 2:
        switcher = {"bug": "bug_mafia.txt",
                    "ciuraru": "ciuraru.txt"}
        return build_quote_file(request, switcher[request[1]]) if request[1] in switcher else False


# noinspection PyUnusedLocal
def build_quote_file(request=0, quote_file="bug_mafia.txt"):
    if not quote_file:
        return "No quotes found. Usage quote <bug/ciuraru>"
    with open(quote_file) as file:
        content = file.readlines()
    string = content[random.randint(0, len(content) - 1)]  # return random string from file
    decoded_string = bytes(string, "utf-8").decode("unicode_escape")  # parse escape sequences such as \n
    return decoded_string


# noinspection PyUnusedLocal
def search_link(request=0):
    return links.search_links(request)


def remember_link(request=0):
    return links.remember_link(request)


def recall_link(request=0):
    return links.recall_link(request)


def forget_link(request=0):
    return links.forget_link(request)


def imgur_pic(request=0):
    return imgur_api.imgur_pic(request)


def login_imgur(request=0):
    return imgur_api.login_imgur(request)


def logout_imgur(request=0):
    return imgur_api.logout_imgur(request)


def login_status_imgur(request=0):
    return imgur_api.login_status_imgur(request)

def meme_gen(request=0):
    return meme.meme_gen(request)

def search_memes(request=0):
    return meme.search_meme(request)