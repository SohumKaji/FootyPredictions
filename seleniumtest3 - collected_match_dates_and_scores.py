from selenium import webdriver
import re
import pickle

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
    
    return re.sub(r'(?<=[a-zA-Z])\s(?=[a-zA-Z])', '',curr_week)

def conv_date(date):
    try:
     day = int(date[:2])
     month = int(date[3:5])
     year = int(date[7:])
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
    
        


path_to_chromedriver = "C:\\Users\\Sohum\\Downloads\\chromedriver_win32\\chromedriver.exe" # change path as needed
#path_to_chromedriver.replace("\\","/")
browser = webdriver.Chrome(executable_path = path_to_chromedriver)

results = dict()
track_dates = []

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

"""
    match_date = conv_month(curr_week[1], curr_week[2], '16')
    if(match_date not in track_dates): track_dates.append(match_date)

    if(match_date not in results): results[match_date] = []

    try:   
     results[match_date].append([curr_week[4], curr_week[6], (int(curr_week[10][1]), int(curr_week[10][3])), (int(curr_week[7]),int(curr_week[9]))])
    except:
     pass
     #print("Error: ", curr_week)
"""

for i in sorted(track_dates)[0:5]:
    print(i," | ", results[i])

for i in sorted(track_dates)[(len(track_dates)-5):]:
    print(i," | ", results[i])

#Save Scraped Data:

with open('match_dates_and_scores.pickle', 'wb') as f:
    pickle.dump([results, track_dates], f)


browser.quit()
