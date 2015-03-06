import urllib.request
import json
import urllib.parse
from subprocess import call
from http.client import BadStatusLine

def getResponse():
    try:
        req = urllib.request.Request("https://api.twitch.tv/kraken/streams/followed", None, headers)
        response = urllib.request.urlopen(req)
        return response
    except BadStatusLine:
        print("Fetching failed, trying again...")
        getResponse()

authfile = open('authcode.txt')
hashshit = authfile.readline() #idk how to advance line number
auth = authfile.readline().strip()
oauth = 'OAuth ' + auth
headers = {'Authorization' : oauth}
response = getResponse()
jsonst = response.read().decode('utf-8')
pyjson = json.JSONDecoder().decode(jsonst)

streamers = []
names = []
statuses = []

for stream in pyjson["streams"]:
    for item,value in stream["channel"].items():
        if (item == "display_name"):
            streamers.append(value)
        if (item == "name"):
            names.append(value)
        if (item == "status"):
            statuses.append(value)

i=0
for streamer in streamers:
    text = '[' + str(i) + '] ' + streamer + " - " + statuses[i].encode('utf-8').decode('ascii','ignore')
    i = i + 1
    print(text)
rawinput = input("Which streamer would you like to watch? ")
print("Loading the stream: " + streamers[int(rawinput)])
cmd = "twitch.tv/" + names[int(rawinput)]
call(["livestreamer", cmd, "best"])
