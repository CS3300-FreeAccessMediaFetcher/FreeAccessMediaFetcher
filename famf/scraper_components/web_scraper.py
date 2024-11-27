import requests
import regex as re
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
validDataTypes = ['web_page', 'text', 'image', 'audio']

class siteObject:
    def __init__(self,dataType,dataName,dataSize,data):
        self.dataType = dataType
        self.dataName = dataName
        self.dataSize = dataSize
        self.data = data

###################

def retrieveDictionary():
    global dataSet
    localData = dataSet
    return localData

def dataCollection(inc_website : str, inc_dataType: str):
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
        # print(site.prettify())
        print("----------------------------------------------------------------------------------\nBeginning Harvest of site...\n----------------------------------------------------------------------------------")

        if inc_dataType == "text":
            collectAllStrings(site)
        elif inc_dataType == "web_page":
            collectAllLinks(site)
        elif inc_dataType == "image":
            collectAllImg(site, inc_website)
        # collectAllVideos(site)
    else:
        print("unable to reach site")


def collectAllImg(inc_site: BeautifulSoup, inc_input_url: str):
    #One is for counting images in a page
    global imageCounter
    #This one is for labelling images without alt text
    imageNumber = 1
    for imgs in inc_site.find_all('img'):
        imageSource = imgs.attrs['src']
        if 'http' not in imageSource and not (imageSource.startswith("//")):
            imageSource = inc_input_url + "/" + imageSource
        if imageSource.startswith("//"):
            imageSource = imageSource.replace("//","")
        imageName = imgs.get('alt')
        if imageName is None:
            imageName = "Unknown Image " + str(imageNumber)
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

def collectAllStrings(inc_site: BeautifulSoup):
    global textCounter
    for text in inc_site.find_all(['p','title','a']):
        for child in text.contents:
            baseText = child.get_text().strip()
            #baseText = re.sub('\ {2,}', '', baseText)
            newText = re.sub('\n*', '', baseText)
            if newText != '':
                dataPoint = siteObject("text","text","0mb",newText)
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
        dataPoint = siteObject("link",linkName,"0mb",link)
        linkCounter += 1
        addToDictionary(dataPoint)

def addToDictionary(inc_object : siteObject):
    global dataSet
    global dictIndex
    dataSet[dictIndex] = { "dataType": inc_object.dataType, "dataSize": inc_object.dataSize, "dataName": inc_object.dataName, "data": inc_object.data } 
    dictIndex += 1

# This will return all data of one type
# Currently it just prints the information but depending on the type it will download an instance of the data
def retrieveDataByType(inc_dataType):
    global dataSet
    listOfData = []
    for dataIndex in dataSet:
        if dataSet[dataIndex]["dataType"] == inc_dataType:
            listOfData.append(dataSet[dataIndex])
    #for instance in listOfData:
    #    print(instance.dataName, " : ", instance.data)
    return listOfData

def retrieveDataByName(inc_dataName):
    global dataSet
    for dataIndex in dataSet:
        if dataSet[dataIndex]["dataName"] == inc_dataName:
            instance = dataSet[dataIndex]
            print(instance.dataName, " : ", instance.data)


# This function runs after Flask receives the input URL from the frontend
# INPUT FROM FLASK #
def webScraperInput(url: str, data_type: str):
    try:
        dataCollection(url, data_type)
        results_list = retrieveDataByType(data_type)
        print(f"Retrieved {len(results_list)} results of type {data_type} from {url}. Returning to Flask...")
        return { "StatusCode": 200, "DataList": results_list }
    except Exception as e:
        return { "StatusCode": 400, "Error": str(e) }
    
def downloadData(download_type: str, data: list):
    print(download_type, data)

def webScraperDictionaryClear():
    dataSet.clear()