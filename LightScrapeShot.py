import ctypes
import re
from selenium import webdriver
import time
import sys

CF_TEXT = 1
seconds = 5
GMEM_MOVEABLE = 0x0002

k32 = ctypes.windll.kernel32
u32 = ctypes.windll.user32
msvcrt = ctypes.windll.msvcrt

def readFromClipboard():
    if (u32.OpenClipboard(0)):
        if (u32.IsClipboardFormatAvailable(CF_TEXT)):
            data = u32.GetClipboardData(CF_TEXT)
            data_locked = k32.GlobalLock(data)
            text = ctypes.c_char_p(data_locked)
            k32.GlobalUnlock(data_locked)
            print("Data coppied from clipboard succesfully!")
        else:
            print("Data in clipboard is not text!")
            return None
        u32.CloseClipboard();
    else:
        print("Could not open clipboard!")
        return None
    return text.value.decode("utf-8")

def copyToClipboard(string):
    if (u32.OpenClipboard(0)):
        u32.EmptyClipboard()
        hg = k32.GlobalAlloc(GMEM_MOVEABLE, len(string)+1)
        if (hg != None):
            ctypes.memmove(k32.GlobalLock(hg), string.encode('utf-8'), len(string)+1)
            k32.GlobalUnlock(hg)
            result = u32.SetClipboardData(CF_TEXT, hg)
            k32.GlobalFree(hg)
            if (result):
                print("Data coppied to clipboard succesfully!")
                return True
            else:
                print("Could not set clipboard data!")
        else:
            print("Could not allocate space for clipboard data!")
        u32.CloseClipboard();
    else:
        print("Could not open clipboard!")
    return False

def checkUrl(url):
    r = re.compile('http://p*')
    if (r.match(url) != None):
        return True
    return False

def getImageUrl(url):
    driver = webdriver.Firefox()
    driver.set_window_position(0,0)
    driver.set_page_load_timeout(5) #let's not wait for a full page to load
    try:
        driver.get(url)
    except: #timeout throws an exception which we have to ignore
        pass
    frame = driver.find_element_by_id('image-iframe')
    driver.switch_to_frame(frame)
    imgUrl = driver.find_element_by_id('image-img').get_attribute('src')
    driver.quit()
    return imgUrl

url = readFromClipboard()
if (url != None):
    if (checkUrl(url)):
        print("Found url: {}".format(url))
        imgUrl = getImageUrl(url)
        copyToClipboard(imgUrl)
    else:
        print("Bad url! Could not continue.\nClipboard content: {}".format(url))
print("Script will end in {} seconds.".format(seconds))
time.sleep(seconds)
