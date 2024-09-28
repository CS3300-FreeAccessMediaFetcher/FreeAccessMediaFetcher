import requests
import time
from bs4 import BeautifulSoup

# Global Variables
headers = {'User-Agent':
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
            'Accept-Language': 'en-US, en;q=0.5'}
textCounter = 0
linkCounter = 0
imageCounter = 0
otherCounter = 0
dataSet = {}
dictIndex = 0
validDataTypes = ['web_page', 'text', 'image', 'audio', 'video']


class siteObject:
    def __init__(self,dataType,dataName,dataSize,data):
        self.dataType = dataType
        self.dataName = dataName
        self.dataSize = dataSize
        self.data = data


# INPUT FROM FLASK #
def webScraperInput(url: str, data_type: str):
    pass

###################


def dataCollection(inc_website : str):
    lobj_response = requests.get(inc_website,headers=headers)
    if lobj_response.status_code == 200:
        print("Connected to " + inc_website)
        site = BeautifulSoup(lobj_response.text,"html.parser")
        header = site.find('header')
        footer = site.find('footer')
        if header:
            header.decompose()
        if footer:
            footer.decompose()
        # print(site.prettify())
        print("----------------------------------------------------------------------------------\nBeginning Harvest of site...\n----------------------------------------------------------------------------------")

        collectAllStrings(site)
        collectAllLinks(site)
        collectAllImg(site)
    else:
        print("unable to reach site")


def collectAllImg(inc_site: BeautifulSoup):
    #One is for counting images in a page
    global imageCounter
    #This one is for labelling images without alt text
    imageNumber = 1
    for imgs in inc_site.find_all('img'):
        imageSource = imgs.attrs['src']
        if 'http' not in imageSource and not (imageSource.startswith("//")):
            imageSource = scraping_site + "/" + imageSource
        if imageSource.startswith("//"):
            imageSource = imageSource.replace("//","")
            # imageSource = "https:" + imageSource
        imageName = imgs.get('alt')
        if imageName is None:
            imageName = "Unknown Image " + str(imageNumber)
        # print(imageSource)
        # print(imageName)
        dataPoint = siteObject("image",imageName,"0mb",imageSource)
        imageCounter += 1
        imageNumber += 1
        addToDictionary(dataPoint)
        



def collectAllStrings(inc_site: BeautifulSoup):
    global textCounter
    for text in inc_site.find_all(['p','title']):
        for child in text.contents:
            dataPoint = siteObject("text","text","0mb",child.get_text())
            textCounter += 1
            addToDictionary(dataPoint)
            
def collectAllLinks(inc_site: BeautifulSoup):
    global linkCounter
    for atags in inc_site.find_all(['a']):
        link = atags.get("href")
        if 'http' not in link:
            link = scraping_site + "/" + link
        # if "http" in link:
        dataPoint = siteObject("link","link","0mb",link)
        linkCounter += 1
        addToDictionary(dataPoint)

def addToDictionary(inc_object : siteObject):
    global dataSet
    global dictIndex
    dataSet[dictIndex] = inc_object
    dictIndex += 1

# This will return all data of one type
# Currently it just prints the information but depending on the type it will download an instance of the data
def retrieveDataByType(inc_dataType):
    global dataSet
    listOfData = []
    for dataIndex in dataSet:
        if dataSet[dataIndex].dataType == inc_dataType:
            listOfData.append(dataSet[dataIndex])
    for instance in listOfData:
        print(instance.dataName, " : ", instance.data)

def retrieveDataByName(inc_dataName):
    global dataSet
    imgFound = False
    for dataIndex in dataSet:
        if dataSet[dataIndex].dataName == inc_dataName:
            instance = dataSet[dataIndex]
            imgFound = True

    if imgFound:
        print(instance.dataName, " : ", instance.data)
    else:
        print("Image not Found")

# scraping_site = "https://en.wikipedia.org/wiki/List_of_Testudines_families"
scraping_site = "https://books.toscrape.com"
# scraping_site = "http://quotes.toscrape.com"


#This is solely for testing
'''
dataCollection(scraping_site)
print("",textCounter, "blobs of text collected\n",linkCounter,"links collected\n",imageCounter,"images collected\n",otherCounter,"bits of unkown data collected")

retrievalType = input("Enter if you want type or name:")

if retrievalType == "type":
# retrieveDataTest = "image"
    retrieveDataTest = input("Enter the type of data you desire:")
    retrieveDataByType(retrieveDataTest)
elif retrievalType == "name":
    retrieveDataTest = input("Enter the name of the data you desire:")
    retrieveDataByName(retrieveDataTest)
else:
    print("Invalid choice")
'''


