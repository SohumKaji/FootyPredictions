from selenium import webdriver
import re
import pickle
import time
from itertools import zip_longest
import pandas as pd
import os
from selenium.webdriver.common.action_chains import ActionChains


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

#Converts the date into days after the year 2000
#(arbitrary standardization that, in addition to uniformity, allows for arithmetic in terms of days)
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


#Returns the stats for the home team as an array    
def home_stats(data, home_name, away_name):
    stat_list = []
    error_num = 0
    
    for i in data:
        try:
           stat_list.append(i[0])
        except:
           error_num +=1
          
    #if(error_num != 0): file.write(str(home_name)+ ' vs ' + str(away_name) + "Home Stats Error x" + str(error_num) + '\n')

    return stat_list

#Returns the stats for the away team as an array
def away_stats(data, home_name, away_name):
    stat_list = []
    error_num = 0
    
    for i in data:
      try:
          stat_list.append(i[2])
      except:
          error_num +=1
          
    #if(error_num != 0): file.write(str(home_name)+ ' vs ' + str(away_name) + "Away Stats Error x" + str(error_num) + '\n')

    return stat_list

#Make Directories
if not os.path.exists('NN'):
    os.makedirs('NN')
"""
if not os.path.exists('data'):
    os.makedirs('data')
if not os.path.exists('data/half_time_data'):
    os.makedirs('data/half_time_data')
    
data_path = 'data/half_time_data/'

for direc in ['14-15', '15-16', '16-17']:
  if not os.path.exists(data_path+direc):
    os.makedirs(data_path+direc)
    for country in ['eng', 'esp', 'ger', 'ita', 'fra']:  
      os.makedirs(data_path+direc+'/'+country)
      os.makedirs(data_path+direc+'/'+country+'/home')
      os.makedirs(data_path+direc+'/'+country+'/away')
"""    

path_to_chromedriver = "C:\\Users\\Sohum\\Downloads\\chromedriver_win32_2\\chromedriver.exe"
browser = webdriver.Chrome(executable_path = path_to_chromedriver)
browser.maximize_window()
browser.implicitly_wait(5)

home_path = 'NN_'
away_path = 'NN_'

#browser2 = webdriver.Chrome(executable_path = path_to_chromedriver)

collected_stats = ['BallPossession', 'ShotsonGoal', 'ShotsoffGoal', 'BlockedShots', 'FreeKicks', 'CornerKicks','Offsides', 'Throw-in', 'GoalkeeperSaves', 'Fouls']
#final_stats = collected_stats + ['GS', 'GA']
#collected_stats = [elem.lower() for elem in collected_stats]

home_df = None
away_df = None
first = True

for year in ['2014-2015', '2015-2016', '2016-2017']: #'2014-2015', '2015-2016', '2016-2017'
    
  #if(year == '2014-2015'): error_file = open('data/half_time_data/14-15/error_log.txt', 'w')
  #if(year == '2015-2016'): error_file = open('data/half_time_data/15-16/error_log.txt', 'w')
  #if(year == '2016-2017'): error_file = open('data/half_time_data/16-17/error_log.txt', 'w')
  
  for country, league in [['england', 'premier-league-'], ['spain', 'laliga-'], ['germany', 'bundesliga-'], ['italy', 'serie-a-'], ['france', 'ligue-1-']]:  #
  
    """
    if((country =='italy') and (year == '2016-2017')):
      url = 'http://www.flashscore.com/soccer/'+ country + '/' + league[:-1] +'/results/'
    else:
      url = 'http://www.flashscore.com/soccer/'+ country + '/' + league + year + '/results/'
    """
    url = 'http://www.flashscore.com/soccer/'+ country + '/' + league + year + '/results/'
    browser.get(url)
    #print(country + year)

    #Requires clicking the 'Show more matches' link 3 times to see all of the matches
    for i in range(3):
      time.sleep(5)
      show_all = browser.find_elements_by_xpath('//div[@class="container"]//div[@class="content"]//div[@id="tc"]//div[@id="mc"]//div[@id="fsbody"]//table[@id="tournament-page-results-more"]')
      actions = ActionChains(browser)
      actions.move_to_element(show_all[0]).perform()
      #show_all[0].location_once_scrolled_into_view
      #time.sleep(5)
      show_all[0].click()
      time.sleep(1)

    time.sleep(5)
    year_elem = browser.find_elements_by_xpath('//div[@class="container"]//div[@class="content"]//div[@id="tc"]//div[@id="mc"]//div[@id="fsbody"]//table[@class="soccer"]//tbody//tr')
    #new_url = year_elem[0].find_elements_by_css_selector('a')
    #print(len(year_elem))
    #year_results = [elem.text for elem in year_elem]
    #print(year_results)
    year_elem = [elem for elem in year_elem if len(elem.text)>10]
    print(country, year, len(year_elem))
    for elem in reversed(year_elem): 
      year_results = (elem.text).split('\n')
      match_date, home_name, away_name, match_score = year_results[0], year_results[1], year_results[2], year_results[3]
      
      #Format Date
      match_date = match_date.split('.')
      if(int(match_date[1]) > 6):match_date = match_date[1]+'/'+match_date[0] + '/' + year.split('-')[0]
      else: match_date = match_date[1]+'/'+match_date[0] + '/' + year.split('-')[1]
      match_date = conv_date(match_date)

      #Format Team Names
      home_name = remove_spaces(home_name)
      away_name = remove_spaces(away_name)

      #print(match_date, home_name, away_name, match_score)

      #Collect Half-time data
      curr_window = None
      while curr_window == None:
        curr_window = browser.current_window_handle

      elem.click()
      new_window = None
      while new_window == None:
        for window in browser.window_handles:
          if window != curr_window:
            new_window = window
            break
      browser.switch_to.window(new_window)
      next_link = browser.find_element_by_link_text("Statistics")
      next_link.click()

      try:
        next_link = browser.find_element_by_link_text("1st Half")
        next_link.click()
        statistics = browser.find_elements_by_xpath('//body[@id="top"]//div[@id="detail"]//div[@id="detcon"]//div[@id="content-all"]//div[@id="tab-match-statistics"]//div[@id="statistics-content"]' + \
                                                    '//div[@id="tab-statistics-1-statistic"]//table[@class="parts"]//tbody//tr')
      except:
          print("No Halftime Data:", home_name, away_name, year)
          browser.close()
          browser.switch_to.window(browser.window_handles[0])
          
          continue
        
      match_data = []
      final_data = ['None'] * len(collected_stats)
      
      for i, stats in enumerate(statistics):
        curr_match_data = re.sub(r'(?<=[a-zA-Z])\s(?=[a-zA-Z])', '', stats.text).split('\n')
        match_data.append(curr_match_data)

        #print(curr_match_data)
        
        if(curr_match_data[1] == 'BallPossession'): curr_match_data[0] = curr_match_data[0].replace('%', ''); curr_match_data[2] = curr_match_data[2].replace('%', ''); 
        if(curr_match_data[1] in collected_stats): final_data[collected_stats.index(curr_match_data[1])] = curr_match_data


      #Read in the team data so far
      country_dir = '/'+country[0:3]
      if(country == 'spain'): country_dir = '/esp'

        

      """                                                        
      if os.path.isfile(home_path):
        home_df = pd.read_csv(home_path, index_col=0)
      else:
        home_df = pd.DataFrame()

      if os.path.isfile(away_path):
        away_df = pd.read_csv(away_path, index_col=0)
      else:
        away_df = pd.DataFrame()
      """

      #Add new entry
      home_stats_final = home_stats(final_data, home_name, away_name)
      away_stats_final = away_stats(final_data, home_name, away_name)

      if(len(home_stats_final) != len(collected_stats)): print(home_name, home_stats_final); #home_stats_final = ['None'] * len(collected_stats) 
      if(len(away_stats_final) != len(collected_stats)): print(away_name, away_stats_final); #away_stats_final = ['None'] * len(collected_stats)

      #home_df.index = list(home_df.index).append(str(match_date))
      #away_df.index = away_df.index.append(str(match_date))
    
      #home_df = home_df.append(pd.DataFrame([home_stats_final], index = [str(match_date)]))
      #away_df = away_df.append(pd.DataFrame([away_stats_final], index = [str(match_date)]))

      #print(home_stats_final)
      #print(away_stats_final)

      #home_stats_final.append(match_score.split(' : ')[0])
      #home_stats_final.append(match_score.split(' : ')[1])

      #away_stats_final.append(match_score.split(' : ')[1])
      #away_stats_final.append(match_score.split(' : ')[0])
      
      if(not first):
          home_df = home_df.append(pd.DataFrame([home_stats_final], columns = collected_stats, index = [str(home_name)+'_'+str(match_date)]))
          away_df = away_df.append(pd.DataFrame([away_stats_final], columns = collected_stats, index = [str(away_name)+'_'+str(match_date)]))
      else:
          home_df = (pd.DataFrame([home_stats_final], columns = collected_stats, index = [str(home_name)+'_'+str(match_date)]))
          away_df = (pd.DataFrame([away_stats_final], columns = collected_stats, index = [str(away_name)+'_'+str(match_date)]))
          first = False
          

         
      browser.close()
      browser.switch_to.window(browser.window_handles[0])

         
      #time.sleep(5)
      #browser2.switch_to_window(browser.window_handles[-1])
      #browser2.close()
      """
      time.sleep(1)
      b_wind = browser.window_handles
      print(b_wind)
      browser2.switch_to_window(b_wind[1])
      
      new_url = (browser2.current_url).split('#') + '#match-statistics;1'
      browser2.close()
      browser2.switch_to_window(browser2.window_handles[0])
      browser2.get(new_url)
      """

    #Update the team data so far (essentially "checkpoints")
    home_df.to_csv('NN/prev/'+home_path + country + year +'_home.csv')
    away_df.to_csv('NN/prev/'+away_path + country + year +'_away.csv') 
       
#Final Data
home_df.to_csv('NN/NN_home.csv')
away_df.to_csv('NN/NN_away.csv') 

browser.quit()
