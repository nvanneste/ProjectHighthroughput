
import datetime
import json
import logging
import re
import sys
import urllib2



def main():
    url= "https://www.openhumans.org/api/public-data/?source=american_gut"
    data = json.load(urllib2.urlopen(url))

    print(data)

if __name__ == '__main__':
    main()
