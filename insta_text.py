################################
##### Instagram crawler for text
################################


## import module

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from bs4 import BeautifulSoup as bs

import time
import sys
from imp import reload

import re

from urllib.request import urlopen
import requests
import datetime 
import wget
import html2text

import json
from pandas.io.json import json_normalize

import pandas as pd
import numpy as np

from random import *


## Instagram Sign in 

reload(sys)
#sys.setdefaultencoding('utf-8') python3에는 디폴트라 굳이 설정 ㄴㄴ


targetInstagramUrl = 'https://www.instagram.com/accounts/login/?source=auth_switcher'

options = webdriver.ChromeOptions()
#mobile_emulation = { "deviceName": "Nexus 5" }
#options.add_experimental_option("mobileEmulation", mobile_emulation)

login_id = input('put your login id : ')
login_pw = input('put your login password : ')

driver = webdriver.Chrome('chromedriver.exe', chrome_options=options)
driver.get(targetInstagramUrl)

#login process ----------------------------------------------------------------- start
#login process ----------------------------------------------------------------- start
time.sleep(2)

driver.find_elements_by_name("username")[0].send_keys(login_id)
driver.find_elements_by_name("password")[0].send_keys(login_pw)

driver.find_element_by_xpath("//form/div[4]/button").submit()

time.sleep(3)

driver.find_element_by_xpath("/html/body/div[3]/div/div/div[3]/button[2]").click()
#login process ----------------------------------------------------------------- end
#login process ----------------------------------------------------------------- end


## Hashtag Search

hashtag = input('What do you wanna search for : ')
driver.get('https://www.instagram.com/explore/tags/'+ hashtag)


## Get links of posts

links = []
last_height = driver.execute_script("return document.body.scrollHeight") # Get scroll height

while True:
    
    source = driver.page_source
    data = bs(source, 'html.parser')
    body = data.find('body')
    script = body.find('span')

    for link in script.findAll('a'):
        if re.match("/p", link.get('href')):
            links.append('https://www.instagram.com'+link.get('href'))
   
    # Scroll down to bottom        
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        
    # Wait to load page
    time.sleep(uniform(3.0, 5.0))

    # Calculate new scroll height and compare with last scroll height
    new_height = driver.execute_script("return document.body.scrollHeight")
    
    if new_height == last_height:
        break
    last_height = new_height
    

links = list(set(links))


## Web Scraping(json) -> DataFrame

result = pd.DataFrame()

for i in range(len(links)) : 
    try:

        page = urlopen(links[i]).read()
        data = bs(page, 'html.parser')
        body = data.find('body')
        script = body.find('script')
        raw = script.text.strip().replace('window._sharedData =', '').replace(';', '')
        json_data=json.loads(raw)

        posts =json_data['entry_data']['PostPage'][0]['graphql']
        posts = json.dumps(posts)
        posts = json.loads(posts)

        x = pd.DataFrame.from_dict(json_normalize(posts), orient='columns') 
        x.columns =  x.columns.str.replace("shortcode_media.", "")
        result=result.append(x)
    
    except:
        np.nan
        

result = result.drop_duplicates(subset = 'shortcode')
result.index = range(len(result.index))


## Make DataFrame into CSV

result.to_csv('myfile.csv', encoding = 'UTF-8-sig') #엑셀로 열 것 같아서.. ㅋㅋ

