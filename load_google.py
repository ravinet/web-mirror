import sys
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from pyvirtualdisplay import Display
import os

options=Options()
options._binary_location = '/home/ravinent/src/out/Release/chrome'
#eliminate needing to show display of chrome loading page
#options.add_argument("--no-proxy-server")
#options.add_argument("--user-data-dir=/tmp/myprofdir")
#options.add_argument("--enable-quic")
#options.add_argument("--origin-to-force-quic-on=localhost:80")
display = Display(visible=0, size=(800,600))
display.start()
driver=webdriver.Chrome(chrome_options=options)

#load page
driver.get('http://www.mit.edu')

#get page load time
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

driver.quit()
