from selenium import webdriver
import re

def remove_spaces(curr_week):

    curr_week = curr_week.replace('Schalke 04', 'Schalke04')
    curr_week = curr_week.replace('FSV Mainz 05', 'FSVMainz05')
    
    return re.sub(r'(?<=[a-zA-Z])\s(?=[a-zA-Z])', '',curr_week)

def conv_month(day, month, year):

    leap = 0
    if(int(year)%4 == 0): leap = 1
    
    if(month == 'Jan.'): return (int(year)*365)+00+int(day)
    if(month == 'Feb.'): return (int(year)*365)+31+int(day)
    if(month == 'Mar.'): return (int(year)*365)+59+leap+int(day)
    if(month == 'Apr.'): return (int(year)*365)+90+leap+int(day)
    if(month == 'May.'): return (int(year)*365)+120+leap+int(day)
    if(month == 'Jun.'): return (int(year)*365)+151+leap+int(day)
    if(month == 'Jul.'): return (int(year)*365)+181+leap+int(day)
    if(month == 'Aug.'): return (int(year)*365)+212+leap+int(day)
    if(month == 'Sep.'): return (int(year)*365)+243+leap+int(day)
    if(month == 'Oct.'): return (int(year)*365)+273+leap+int(day)
    if(month == 'Nov.'): return (int(year)*365)+304+leap+int(day)
    if(month == 'Dec.'): return (int(year)*365)+334+leap+int(day)
    
    pass
    
        


path_to_chromedriver = "C:\\Users\\Sohum\\Downloads\\chromedriver_win32\\chromedriver.exe" # change path as needed
#path_to_chromedriver.replace("\\","/")
browser = webdriver.Chrome(executable_path = path_to_chromedriver)

results = dict()
track_dates = []

for year in [2012, 2013, 2014, 2015, 2016, 2017]:
 
 for country, num_teams in [['england', 20], ['spain', 20], ['germany', 18], ['italy', 20] , ['france', 20]]:

  if(year == 2017):
   url = 'http://www.soccerstats.com/latest.asp?league=' + country +'&pmtype=bygameweek'
   #browser.get(url)


   #browser.find_element_by_link_text('All results').click()
   ##browser.find_element_by_link_text('10').click()
  else:
   url = 'http://www.soccerstats.com/team_results.asp?league=' + country + '_' + str(year)+'&pmtype=bygameweek'
   
  browser.get(url)
  #browser.find_element_by_link_text('Matches').click()
  #browser.switch_to.frame(browser.find_element_by_tag_name("iframe"))
  #browser.find_element_by_partial_link_text('Matches by gameweek').click()
  

  for j in range(1, 5): #range(10, (num_teams-1)*2)
   browser.find_element_by_link_text(str(j)).click()

   if(j<num_teams): k = range(0, int(num_teams/2))
   else: k = range(int(num_teams/2),num_teams)
 
   for i in k:
    curr_week = browser.find_elements_by_xpath('//div[@class="tabbertab "]//tr[@class="odd"]')[i].text #get_attribute("innerHTML")
    print(curr_week)

    curr_week = remove_spaces(curr_week).split()

    #print(curr_week)

    match_date = conv_month(curr_week[1], curr_week[2], '16')
    if(match_date not in track_dates): track_dates.append(match_date)

    if(match_date not in results): results[match_date] = []

    try:   
     results[match_date].append([curr_week[4], curr_week[6], (int(curr_week[10][1]), int(curr_week[10][3])), (int(curr_week[7]),int(curr_week[9]))])
    except:
     pass
     #print("Error: ", curr_week)
   
for i in sorted(track_dates):
    print(i," | ", results[i])
