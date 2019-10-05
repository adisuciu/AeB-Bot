import os
import json
import settings
from common import log

Links = {}

def load_links_file():
    if not os.path.isfile(settings.links_file):
        log("%s does not exist. No links loaded" % settings.links_file)
        return  # file does not exist

    with open(settings.links_file) as file:
        file_content = file.read()

    global Links
    Links = json.loads(file_content)
    log("Links dictionary loaded from %s" % settings.links_file)


def save_links_file():
    output = json.dumps(Links)
    with open(settings.links_file, mode="w") as file:
        file.write(output)


def find_links_contain(cont=""):
    retval = []
    for link in Links:
        if cont in str(link):
            retval.append(link)
    return retval


def search_links(request):
    if type(request) == list and len(request) in {1, 2}:
        load_links_file()
        string = "Currently remembered links %sare:\n" % \
                 (("that start with '%s' " % request[1]) if len(request) == 2 else "")
        string += "'" + "', '".join(find_links_contain(request[1] if len(request) == 2 else '')) + "'"
        return string
    else:
        return "Wrong number of parameters. Usage /listlink [phrase]"


def remember_link(request):
    if type(request) == list and len(request) == 3:
        if request[1] in Links:
            return "This name already exists in the database"
        else:
            request[2] = remove_braces_from_link(request[2])
            Links[request[1]] = request[2]  # + ("v" if str(request[2].endswith(".gif")) else "") # can be activated
            save_links_file()
            return "'%s' remembered" % request[1]
    else:
        return "Wrong number of parameters. Usage: /remember <name> <link>"


def forget_link(request):
    if type(request) == list and len(request) == 2:
        if request[1] in Links:
            del Links[request[1]]
            save_links_file()
            return "'%s' forgotten" % request[1]
        else:
            return "'%s' cannot be found" % request[1]
    else:
        return "Wrong number of parameters. Usage: /forget <name>"


# noinspection PyUnusedLocal
def recall_link(request):
    load_links_file()  # reload just in case - it should already be synced
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