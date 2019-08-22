from selenium import webdriver
import time

# As my chrome browser is located in a non default location
options = webdriver.ChromeOptions()
options.binary_location = "/Volumes/DATA/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
chrome_driver_binary = "/usr/local/bin/chromedriver"
driver = webdriver.Chrome(chrome_driver_binary, chrome_options=options)

driver.get('http://www.google.com/xhtml')
time.sleep(5) # Let the user actually see something!
search_box = driver.find_element_by_name('q')
search_box.send_keys('ChromeDriver')
search_box.submit()
time.sleep(5) # Let the user actually see something!
driver.quit()