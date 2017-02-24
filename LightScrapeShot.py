import pyperclip
import re
from selenium import webdriver
import time

seconds = 2

def checkUrl(url):
    r = re.compile('http://p*')
    if (r.match(url) != None):
        return True
    return False

def getImageUrl(url):
    driver = webdriver.Firefox()
    driver.set_window_position(10000,0) #let's move the browser window out of the way
    driver.set_page_load_timeout(5) #let's not wait for a full page to load
    try:
        driver.get(url)
    except: #timeout throws an exception which we have to ignore
        pass
    #page is loaded; let's switch to the iframe and extract our url
    frame = driver.find_element_by_id('image-iframe')
    driver.switch_to_frame(frame)
    imgUrl = driver.find_element_by_id('image-img').get_attribute('src')
    driver.quit()
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
