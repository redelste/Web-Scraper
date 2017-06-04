 #the BBC test
import argparse, urllib3, certifi, sys, json, os, shutil
from lxml import html
from bs4 import BeautifulSoup
from termcolor import colored, cprint
import requests

parser = argparse.ArgumentParser()
parser.add_argument("searchTerms", help="terms for which you are searching")
args = parser.parse_args()
searchList = args.searchTerms.split(" ")

# set up urllib3 with cirtifi certificates
http = urllib3.PoolManager(
    cert_reqs= 'CERT_REQUIRED',
    ca_certs= certifi.where()
)

# create the initial url for the search
#you have to change this part depending on the site
testURL = "https://www.bbc.co.uk/search?q="
for term in searchList:
    if term != "":
        testURL += (term + "+")
testURL = testURL[0:len(testURL)-1] # remove the last '+' from the url


page = requests.get(testURL)
soup = BeautifulSoup(page.content, 'html.parser')

html = list(soup.children)[2] #selects the html section of the code so you can sift thorugh all of it
soup = BeautifulSoup(page.content, 'html.parser')
urlList = [] #should be a list of urls
resultList = soup.find_all('ol', attrs={'class':'search-results results'})
for result in resultList:
#    url = result.find('h1').get('h1', itemprop = 'headline')
#    url = result.find('a').get('href')
        url = soup.find_all('h1', attrs={'itemprop':'headline'})
        index = 2
        for i in url:
            if index < 15:
                i = i.find('a').get('href')
                urlList.append(i)
            index+=1

for i in urlList:
        print(i)

contentList = [] # [url, title, date, content]
jsonList = []

for url in urlList:
    data = {"url":"","title":"","date":"","content":""}
    data["url"] = url
    page = http.request('GET',url)
    page = BeautifulSoup(page.data, 'lxml')
    title = page.find('title').text
    data["title"] = title
    date = page.find('meta', attrs={'property': 'rnews:datePublished'})
    data["date"] = date
    print(date)
    article = page.find_all('p')
    content = ""
    for x in article:
        content += x.text
    data["content"] = content
    contentList.append([url, title, date, content])
    #jsonData = json.dumps(data)
    #jsonList.append(jsonData)
    badList = ["Sign in", "Something's gone wrong", "None", "To enjoy CBBC", "Snooker"]
    if content not in badList:
        print(content)
        jsonList.append(data)
i = 0
for item in jsonList:
    name =  "bbc" + str(i) +".json"
    with open(name, 'w') as outfile:
        json.dump(item, outfile)
    shutil.move(name, "json_files/" + name)
    i+=1
