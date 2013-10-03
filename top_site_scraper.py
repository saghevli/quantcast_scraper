# This file parses quantcast.com and aggregates a list of
# sites that quantcast has detailed data on.

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

    bigSiteList = []
    for i in range(1, 3):
        pageList = getPageList(i)
        if saveToDisc :
            pickle.dump(pageList, 
                    open(os.path.join(os.path.dirname(__file__),
                    './res/sites/page_' + str(i) + "_urls.p"), "wb" ))
        else :
            bigSiteList.extend(pageList)

    if not saveToDisc:
        pprint(bigSiteList)

def getPageList(pageNum):
    loopUntilSuccess = True
    tryCount = 0
    # catch exceptions and try 30 times
    while loopUntilSuccess and tryCount < 30:
        try:
            connection = urllib2.urlopen(
                    "https://www.quantcast.com/top-sites/US/" + str(pageNum))
            soup = BeautifulSoup(connection.read())
            soup.prettify()
            connection.close()
        except:
            print "Error on page load, will sleep and retry."
            time.sleep(1)

    sitesTableLeft = soup.find_all('table',
            class_=re.compile('listView'))[0]
    sitesTableRight = soup.find_all('table',
            class_=re.compile('listView'))[1]
    topSitesLeft = sitesTableLeft.find_all('tr')
    topSitesRight = sitesTableRight.find_all('tr')

    resultList = getListFromTable(topSitesLeft)
    resultList.extend(getListFromTable(topSitesRight))
    return resultList

# topsites is a bs4.element.ResultSet object
def getListFromTable(topSites):
    topSites.pop(0)
    outputList = []
    for entry in topSites:
        link = entry.find('a')
        #filter hidden sites
        if link is None:
            continue
        badge = entry.find('td', class_=re.compile('badge')).find('img')
        if badge is not None:
            outputList.append(str(link.contents[0]))
    return outputList

if __name__ == "__main__":
    main()