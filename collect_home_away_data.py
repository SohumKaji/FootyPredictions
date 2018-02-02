from selenium import webdriver
import re
import pickle
import pandas as pd

###############################################
#Input the direct path to your chromdriver.exe#
###############################################

path_to_chromedriver = "C:\\Users\\Sohum\\Downloads\\chromedriver_win32\\chromedriver.exe"


#Removes spaces in names/labels and use .split to differentiate them from numeric entries
#Format team names with numeric/unexpected alphabets in the name as well
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

    curr_week = curr_week.replace('(WBA)', '')
    
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

#Finds the stats we are looking for and logs in the errors file if they are unable to be found
def check_data(data, home_team, away_team, file, collected_stats, missing_val, total_errors):
    final_data = ['None'] * len(collected_stats)
    #print(final_data)

    for elem in data:
        if((elem[0].isdigit())):
            home_stat, elem_name, away_stat = re.sub(r'(?<=[a-zA-Z])\s(?=[a-zA-Z])', '',elem).split(' ') #[1].lower()
            #print("###########", home_stat, elem_name, away_stat)

            elem_name = elem_name.lower()


            #Formatting for the SGD classifier
            if(elem_name == 'heads'): elem_name = 'headtheball'

            if(elem_name == 'possession'): home_stat = home_stat.replace('%', ''); away_stat = away_stat.replace('%', '')
            if(elem_name == 'pass'): home_pass = float(home_stat); away_pass = float(away_stat)
            if(elem_name == 'passsuccess'):
              if(home_stat[-1] == '%'): home_stat = home_stat.replace('%', ''); away_stat = away_stat.replace('%', '')
              elif(home_stat != 'None' and home_stat != 0 and away_stat != 'None' and away_stat != 0):
                  home_stat = 100*float(home_stat)/home_pass
                  away_stat = 100*float(away_stat)/away_pass
            
            if(elem_name in collected_stats): final_data[collected_stats.index(elem_name)] = str(home_stat)+' '+str(elem_name)+' '+str(away_stat)

    for i, elem in enumerate(final_data):
        if(elem == 'None'):
            file.write(str(home_team)+' vs ' + str(away_team) + " | Missing Val: " + str(collected_stats[i] + '\n'))
            total_errors +=1
            if(collected_stats[i] in missing_val):
                missing_val[collected_stats[i]] += 1
                #print("Missing Val Updated: ", collected_stats[i])
            else:
                missing_val[collected_stats[i]] = 1
                #print("Missing Val Created: ", collected_stats[i])

    return final_data, missing_val, total_errors

#Returns the stats for the home team as an array    
def home_stats(data, home_team, away_team, file):
    stat_list = []
    error_num = 0
    
    for i in data:
        if(i == 'None'):
            stat_list.append(i)
        else:
          try:
             stat_list.append(re.sub(r'(?<=[a-zA-Z])\s(?=[a-zA-Z])', '',i).split(' ')[0])
          except:
             error_num +=1
          
    #if(error_num != 0): file.write(str(home_team)+ ' vs ' + str(away_team) + "Home Stats Error x" + str(error_num) + '\n')

    if(len(stat_list)<16): print(home_team, stat_list)       

    return stat_list

#Returns the stats for the away team as an array
def away_stats(data, home_team, away_team, file):
    stat_list = []
    error_num = 0
    
    for i in data:
      if(i == 'None'):
        stat_list.append(i)
      else:
        try:
          stat_list.append(re.sub(r'(?<=[a-zA-Z])\s(?=[a-zA-Z])', '',i).split(' ')[2])
        except:
          error_num +=1
          
    #if(error_num != 0): file.write(str(home_team)+ ' vs ' + str(away_team) + "Away Stats Error x" + str(error_num) + '\n')
    if(len(stat_list)<16): print(away_team, stat_list)       

    return stat_list


#Set up our two browser windows
browser = webdriver.Chrome(executable_path = path_to_chromedriver)
browser2 = webdriver.Chrome(executable_path = path_to_chromedriver)


#Vars that control which stats are collected
collected_stats = ['Possession', 'Fouls', 'Shots', 'ShotsonGoal', 'OffTarget', 'CornerKicks', 'YellowCards', 'Headtheball', 'HeadSuccess', 'Saves', 'Blocked', 'Tackles', 'Dribbles', 'Throwins', 'Pass', 'PassSuccess']
collected_stats = [elem.lower() for elem in collected_stats]
req_data = "TechStatistics"
main_df = pd.DataFrame()

for year in ['2014-2015', '2015-2016', '2016-2017']: #

 #Error file for each year   
 error_file = open('data/full_match_data/'+year[2:4]+'-'+year[7:]+'/'+'home_away_data_error_log_'+year[2:4]+'_'+year[7:]+'.txt', 'w')
 total_errors = 0
 league_matches = dict()
 missing_val = dict()

 
 for country, ext in [['eng', '36'], ['ita','34'], ['esp','31'], ['ger', '8'], ['fra', '11']]: #  
    
  error_file.write('------------------------\n')
  error_file.write(str(country) + ', ' + str(year) + '\n')
  error_file.write('------------------------\n')
  print('\n' + str(country) + str(year))
  print("------------------------")
 

  url = 'http://info.nowgoal.com/en/League/' + year +'/' + ext +'.html'
  browser.get(url)
 
  #temp_home_dict = dict()
  #temp_away_dict = dict()
  home_df = pd.DataFrame()
  away_df = pd.DataFrame()

  #Cycle through all match weeks and matches
  k = 0
  if(year == '2014-2015'): k = 6
 
  try:
   week_num = browser.find_elements_by_xpath("//div[@id='i_data']//td[@class ='lsm2']")[k:]
  except:
   error_file.write("Could not find data for 'weeks' \n")
   total_errors+=1
  
  for number, each_week in enumerate(week_num): 
   each_week.click()

   match_stats = browser.find_elements_by_xpath('//div[@class="redf"]')

   error_file.write("\nWeek" + str(number+k+1)+'\n')
   for e in match_stats:
    new_url = e.find_element_by_css_selector('a').get_attribute('href')   
    browser2.get(new_url)

    #Determine Home and Away Team
    try:
     home_team = remove_spaces(browser2.find_element_by_xpath("//div[@id='main']//div[@id='matchData']//div[@id='matchDIV']//div[@id='home']//span[@class='name']").text)
     away_team = remove_spaces(browser2.find_element_by_xpath("//div[@id='main']//div[@id='matchData']//div[@id='matchDIV']//div[@id='guest']//span[@class='name']").text)
    except:
     error_file.write("Could not find data for: " + str(new_url) + '\n')
     total_errors+=1
     continue

    #Collect Match Statistics
    #Two formats are used on nowgoal, so first try checks to see if the first style works. Sometimes the first method will yield no data and throw an exception,
    #Sometimes it will have incorrect data, that's the reason for the odd try/except/continue and then the if statement following
    match_date_text = None
    try: 
     match_date = browser2.find_element_by_xpath("//div[@id='main']//div[@id='matchData']//div[@id='matchDIV']//div[@id='matchItems']//div[@class='item']//span")
     match_date_text = match_date.text.split(' ')[1][5:]
    except:
     continue
    if(len(match_date_text) < 8): match_date_text = match_date.text.split(' ')[3] #print("Error:", home_team," vs ", away_team," date = ", match_date_text, "|", match_date.text); match_date_text = match_date.text.split(' ')[3]; print("Fixed: ", match_date_text)
    match_date = conv_date(match_date_text)
   

   
    match_data = browser2.find_elements_by_xpath("//div[@id='main']//div[@class='content']//table[@class='bhTable']")

    #determine formatting of match data
    data_index = None    
    for i, elem in enumerate(match_data):
        #print(re.sub(r'[^a-zA-Z]', '',elem.text).split(' ')[0][:len(req_data)])
        if(re.sub(r'[^a-zA-Z]', '',elem.text).split(' ')[0][:len(req_data)] == req_data): data_index = i

    #if(data_index == None): print("\nNo Data Error!!", home_team, away_team," | ", re.sub(r'(?<=[a-zA-Z])\s(?=[a-zA-Z])', '',match_data[2].text[0]).split(' '), "\n")

    try:
     match_data = (match_data[data_index].text).split('\n')
    except:
     error_file.write("Split Data Exception: " + str(home_team) + ' vs ' + str(away_team) + ' | ' + str(match_data[0].text.split(' ')) + '\n') #, match_data[1].text, match_data[2].text)
     total_errors+=1

    try:
     match_data, missing_val, total_errors = check_data(match_data, home_team, away_team, error_file, collected_stats, missing_val, total_errors)
    except:
     error_file.write("Check Data Exception: " + str(home_team) + ' vs ' + str(away_team) +' | ' + str(match_data) + '\n') #, match_data[1].text, match_data[2].text)
     total_errors+=1

    #Make New Dict entry if it does not exist
    #if((home_team,match_date) not in temp_home_dict): temp_home_dict[(home_team,match_date)] = []
    #if((away_team,match_date) not in temp_away_dict): temp_away_dict[(away_team,match_date)] = []


    #Corner Kicks, Yellow Cards, Shots, Shot on Goal, Off Target, Blocked, Possession, Pass, Pass Success, Fouls, Offsides, Heads, Head Success, Saves, Tackles, Substitutions, Dribbles
    #temp_home_dict[(home_team,match_date)].append(home_stats(match_data, home_team, away_team, error_file))
    #temp_away_dict[(away_team,match_date)].append(away_stats(match_data, home_team, away_team, error_file))
    #print(home_stats(match_data, home_team, away_team, error_file), '\n')
    #print(collected_stats)
    home_stats_final = home_stats(match_data, home_team, away_team, error_file)
    away_stats_final = away_stats(match_data, home_team, away_team, error_file)

    if(len(home_stats_final) != len(collected_stats)): home_stats_final = ['None'] * len(collected_stats); print(home_team, away_team, match_date)
    if(len(away_stats_final) != len(collected_stats)): away_stats_final = ['None'] * len(collected_stats); print(home_team, away_team, match_date)

    #print([home_stats_final])
    #print([away_stats_final])
    
    home_df = home_df.append(pd.DataFrame([home_stats_final], columns = collected_stats, index = [home_team+'_'+str(match_date)]))
    away_df = away_df.append(pd.DataFrame([away_stats_final], columns = collected_stats, index = [away_team+'_'+str(match_date)]))
    #print(home_df)
    #print(away_df)
    

    #if(match_stats.index(e) == 5): print(home_stats(match_data)); print(away_stats(match_data))

  #Output to console, describes the year/total number of entries for that year (for each league)
  print(year, " | ", home_df.shape)
  print(year, " | ", away_df.shape)
  league_matches[country] = country + ", " + year + " | " + 'home: '+str(home_df.shape[0]) + " | " + 'away: '+str(away_df.shape[0])


  
  #Save Scraped Data:
  #with open('data/full_match_data/'+year[2:4]+'-'+year[7:]+'/'+country+'_hist_data_'+year[2:4]+'_'+year[7:]+'.pickle', 'wb') as f:
   #pickle.dump([temp_home_dict, temp_away_dict], f)
  
  home_df.to_csv('data/full_match_data/'+year[2:4]+'-'+year[7:]+'/'+country+'_hist_data_'+year[2:4]+'_'+year[7:]+'_home.csv')
  away_df.to_csv('data/full_match_data/'+year[2:4]+'-'+year[7:]+'/'+country+'_hist_data_'+year[2:4]+'_'+year[7:]+'_away.csv')

 #Write total errors and missing values by category to error log
 error_file.write('\n')  

 for elem in league_matches:
  error_file.write(str(league_matches[elem]+'\n'))

 error_file.write('\n')

 error_file.write("\nTotal Errors: " + str(total_errors) + "\n")
 error_file.write("\nMissing Values:\n")

 for elem in missing_val:
  error_file.write(str(elem) + ": " + str(missing_val[elem]) + "\n")

 error_file.close()

browser.quit()
browser2.quit()
   
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
