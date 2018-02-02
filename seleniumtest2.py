from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

path_to_chromedriver = "C:\\Users\\Sohum\\Downloads\\chromedriver_win32\\chromedriver.exe" # change path as needed
#path_to_chromedriver.replace("\\","/")
browser = webdriver.Chrome(executable_path = path_to_chromedriver)

url = 'http://www.scoreboard.com/soccer/'
browser.get(url)

browser.find_element_by_link_text('England').click()
browser.find_element_by_link_text('Premier League').click()
browser.find_element_by_link_text('Archive').click()
browser.find_element_by_link_text('Premier League 2012/2013').click()

show_games = browser.find_element_by_link_text('Show more games').click()
time.sleep(5)
browser.execute_script("window.scrollTo(0, document.body.scrollHeight)")
show_games = browser.find_element_by_link_text('Show more games').click()
time.sleep(5)
browser.execute_script("window.scrollTo(0, document.body.scrollHeight)")
show_games = browser.find_element_by_link_text('Show more games').click()
time.sleep(5)
browser.execute_script("window.scrollTo(0, document.body.scrollHeight)")
show_games = browser.find_element_by_link_text('Show more games').click()

curr_week = []


curr_week.append(browser.find_elements_by_xpath('//tr[@class="even stage-finished"]').text)
curr_week.append(browser.find_elements_by_xpath('//tr[@class="odd stage-finished"]').text)


print (curr_week[0], curr_week[1])
