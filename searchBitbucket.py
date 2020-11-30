#!/usr/bin/python
import requests
import json
import re
import sys
  
def print_usage():
    print "Usage: searchBitbucket.py <query string>"
    print "This script queries Bitbucket server and returns the results"
    print "of regex-matched keywords"
    print "Example: searchBitbucket.py secret"
    sys.exit(1)

def print_error():
    print "Error: You must specify a query string"
    sys.exit(1)

try:
    KEYWORDS = str(sys.argv[1])
except:
    print_error()

#insert bitbucket rest api endpoint that accepts search POST requests  
API_ENDPOINT = "https://<bitbucket_server>/rest/search/latest/search"
  
# sending post request and saving response as response object 
r = requests.post(url = API_ENDPOINT, json = {"query":KEYWORDS,"entities":{"code":{}},"limits":{"primary":999,"secondary":999}}) 
  
# extracting response text  
response_message = r.json() 
json_obj = response_message

#999 is max results, set on server (default)
c = 0
while c < 1000:
    try:
        filename = json_obj['code']['values'][c]['file']
    except:
        filename = "Error"
    try:
        lines = json.dumps(json_obj['code']['values'][c]['hitContexts'], indent = 3)
    except:
        lines = "Error"
    print ("Result: ", c)
    #add some color and print output
    pattern = KEYWORDS
    replace = "\033[34m" + KEYWORDS + "\033[0m"
    res = re.sub(pattern, replace, lines, flags=re.I)
    print res
    print filename
    keyinput = str(raw_input("Press any key to continue...[w] write to log, [q] to quit :"))
    if keyinput is "w":
        f = open("search_log.txt", "a")
        f.write(res)
        f.write(filename)
        f.close()
    elif keyinput is "q":
        print "Quitting..."
        sys.exit(1)
    