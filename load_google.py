import sys
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from pyvirtualdisplay import Display
import os

#folder = sys.argv[1]
#print folder
options=Options()
options._binary_location = '/home/skype-alpha/July3rdGoogleMeeting/src/out/Release/chrome'
options.add_argument("--no-proxy-server")
options.add_argument("--user-data-dir=/tmp/myprofdir")
options.add_argument("--enable-quic")
options.add_argument("--origin-to-force-quic-on=localhost:80")
display = Display(visible=0, size=(800,600))
display.start()
driver=webdriver.Chrome(chrome_options=options)
#timestart = time.time()
driver.get('http://localhost:80/www.mit.edu/index.html')
#timeend = time.time()
#loadtime = timeend - timestart
#print loadtime

navigationStart = driver.execute_script("return window.performance.timing.navigationStart")
responseStart = driver.execute_script("return window.performance.timing.responseStart")
domComplete = driver.execute_script("return window.performance.timing.domComplete")
responseEnd = driver.execute_script("return window.performance.timing.responseEnd") 
backendPerformance = responseStart - navigationStart
frontendPerformance = domComplete - responseStart
alttotal = responseEnd - navigationStart
print "Back End: %s" % backendPerformance
print "Front End: %s" % frontendPerformance
print "Alt is %s" % alttotal
#time.sleep(5) # Let the user actually see something!
#search_box = driver.find_element_by_name('q')
#search_box.send_keys('Lorem epsum')
#search_box.submit()
#time.sleep(5) # Let the user actually see something!
driver.quit()
