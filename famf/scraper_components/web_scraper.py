import requests
import sys
import regex as re
from urllib.parse import urlsplit
from urllib.robotparser import RobotFileParser
from bs4 import BeautifulSoup
import winreg
import os




# Global Variables

headers = {'User-Agent':
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
            'Accept-Language': 'en-US, en;q=0.5'}

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
        dataPoint = siteObject("image",imageName,sys.getsizeof(imageSource),imageSource)
        imageCounter += 1
        imageNumber += 1
        addToDictionary(dataPoint)

def collectAllStrings(inc_site: BeautifulSoup):
    global textCounter
    for text in inc_site.find_all(['p','title','a','span']):
        for child in text.contents:
            baseText = child.get_text().strip()
            #baseText = re.sub('\ {2,}', '', baseText)
            newText = re.sub('\n*', '', baseText)
            if newText != '':
                dataPoint = siteObject("text","text", sys.getsizeof(newText),newText)
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
        dataPoint = siteObject("link",linkName,sys.getsizeof(link),link)
        linkCounter += 1
        addToDictionary(dataPoint)

#Adds the object that is being passed into the function into the over arching dictionary of objects scraped from the site
def addToDictionary(inc_object : siteObject):
    global dataSet
    global dictIndex
    dataSet[dictIndex] = { "dataType": inc_object.dataType, "dataSize": inc_object.dataSize, "dataName": inc_object.dataName, "data": inc_object.data } 
    dictIndex += 1

# This will return all data of one type
# Currently it just returns the information based on the type
def retrieveDataByType(inc_dataType):
    global dataSet
    listOfData = []
    for dataIndex in dataSet:
        if dataSet[dataIndex]["dataType"] == inc_dataType:
            listOfData.append(dataSet[dataIndex])
    #for instance in listOfData:
    #    print(instance.dataName, " : ", instance.data)
    return listOfData

# This will return data by a certain name (only works for images at the moment)
# Currently it just returns the data based on the name
def retrieveDataByName(inc_dataName):
    global dataSet
    for dataIndex in dataSet:
        if dataSet[dataIndex]["dataName"] == inc_dataName:
            instance = dataSet[dataIndex]
            print(instance.dataName, " : ", instance.data)


# This function runs after Flask receives the input URL from the frontend
# INPUT FROM FLASK #
def webScraperInput(url: str, data_type: str):
    if robotsText(url):
        try:
            dataCollection(url, data_type)
            results_list = retrieveDataByType(data_type)
            print(f"Retrieved {len(results_list)} results of type {data_type} from {url}. Returning to Flask...")
            return { "StatusCode": 200, "DataList": results_list }
        except Exception as e:
            return { "StatusCode": 400, "Error": str(e) }
    else:
        return { "StatusCode": 403, "Error": str("Robots.txt hates us") }

    
def downloadData(download_type: str, data: list):
    print(download_type, data)
    download_path = retrieveDownloadsFolder()

    #The following variable is to store all the text in the same variable
    text_list = []
    for item in data: 
        if item['type'] == 'image' :
            photoLink = item['link']
            downloadImage(photoLink,download_path)
            # print(photoLink)
        elif item['type'] == 'text' :
            textBlock = "\n "  + item['text']
            text_list.append(textBlock)
            # print(text_list)
        else:
            print("This type has not yet been implemented")
    if len(text_list) > 0:
        downloadText(text_list,download_path)
        
def downloadImage(image_url,download_path):
    response = requests.get(image_url)
    
    if response.status_code == 200:
        filename = re.search(r'/([\w_-]+[.](jpg|gif|png|svg))$', image_url)
        if not filename:
            print("Regex didn't match with the url: {}".format(image_url))
        else:
            final_path = download_path + filename.group(1)
            with open(final_path, 'wb') as f:
                f.write(response.content)
    else:
        print("Failed to retrieve the image. Status code:", response.status_code)

def downloadText(text_list, download_path):
    filename = "downloaded_text.txt"

    final_path = download_path + filename

    if os.path.exists(final_path):
        with open("existing_file.txt", "a") as file:
            file.writelines(text_list)
    else:
         with open(final_path, "w") as file:
            file.writelines(text_list)
        
    

def retrieveDownloadsFolder():
    reg_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders")
    downloads_path = winreg.QueryValueEx(reg_key, "{374DE290-123F-4565-9164-39C4925E467B}")[0] + "\\"
    winreg.CloseKey(reg_key)
    # print(downloads_path)
    return downloads_path

def webScraperDictionaryClear():
    dataSet.clear()

def robotsText(url: str):
    #Testing New Code
    split_url = urlsplit(url)
    lstr_robotUrl = split_url.scheme + "://" + split_url.netloc + "/robots.txt"

    response = requests.get(lstr_robotUrl,headers=headers)

    if response.status_code == 200 :
        rp = RobotFileParser()
        rp.parse(response.text.splitlines())
        
        user_agent = '*'
        url_to_check = url
    
        if rp.can_fetch(user_agent, url_to_check):
            print(f"We are allowed to access {url_to_check}")
            return True
        else:
            print(f"We are NOT allowed to access {url_to_check}")
            return False

    elif response.status_code == 404:
        #There is no robots.txt page
        return True
    else:
        return False


    