import urllib2
import re
from pprint import pprint
from bs4 import BeautifulSoup

def main():
    # dataList = getPageData("https://www.quantcast.com/stackexchange.com")
    # pprint(dataList)

    #getSiteNames
    bigDataSet = []
    for i in range(1, 2):
        bigDataSet.extend(getPageList(i))

    # results = []
    # for entry in bigDataSet:
    #     results.append((entry, getPageData(entry)))
    # pprint(results)

    pprint(bigDataSet)

def getPageList(pageNum):
    connection = urllib2.urlopen(
            "https://www.quantcast.com/top-sites/US/" + str(pageNum))
    soup = BeautifulSoup(connection.read())
    soup.prettify()
    connection.close()

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
    output = []
    for entry in topSites:
        link = entry.find('a')
        #filter hidden sites
        if link is None:
            continue
        badge = entry.find('td', class_=re.compile('badge')).find('img')
        if badge is not None:
            output.append(str(link.contents[0]))
    return output

def getPageData(url):
    connection = urllib2.urlopen("https://www.quantcast.com/" + str(url))
    soup = BeautifulSoup(connection.read())
    soup.prettify()
    connection.close()

    allrows = soup.find_all('tr', class_=re.compile('tr-'))
    contents = []
    for row in allrows:
        name = str(row.find_all('td',
                class_=re.compile('bucket-label'))[0].contents[0])
        data = str(row.find_all('td',
                class_=re.compile('index-'))[0].contents[0].split()[0])
        contents.append((name, data))

    return contents

if __name__ == "__main__":
    main()