import settings
import time
import datetime
import urllib
import sys

start_time = time.time()
with open(settings.log_file, mode='w') as f:  # delete previous file
    pass


def get_uptime():
    sec = datetime.timedelta(seconds=int((time.time() - start_time)))
    d = datetime.datetime(1, 1, 1) + sec
    return d


def log(message):
    d = get_uptime()
    string = ("[%d:%02d:%02d:%02d] - " % (d.day - 1, d.hour, d.minute, d.second)) + str(message)
    print(string)
    with open(settings.log_file, mode='a') as file:
        file.write(string + '\n')


def log_exception(message):
    log("EXCEPTION! - " + str(message))


def send_http_query(query):
    result_qry = ""
    # review this part
    # noinspection PyBroadException
    try:
        result_qry = urllib.request.urlopen(query).read()
    except:  # urllib.error.HTTPError:
        if type(query) == str:
            log("request query - " + query)
        else:
            log(query.full_url)
        if result_qry:
            log("response query - " + str(result_qry))
        else:
            log("no response")
        log_exception(str(sys.exc_info()))
    return result_qry
