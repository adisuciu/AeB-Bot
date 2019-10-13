import imgur_api
import settings
from common import send_http_query
from common import log
import urllib
import urllib.request
import io
from base64 import b64encode
import json
import mimetypes
import datetime
import links
from links import find_links_contain

import PIL
from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw

Dict = {"10guy": "10+Guy",
        "chucknorris": "3g3xw",
        "anditsgone": "Aaaaand+Its+Gone",
        "advicemallard": "Actual+Advice+Mallard",
        "aintnobodygottimeforthat": "Aint+Nobody+Got+Time+For+That",
        "amitheonlyone": "Am+I+The+Only+One+Around+Here",
        "ancientaliens": "Ancient+Aliens",
        "backinmyday": "Back+In+My+Day",
        "badluckbrian": "Bad+Luck+Brian",
        "batmanslap": "Batman+Slapping+Robin",
        "beargrylls": "Bear+Grylls",
        "braceyourselves": "Brace+Yourselves+X+is+Coming",
        "badjokeeel": "Bad+Joke+Eel",
        "cristos": "Buddy+Christ",
        "businesscat": "Business+Cat",
        "butthurtdweller": "Butthurt+Dweller",
        "captainhindsight": "Captain+Hindsight",
        "chubbybubbles": "Chubby+Bubbles+Girl",
        "cleavegegirl": "Cleavage+Girl",
        "collegefreshman": "College+Freshman",
        "condescendingwonka": "Condescending+Wonka",
        "confessionbear": "Confession+Bear",
        "conspiracykeanu": "Conspiracy+Keanu",
        "disastergirl": "Disaster+Girl",
        "drevillaser": "Dr+Evil+Laser",
        "dwightschrute": "Dwight+Schrute",
        "evilracoon": "Evil+Plotting+Raccoon",
        "firstdayontheinternet": "First+Day+On+The+Internet+Kid",
        "firstworldproblem": "First+World+Problems",
        "futuramafry": "Futurama+Fry",
        "futuramazoidberg": "Futurama+Zoidberg",
        "gayseal": "Homophobic+Seal",
        "goodguygreg": "Good+Guy+Greg",
        "gordonramsay": "Angry+Chef+Gordon+Ramsay",
        "grumpycat": "Grumpy+Cat",
        "highdog": "High+Dog",
        "storygrandpa": "Storytelling+Grandpa",
        "facepalmbear": "Facepalm+Bear",
        "awkwardpenguin": "Socially+Awesome+Awkward+Penguin",
        "hideyokids": "Hide+Yo+Kids+Hide+Yo+Wife",
        "ishouldbuyaboat": "I+Should+Buy+A+Boat+Cat",
        "itooliketolivedangerously": "I+Too+Like+To+Live+Dangerously",
        "illhaveyouknow": "Ill+Have+You+Know+Spongebob",
        "inception": "Inception",
        "insanitywolf": "Insanity+Wolf",
        "josephducreux": "Joseph+Ducreux",
        "laughingvillains": "Laughing+Villains",
        "mrmackey": "Mr+Mackey",
        "officercartman": "Officer+Cartman",
        "onedoesnot": "One+Does+Not+Simply",
        "overlyattachedgf": "Overly+Attached+Girlfriend",
        "manlyman": "Overly+Manly+Man",
        "patrioteagle": "Patriotic+Eagle",
        "pedobear": "Pedobear",
        "pettergriffinnews": "Peter+Griffin+News",
        "philosoraptor": "Philosoraptor",
        "putitpatrick": "Put+It+Somewhere+Else+Patrick",
        "rpgfan": "RPG+Fan",
        "dotafan": "RPG+Fan",
        "rastateacher": "Rasta+Science+Teacher",
        "redditorwife": "Redditors+Wife",
        "redneckrandall": "Redneck+Randal",
        "photogenicguy": "Ridiculously+Photogenic+Guy",
        "ronswanson": "Ron+Swanson",
        "sadkeanu": "Sad+Keanu",
        "samueljackson": "Samuel+Jackson+Glance",
        "scrooge": "Scrooge+McDuck+2",
        "scumbaggirl": "Scumbag+Girl",
        "scumbagsteve": "Scumbag+Steve",
        "seriousxzibit": "Serious+Xzibit",
        "takemymoney": "Shut+Up+And+Take+My+Money+Fry",
        "spidermancomputer": "Spiderman+Computer+Desk",
        "spidermanhospital": "Spiderman+Hospital",
        "successkid": "Success+Kid+Original",
        "suddenclarity": "Sudden+Clarity+Clarence",
        "skiinstructor": "Super+Cool+Ski+Instructor",
        "thatwouldbegreat": "That+Would+Be+Great",
        "mostinterestingman": "The+Most+Interesting+Man+In+The+World",
        "skepticalkid": "Third+World+Skeptical+Kid",
        "thirdworldsuccess": "Third+World+Success+Kid",
        "thatescalatedquickly": "Well+That+Escalated+Quickly",
        "whynotboth": "Why+Not+Both",
        "yodawg": "Yo+Dawg+Heard+You",
        "confessionkid": "confession+kid",
        "lazycollegesenior": "Lazy+College+Senior",
        "matrixmorpheus": "Matrix+Morpheus",
        "toodamnhigh": "Too+Damn+High",
        "darthvader": "star-wars-vader-force-choke",
        "ghettojesus": "Ghetto+Jesus",
        "facepalm2": "Frustrated+Boromir",
        }


def find_memes_contain(cont=""):
    retval = []
    for key, value in sorted(Dict.items()):
        if cont in key:
            retval.append(key)
    return retval


def search_meme(request):
    if type(request) == list and len(request) in {1, 2}:
        string = "Currently implemented memes %sare:\n" % \
                 (("that contain with '%s' " % request[1]) if len(request) == 2 else "")
        string += "'" + "', '".join(find_memes_contain(request[1] if len(request) == 2 else '')) + "'"
        return string
    else:
        return "Wrong number of parameters. Usage /search_meme [phrase]"


def DrawOutlinedText(image, coords, text, font, outline="black", fill="white"):
    if type(coords) != tuple:
        raise ValueError("coords not tuple")
    x = coords[0]
    y = coords[1]
    image.text((x - 1, y - 1), text, font=font, fill=outline)
    image.text((x + 1, y + 1), text, font=font, fill=outline)
    image.text((x + 1, y - 1), text, font=font, fill=outline)
    image.text((x - 1, y + 1), text, font=font, fill=outline)
    image.text(coords, text, font=font, fill=fill)


def build_meme_from_link(request, toptext_, bottomtext_):
    toptext = urllib.parse.unquote_plus(toptext_)
    bottomtext = urllib.parse.unquote_plus(bottomtext_)

    if not toptext and not bottomtext:
        return request[1]

    response = send_http_query(request[1])
    if response:
        file = io.BytesIO(response)
    else:
        return "URL not found"

    log("image loaded from %s " % request[1])
    basewidth = 640

    # resize file to base width 500

    img = Image.open(file)
    wpercent = (basewidth / float(img.size[0]))
    if 0.9 <= wpercent <= 1.1:
        hsize = int(float(img.size[1]) * float(wpercent))
        img = img.resize((basewidth, hsize), PIL.Image.ANTIALIAS)
        log("image resized")

    draw = ImageDraw.Draw(img)
    shadowcolor = "black"
    fillcolor = "white"
    width = img.size[0]
    height = img.size[1]
    textwidth = (width * 80)/100
    textheight = (height * 18)/100
    maxFontSize = 300
    # search appropriate font size
    for i in range(maxFontSize):
        font = ImageFont.truetype(settings.font_location, i)
        toptextsize = font.getsize(toptext)
        if textwidth < toptextsize[0]:
            break
        if textheight < toptextsize[1]:
            break;

    # draw top text
    DrawOutlinedText(draw, ((width - toptextsize[0]) / 2, 5), toptext, font=font, outline=shadowcolor, fill=fillcolor)

    # search appropriate font size
    bottextsize = (0,0)
    for i in range(maxFontSize):
        font = ImageFont.truetype(settings.font_location, i)
        bottextsize = font.getsize(bottomtext)
        # workaround for older PIL version that is used by pythonanywhere
        bottextheight=i
        if textwidth < bottextsize[0]:
            break
        if textheight < bottextsize[1]:
            break

    # draw bottom text
    DrawOutlinedText(draw, ((width - bottextsize[0]) / 2, height - bottextheight - 10), bottomtext,
                     font=font, outline=shadowcolor, fill=fillcolor)

    img=img.convert("RGB")
    img.save(settings.image_temp_file, quality=50)
    log("Text added to the image")
    with open(settings.image_temp_file, "rb") as file:
        data = urllib.parse.urlencode({'image': b64encode(file.read())})
    binary_data = data.encode('ASCII')
    log("Upload start")
    req = urllib.request.Request("https://api.imgur.com/3/upload", data=binary_data,
                                 headers=imgur_api.build_header())
    log("logged in as %s" % imgur_api.get_bot_username())
    response = send_http_query(req)
    if response:
        log("Upload finish")
        json_data = json.loads(response.decode('utf-8'))
        return json_data['data']['link']
    else:
        log("Upload failed")
        return "Upload to imgur failed"


# Returns the Image urls + the file name
def processRedditAndImgurURL(url):
    o = urllib.parse.urlparse(url)

    # logger.debug(url)
    # logger.debug(o)

    # From Reddit
    if 'i.reddit.com' == o.netloc:
        # Direct Link
        return url

    # From Imgur
    if 'i.imgur.com' == o.netloc:
        # Direct Link
        return url

    if 'imgur.com' == o.netloc and ('/a/' in o.path or '/gallery/' in o.path):
        # Album (Can't get images from here)
        response=urllib.request.urlopen(url)
        data = response.read()
        content = data.decode("utf-8")
        url = "https://i.imgur.com/" + content.split("https://i.imgur.com/",1)[1].split("\"")[0]
        return url

    if 'imgur.com' == o.netloc:
        # Page link
        img_id = url.split('/')[-1] + '.jpg'
        return url + '.jpg'

    return url

def meme_gen(request):
    if len(request) == 2:
        toptext = ""
        bottomtext = ""
    elif len(request) ==3:
        toptext=""
        bottomtext=urllib.parse.quote_plus(request[2])
    elif len(request) < 4:
        return "Wrong number of parameters. Usage /memegen <meme> '<text1>' '<text2>'"
    else:
        toptext = urllib.parse.quote_plus(request[2])
        bottomtext = urllib.parse.quote_plus(request[3])

    request[1]=links.remove_braces_from_link(request[1])

    if request[1] not in Dict:
        if (request[1]) not in links.Links:
            pass

        else:  # request is in links dictionary
            request[1] = links.Links[request[1]]  # change request to link

        request[1] = processRedditAndImgurURL(request[1])
        parsed_url = urllib.parse.urlparse(request[1])
        if not bool(parsed_url.scheme):
            return "Meme %s not found. Did you mean: %s" % (request[1], "'" +
                                                            "', '".join(find_memes_contain(request[1])) + "'" +
                                                            "', '".join(find_links_contain(request[1])) + "'")
        maintype = mimetypes.guess_type(parsed_url.path)[0]

        if maintype not in ('image/png', 'image/jpeg'):
            return "URL is not a png or jpeg"

        retval = build_meme_from_link(request, toptext, bottomtext)
    else:  # request in meme dictionary
        retval = "http://apimeme.com/meme?meme=%s&top=%s&bottom=%s" % (Dict[request[1]], toptext, bottomtext)

        if imgur_api.logged_in():
            data = urllib.parse.urlencode({'image': retval})
            binary_data = data.encode('ASCII')
            req = urllib.request.Request("https://api.imgur.com/3/upload", data=binary_data,
                                         headers=imgur_api.build_header())
            send_http_query(req)

    with open("meme_history", "a") as file:
        dt = datetime.datetime.now()
        #global last_sender
        file.write("[%d-%02d-%02d-%02d:%02d:%02d] <%s> %s\n" % (dt.year, dt.month, dt.day, dt.hour, dt.minute,
                                                                dt.second, "NOTIMPLEMENTED", retval))
    return retval
