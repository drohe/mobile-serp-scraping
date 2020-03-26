import csv
import json
import os
import requests
import urllib
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from queryArray import queries #This is a .py file with queries = [] and your list of queries (as strings) inside the array

### START THE SET UP YOUR CHROME DRIVER

# The following two commented lines are where this was tested swapping the userAgent. These did NOT have any Interesting Finds in the results (not identified for a propr mobile SERP)
#"deviceMetrics": { "width": 360, "height": 640, "pixelRatio": 3.0 },
#"userAgent": "Mozilla/5.0 (Linux; Android 4.2.1; en-us; Nexus 5 Build/JOP40D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 Mobile Safari/535.19" }
mobile_emulation = {'deviceName': 'Pixel 2'}
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)
browser = webdriver.Chrome(r'c:/python/chromedriver/chromedriver.exe',options=chrome_options) # YOU WILL NEED TO INPUT THE PATH TO YOUR CHROMEDRIVER EXECUTABLE FILE IN THE FIRST ARGUMENT. WINDOWS OS MAY REQUIRE USING r BEFORE THE QUOTES AND PUTTING THE ACTUAL .EXE FILE IN THE PATH

### END CHROME DRIVER SETUP

### START THE SET UP FOR YOUR OUTPUTS
projectOutput = input('Enter a name for this project folder: ') # YOU WILL BE PROMPTED IN THE COMMAND LINE TO NAME YOUR PROJECT
os.mkdir(projectOutput) # A NEW FOLDER WHERE ALL OF THE SCREENSHOTS WILL BE SAVED BASED ON YOUR PROJECT NAME
outputcsv = os.path.join(os.path.dirname(projectOutput), projectOutput +'.csv') #the path for your CSV file
## Creating your CSV file
f = csv.writer(open(outputcsv, "w+", newline="\n", encoding="utf-8"))
f.writerow(["Query","Interesting Finds\?", "Finds Links"])
### END THE OUTPUTS SETUP

### OPEN GOOGLE.COM VIA YOUR CHROME DRIVER (NAMED BROWSER) AND RESIZE THE WINDOW (TIED TO THE PIXEL 2) TO HELP WITH SCREENSHOTS
browser.get('https://www.google.com')
browser.set_window_size(360,640)

### BEGIN THE LOOP THROUGH EACH QUERY OF YOUR QUERIES ARRAY
for query in queries:
  elem = browser.find_element_by_name("q") #Find the input field to have Selenium type in the query
  elem.clear()
  elem.send_keys(query) #Selenium types in the query
  elem.send_keys(Keys.RETURN)
  element = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.ID, "botstuff")) # the #botstuff loads at the bottom of the SERP, so this helps to ensure the page is fully loaded before scraping
    )
  body = browser.find_elements_by_tag_name('body')[0] #This is used for screenshots further down

#Interesting Finds
  if browser.find_elements_by_css_selector('g-card.I7zR5'):
     interestingFinds = True
     findsCode = browser.find_elements_by_css_selector('g-card.I7zR5')
     findsLinks = []
     for card in findsCode:
         links = card.find_elements_by_css_selector('div.mnr-c div div div a')
         for link in links:
             href = link.get_attribute('href')
             amp = False
             if link.get_attribute('class'):
                 classes = link.get_attribute('class')
                 if 'amp_r' in classes:
                     amp = True
             link = {'link': href, 'amp': amp}
             findsLinks.append(link)
  else:
    interestingFinds = False
    findsLinks = ""

  f.writerow([query,interestingFinds,findsLinks]) #create row in CSV


### START SCREENSHOTS
  imageName = query.replace(' ','-')
  browser.save_screenshot(os.path.join(projectOutput,imageName + '.png'))
  totalLength = body.size['height']
  lastClip = totalLength -500
  clipsNeeded = round(lastClip/500)
  i = 0
  clipHeight = 500
  while i < clipsNeeded:
    browser.execute_script('window.scrollTo(360,arguments[0])',clipHeight)
    clipNum = str(i)
    browser.save_screenshot(os.path.join(projectOutput,imageName + clipNum + '.png'))
    clipHeight = clipHeight + 500
    i += 1
