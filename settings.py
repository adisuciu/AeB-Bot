import datetime

bot_prefix=''
dt = datetime.datetime.now()

links_file = "links.txt"
log_file = "logs/log-%d%02d%02d-%02d%02d%02d.txt" % (dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second)
image_temp_file = "temp.jpg"

with open("font","r") as f:
    font_location = f.read()
about_message = "Aici este BAIETII Official bot - v0.1\nSources available at: " \
                "https://github.com/adisuciu/AeB-Bot\n"

