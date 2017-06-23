from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
import re
import pyperclip
import time

seconds = 2

def checkUrl(url):
    r = re.compile('http[s]?://p*')
    if (r.match(url) != None):
        return True
    return False

def getImageUrl(url):
    req = Request(url, headers={'User-Agent' : "LightScrapeShot"})
    response = urlopen(req)
    html = response.read()
    soup = BeautifulSoup(html, 'html.parser')
    imgUrl = soup.find('img', id='screenshot-image')['src']
    return imgUrl
url = pyperclip.paste()
if (url != None):
    if (checkUrl(url)):
        print("Clipboard url: {}".format(url))
        imgUrl = getImageUrl(url)
        print("Scraped url: {}".format(imgUrl))
        pyperclip.copy(imgUrl)
    else:
        print("Bad url! Could not continue.")
print("Script will end in {} seconds.".format(seconds))
time.sleep(seconds)
