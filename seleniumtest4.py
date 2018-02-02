from selenium import webdriver
import re
import pickle
import numpy as np
import pandas as pd


def remove_spaces(curr_week):

    curr_week = curr_week.replace('FC Schalke 04', 'FCSchalke04')
    curr_week = curr_week.replace('1. FSV Mainz 05', '1.FSVMainz05')
    curr_week = curr_week.replace('1. FC Köln', '1.FCKöln')
    curr_week = curr_week.replace('1. FC Kaiserslautern', '1.FCKaiserslautern')
    curr_week = curr_week.replace('1899 Hoffenheim', '1899Hoffenheim')
    curr_week = curr_week.replace('Hannover 96', 'Hannover96')
    curr_week = curr_week.replace('1. FC Nürnberg', '1.FCNürnberg')
    curr_week = curr_week.replace('Bayern München', 'BayernMünchen')
    curr_week = curr_week.replace('Bor. Mönchengladbach', 'Bor.Mönchengladbach')
    curr_week = curr_week.replace('SC Paderborn 07', 'SCPaderborn07')
    curr_week = curr_week.replace('FC Ingolstadt 04', 'FCIngolstadt04')
    curr_week = curr_week.replace('SV Darmstadt 98', 'SVDarmstadt98')
    #curr_week = curr_week.replace('', '')
    
    return re.sub(r'(?<=[a-zA-Z])\s(?=[a-zA-Z])', '',curr_week).split(' ')[0]

def conv_date(date):
    date = date.split('/')
    try:
     month = int(date[0])
     day = int(date[1])
     year = int(date[2][2:])
    
    except:
     print("Exception:", date)

    #print(day, month, year)

    leap = 0
    if(year%4 == 0): leap = 1
    
    if(month == 1): return (year*365)+00+day
    if(month == 2): return (year*365)+31+day
    if(month == 3): return (year*365)+59+leap+day
    if(month == 4): return (year*365)+90+leap+day
    if(month == 5): return (year*365)+120+leap+day
    if(month == 6): return (year*365)+151+leap+day
    if(month == 7): return (year*365)+181+leap+day
    if(month == 8): return (year*365)+212+leap+day
    if(month == 9): return (year*365)+243+leap+day
    if(month == 10): return (year*365)+273+leap+day
    if(month == 11): return (year*365)+304+leap+day
    if(month == 12): return (year*365)+334+leap+day
    
    pass
    
def home_stats(data):
    stat_list = []
    
    for i in data:
        try:
            stat_list.append(re.sub(r'(?<=[a-zA-Z])\s(?=[a-zA-Z])', '',i).split(' ')[0])
        except:
            print("Error:", i)

    return stat_list

def away_stats(data):
    stat_list = []
    
    for i in data:
      try:
          stat_list.append(re.sub(r'(?<=[a-zA-Z])\s(?=[a-zA-Z])', '',i).split(' ')[2])
      except:
          print("Error:", i)

    return stat_list


path_to_chromedriver = "C:\\Users\\Sohum\\Downloads\\chromedriver_win32\\chromedriver.exe" # change path as needed
#path_to_chromedriver.replace("\\","/")
browser = webdriver.Chrome(executable_path = path_to_chromedriver)
browser2 = webdriver.Chrome(executable_path = path_to_chromedriver)

eng_home_stats_2014_15 = dict()
eng_away_stats_2014_15 = dict()

eng_home_stats_2015_16 = dict()
eng_away_stats_2015_16 = dict()

eng_home_stats_2016_17 = dict()
eng_away_stats_201_17 = dict()



for year in ['2014-2015']:
 url = 'http://info.nowgoal.com/en/League/' + year +'/36.html'
 browser.get(url)
 
 temp_home_dict = dict()
 temp_away_dict = dict()

 #Cycle through all match weeks and matches
 k = 0
 if(year == '2014-2015'): k = 6
 print(year)
 
 week_num = browser.find_elements_by_xpath("//div[@id='i_data']//td[@class ='lsm2']")[k:]
 for number, each_week in enumerate(week_num): 
  each_week.click()

  match_stats = browser.find_elements_by_xpath('//div[@class="redf"]')

  print("Week", (number+k+1))
  for e in match_stats:
   new_url = e.find_element_by_css_selector('a').get_attribute('href')   
   browser2.get(new_url)

   #Determine Home and Away Team
   home_team = remove_spaces(browser2.find_element_by_xpath("//div[@id='main']//div[@id='matchData']//div[@id='matchDIV']//div[@id='home']//span[@class='name']").text)
   away_team = remove_spaces(browser2.find_element_by_xpath("//div[@id='main']//div[@id='matchData']//div[@id='matchDIV']//div[@id='guest']//span[@class='name']").text)

   #Collect Match Statistics
   match_date = browser2.find_element_by_xpath("//div[@id='main']//div[@id='matchData']//div[@id='matchDIV']//div[@id='matchItems']//div[@class='item']//span")
   match_date_text = match_date.text.split(' ')[1][5:]
   if(len(match_date_text) < 8): print("Error:", home_team," vs ", away_team," date = ", match_date_text, "|", match_date.text); match_date_text = match_date.text.split(' ')[3]; print("Fixed: ", match_date_text)
   match_date = conv_date(match_date_text)
   

   
   match_data = browser2.find_elements_by_xpath("//div[@id='main']//div[@class='content']//table[@class='bhTable']")
   match_data = (match_data[2].text).split('\n')[1:18]

   #Make New Dict entry if it does not exist
   if((home_team,match_date) not in temp_home_dict): temp_home_dict[(home_team,match_date)] = []
   if((away_team,match_date) not in temp_away_dict): temp_away_dict[(away_team,match_date)] = []


   #Corner Kicks, Yellow Cards, Shots, Shot on Goal, Off Target, Blocked, Possession, Pass, Pass Success, Fouls, Offsides, Heads, Head Success, Saves, Tackles, Substitutions, Dribbles
   temp_home_dict[(home_team,match_date)].append(home_stats(match_data))
   temp_away_dict[(away_team,match_date)].append(away_stats(match_data))


 print(year, " | ", len(temp_home_dict))
 print(year, " | ", len(temp_away_dict))

 if(year == '2014-2015'): eng_home_stats_2014_15 = temp_home_dict; eng_away_stats_2014_15 = temp_away_dict
 if(year == '2015-2016'): eng_home_stats_2015_16 = temp_home_dict; eng_away_stats_2015_16 = temp_away_dict
 if(year == '2016-2017'): eng_home_stats_2016_17 = temp_home_dict; eng_away_stats_2016_17 = temp_away_dict
     

#Save Scraped Data:

with open('england_hist_data_2014_15.pickle', 'wb') as f:
    pickle.dump([eng_home_stats_2014_15, eng_away_stats_2014_15], f)

 

###################
#BETA For 1 Match  
###################

"""
week_num = browser.find_elements_by_xpath("//div[@id='i_data']//td[@class ='lsm2']")
week_num[4].click()

#Open Match Stats window in a new window
match_stats = browser.find_element_by_xpath('//div[@class="redf"]')
new_url = match_stats.find_element_by_css_selector('a').get_attribute('href')   
print(new_url)
browser2.get(new_url)

#Determine Home and Away Team
home_team = remove_spaces(browser2.find_element_by_xpath("//div[@id='main']//div[@id='matchData']//div[@id='matchDIV']//div[@id='home']//span[@class='name']").text)
away_team = remove_spaces(browser2.find_element_by_xpath("//div[@id='main']//div[@id='matchData']//div[@id='matchDIV']//div[@id='guest']//span[@class='name']").text)

#Collect Match Statistics
match_date = browser2.find_element_by_xpath("//div[@id='main']//div[@id='matchData']//div[@id='matchDIV']//div[@id='matchItems']//div[@class='item']//span")
match_data = browser2.find_elements_by_xpath("//div[@id='main']//div[@class='content']//table[@class='bhTable']")
match_data = (match_data[2].text).split('\n')[1:18]


eng_home_stats_2014_15 = dict()
eng_away_stats_2014_15 = dict()

#Make New Dict entry if it does not exist
if(home_team not in eng_home_stats_2014_15): eng_home_stats_2014_15[home_team] = []
if(away_team not in eng_away_stats_2014_15): eng_away_stats_2014_15[away_team] = []


#Corner Kicks, Yellow Cards, Shots, Shot on Goal, Off Target, Blocked, Possession, Pass, Pass Success, Fouls, Offsides, Heads, Head Success, Saves, Tackles, Substitutions, Dribbles
eng_home_stats_2014_15[home_team].append(home_stats(match_data))
eng_away_stats_2014_15[away_team].append(away_stats(match_data))



print(home_team)
print(away_team)
print(match_date.text.split(' ')[1][5:])
print(eng_home_stats_2014_15[home_team][0])
print(eng_away_stats_2014_15[away_team][0])
"""

"""
for year in ['2011-2012', '2012-2013', '2013-2014', '2014-2015', '2015-2016', '2016-2017']:
 
 for country, num_teams in [['eng-premier-league-', 20], ['esp-primera-division-', 20], ['bundesliga-', 18], ['ita-serie-a-', 20] , ['fra-ligue-1-', 20]]:

  url = 'http://www.worldfootball.net/all_matches/' + country + year #eng-premier-league-2011-2012/''&pmtype=bygameweek' 
  browser.get(url)
  
  year_results = browser.find_elements_by_xpath('//div[@class="box"]//tr') #[int(num_teams/2)+i].text #get_attribute("innerHTML")

  for curr_match in year_results:

    curr_week = curr_match.text
    #print(curr_week)
    
    curr_week = remove_spaces(curr_week).split()
    match_date = ''

    if(len(curr_week) == 7):
     match_date = conv_date(curr_week.pop(0))
     if(match_date not in track_dates): track_dates.append(match_date)
     #print(curr_week)
    if(len(curr_week) == 6):
     if(match_date not in results): results[match_date] = []
     
     try:
      # Home team, Away Team, (Halftime, Score), (Fulltime, Score)   
      results[match_date].append([curr_week[1],curr_week[3], (int(curr_week[5][1]), int(curr_week[5][3])), ((int(curr_week[4].split(':')[0]), int(curr_week[4].split(':')[1])))])
     except:
      print("Exception:", curr_week)


    match_date = conv_month(curr_week[1], curr_week[2], '16')
    if(match_date not in track_dates): track_dates.append(match_date)

    if(match_date not in results): results[match_date] = []

    try:   
     results[match_date].append([curr_week[4], curr_week[6], (int(curr_week[10][1]), int(curr_week[10][3])), (int(curr_week[7]),int(curr_week[9]))])
    except:
     pass
     #print("Error: ", curr_week)


for i in sorted(track_dates)[0:5]:
    print(i," | ", results[i])

for i in sorted(track_dates)[(len(track_dates)-5):]:
    print(i," | ", results[i])

#Save Scraped Data:

with open('match_dates_and_scores.pickle', 'wb') as f:
    pickle.dump([results, track_dates], f)
"""

#browser.quit()
