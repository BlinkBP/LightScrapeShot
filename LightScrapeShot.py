from urllib.request import urlopen, Request
from PIL import Image, ImageGrab
from io import BytesIO
from bs4 import BeautifulSoup
import ctypes
import sys
import os
import re
import pyperclip
import time

seconds = 2
k32 = ctypes.windll.kernel32
u32 = ctypes.windll.user32
msvcrt = ctypes.windll.msvcrt

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

def getImage(url):
    req = Request(url, headers={'User-Agent' : "LightScrapeShot"})
    response = urlopen(req)
    #Getting byte object representing the image
    bytesImg = BytesIO(response.read())
    #Creating image from byte object
    img = Image.open(bytesImg)
    #Converting jpg to bmp
    out = BytesIO()
    img.convert("RGB").save(out, "BMP")
    #getting rid of bmp header and turning everything into binary
    byteImg = out.getvalue()[14:]
    return byteImg, out.getbuffer().nbytes

def copyImageToClipboard(img, size):
    if (u32.OpenClipboard(0)):
        u32.EmptyClipboard()
        #GMEM_MOVEABLE = 0x0002
        hg = k32.GlobalAlloc(0x0002, int(size))
        if (hg != None):
            ctypes.memmove(k32.GlobalLock(hg), img, size)
            k32.GlobalUnlock(hg)
            #CF_BITMAP = 2, CF_TEXT = 1, CF_DIB = 8
            result = u32.SetClipboardData(8, hg)
            k32.GlobalFree(hg)
            if (result):
                print("Data coppied to clipboard succesfully!")
            else:
                print("Could not set clipboard data!")
        else:
            print("Could not allocate space for clipboard data!")
        u32.CloseClipboard();
    else:
        print("Could not open clipboard!")
    return False

url = pyperclip.paste()
if (url != None):
    if (checkUrl(url)):
        print("Clipboard url: {}".format(url))
        imgUrl = getImageUrl(url)
        if (len(sys.argv) > 1):
            if (sys.argv[1] == "-u"):
                print("Scraped url: {}".format(imgUrl))
                pyperclip.copy(imgUrl)
        else:
            print("Copying image to clipboard.")
            img, size = getImage(imgUrl)
            copyImageToClipboard(img, size)
    else:
        print("Bad url! Could not continue.")
print("Script will end in {} seconds.".format(seconds))
time.sleep(seconds)
