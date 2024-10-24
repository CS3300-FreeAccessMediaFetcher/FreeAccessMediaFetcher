import requests
import time
from bs4 import BeautifulSoup

# headers = {'User-Agent':
#             'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
#             'Accept-Language': 'en-US, en;q=0.5'}
# headers = {'accept':'*/*',
# 'accept-encoding':'gzip, deflate, br',
# 'accept-language':'en-GB,en;q=0.9,en-US;q=0.8,hi;q=0.7,la;q=0.6',
# 'cache-control':'no-cache',
# 'dnt':'1',
# 'pragma':'no-cache',
# 'referer':'https',
# 'sec-fetch-mode':'no-cors',
# 'sec-fetch-site':'cross-site',
# 'user-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',}

# Global Variables

textCounter = 0
linkCounter = 0
imageCounter = 0
videoCounter = 0
otherCounter = 0
dataSet = {}
dictIndex = 0


class siteObject:
    def __init__(self,dataType,dataName,dataSize,data):
        self.dataType = dataType
        self.dataName = dataName
        self.dataSize = dataSize
        self.data = data

        
# INPUT FROM FLASK #
def webScraperInput(url: str, data_type: str):
    print("Hello Flask!")
    return { "StatusCode": 200 }

###################

def retrieveDictionary():
    global dataSet
    localData = dataSet
    return localData

def dataCollection(inc_website : str):
    lobj_response = requests.get(inc_website)
    if lobj_response.status_code == 200:
        print("Connected to " + inc_website)
        site = BeautifulSoup(lobj_response.text,"html.parser")
        header = site.find('header')
        footer = site.find('footer')
        if header:
            header.decompose()
        if footer:
            footer.decompose()
        print(site.prettify())
        print("----------------------------------------------------------------------------------\nBeginning Harvest of site...\n----------------------------------------------------------------------------------")

        collectAllStrings(site)
        collectAllLinks(site)
        collectAllImg(site)
        # collectAllVideos(site)
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
        

def collectAllVideos(inc_site: BeautifulSoup):
    global videoCounter
    #Below is a counter to label videos
    videoNumber = 1
    
    video_tags = inc_site.findAll('video')
    print("Total ", len(video_tags), "videos found")
    for videos in inc_site.find_all('video'):
        videoSource = videos.attrs['src']
        videoCounter += 1
        videoNumber += 1
        print(videoSource)

def collectAllStrings(inc_site: BeautifulSoup):
    global textCounter
    for text in inc_site.find_all(['p','title']):
        for child in text.contents:
            if child.get_text() == "":
                print("Blank text")
            else:    
                dataPoint = siteObject("text","text","0mb",child.get_text())
                textCounter += 1
                addToDictionary(dataPoint)
            
def collectAllLinks(inc_site: BeautifulSoup):
    global linkCounter
    for atags in inc_site.find_all(['a']):
        if atags.get_text() != "":
            linkName = atags.get_text()
        else:
            linkName = "Unlabeled Link"
        link = atags.get("href")
        # if "http" in link:
        dataPoint = siteObject("link",linkName,"0mb",link)
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
    for dataIndex in dataSet:
        if dataSet[dataIndex].dataName == inc_dataName:
            instance = dataSet[dataIndex]
            print(instance.dataName, " : ", instance.data)




#The following code is solely for testing

# scraping_site = "https://en.wikipedia.org/wiki/List_of_Testudines_families" #mass testing
scraping_site = "https://books.toscrape.com" #Image testing
# scraping_site = "https://www.youtube.com/watch?v=LJHQXmOpkUE" #video testing
# scraping_site = "http://quotes.toscrape.com" #Text testing

dataCollection(scraping_site)


print("",textCounter, "blobs of text collected\n",linkCounter,"links collected\n",imageCounter,"images collected\n",otherCounter,"bits of unkown data collected")



print(dataSet)

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