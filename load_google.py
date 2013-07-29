import sys
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from pyvirtualdisplay import Display
import os

#cmdline args
if (len(sys.argv) < 3):
  print "Usage: Enter chrome location, and site to fetch, congestion control\n"
  exit(5)

chrome_binary=sys.argv[1]
site_to_fetch=sys.argv[2]
cc=sys.argv[3]

options=Options()
options._binary_location = chrome_binary
#eliminate needing to show display of chrome loading page

if (cc == "quic"):
  options.add_argument("--no-proxy-server")
  options.add_argument("--user-data-dir=/tmp/myprofdir")
  options.add_argument("--enable-quic")
  options.add_argument("--origin-to-force-quic-on="+site_to_fetch.split('//')[1]+":80")

display = Display(visible=0, size=(800,600))
display.start()
driver=webdriver.Chrome(chrome_options=options)

#load page
driver.get(site_to_fetch)

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
