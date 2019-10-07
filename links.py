import os
import json
import settings
from common import log
import db

Links = {}

def load_links_db():
    global Links
    try:
        new_links = db.select("*")
        Links = new_links
        log("Links dictionary loaded from db")
    except:
        log("DB error")
        pass



def find_links_contain(cont=""):
    retval = []
    for link in Links:
        if cont in str(link):
            retval.append(link)
    return retval


def search_links(request):
    if type(request) == list and len(request) in {1, 2}:
        load_links_db()
        string = "Currently remembered links %sare:\n" % \
                 (("that start with '%s' " % request[1]) if len(request) == 2 else "")
        string += "'" + "', '".join(find_links_contain(request[1] if len(request) == 2 else '')) + "'"
        return string
    else:
        return "Wrong number of parameters. Usage /listlink [phrase]"


def remember_link(request):
    if type(request) == list and len(request) == 3:
        overwrite=False
        if request[1] in Links:
            overwrite=True
            prevVal=Links[request[1]]

        request[2] = remove_braces_from_link(request[2])
        Links[request[1]] = request[2]  # + ("v" if str(request[2].endswith(".gif")) else "") # can be activated
        if overwrite:
            db.update(request[1],request[2])
            return "'%s' overwritten, previous value: '%s'" % (request[1], prevVal)
        else:
            db.insert(request[1],request[2])
            return "'%s' remembered" % request[1]
    else:
        return "Wrong number of parameters. Usage: /remember <name> <link>"


def forget_link(request):
    if type(request) == list and len(request) == 2:
        if request[1] in Links:
            db.delete(request[1])
            del Links[request[1]]

            return "'%s' forgotten" % request[1]
        else:
            return "'%s' cannot be found" % request[1]
    else:
        return "Wrong number of parameters. Usage: /forget <name>"


# noinspection PyUnusedLocal
def recall_link(request):
    load_links_db()  # reload just in case - it should already be synced
    if type(request) == list and len(request) in {2, 3}:
        global nsfw_tag
        if {'nsfw', 'hide', 'NSFW'}.intersection(request):  # nsfw/hide parameter
            nsfw_tag = True

        if 'nsfw' in request[1]:  # link key contains nsfw
            nsfw_tag = True

        if request[1] in Links:
            return str(Links[request[1]])
        else:
            return "'%s' cannot be found\nDid you mean any of the following: %s" % \
                   (request[1], "'" + "', '".join(find_links_contain(request[1])) + "'")
    else:
        return "Wrong number of parameters. Usage /recall <name> [nsfw/hide]"

def remove_braces_from_link(link):
    link = link.replace("[","")
    link = link.replace("]", "")
    return link