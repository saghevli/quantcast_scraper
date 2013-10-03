# This file grabs data from a specific site's profile on quantcast.com and
# stores it. 

import urllib2
import re
import os
import time
import cPickle as pickle
from pprint import pprint
from bs4 import BeautifulSoup

def main():
    saveToDisc = False
    x = raw_input("Save to disk? [y/n]:")
    if x == 'y':
        saveToDisc = True

    output_dict = {}

    for i in range(1, 2):
        page_list = pickle.load(
                open(os.path.join(os.path.dirname(__file__),
                './res/sites/page_' + str(i) + "_urls.p"), "rb"))
        for url in page_list:
            output_dict[url] = getPageData(url)

        # either save to pickle file or print
        if saveToDisc :
            pickle.dump(output_dict,
                    open(os.path.join(os.path.dirname(__file__),
                    './res/data/page_' + str(i) + "_data.p"), "wb"))
        else:    
            pprint(output_dict)

def getPageData(url):
    loopUntilSuccess = True
    tryCount = 0
    # catch exceptions and try 30 times
    while loopUntilSuccess and tryCount < 30:
        try:
            connection = urllib2.urlopen(
                "https://www.quantcast.com/" + str(url))
            soup = BeautifulSoup(connection.read())
            soup.prettify()
            connection.close()
            tryCount += 1
            loopUntilSuccess = False
        except:
            print "Error on page load, will sleep and retry."
            time.sleep(1)

    allrows = soup.find_all('tr', class_=re.compile('tr-'))
    contents = {}
    for row in allrows:
        name = str(row.find_all('td',
                class_=re.compile('bucket-label'))[0].contents[0])
        data = str(row.find_all('td',
                class_=re.compile('index-'))[0].contents[0].split()[0])
        contents[name] = data

    return contents

if __name__ == "__main__":
    main()