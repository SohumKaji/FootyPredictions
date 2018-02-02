import os
import pandas as pd
import numpy as np
from copy import deepcopy


pd.options.mode.chained_assignment = None # default = 'warn', was warning for False Positives

data_path = ''

"""
if not os.path.exists(data_path):
  os.makedirs(data_path)
for direc in ['14-15', '15-16', '16-17']:
  if not os.path.exists(data_path+direc):
    os.makedirs(data_path+direc)
    for country in ['eng', 'esp', 'ger', 'ita', 'fra']:  
      os.makedirs(data_path+direc+'/'+country)
      os.makedirs(data_path+direc+'/'+country+'/home')
      os.makedirs(data_path+direc+'/'+country+'/away')
"""

home_total = pd.DataFrame()
away_total = pd.DataFrame()

for year in ['14-15', '15-16', '16-17']:
 
  for league in [['eng', 10], ['ita', 10], ['esp', 10], ['fra', 10], ['ger', 9]]:

    #Read in DataFrames

    home_path = 'data/full_match_data'+'/'+year+'/'+league[0]+'_hist_data_'+year[0:2]+'_'+year[3:]+'_home.csv'
    away_path = 'data/full_match_data'+'/'+year+'/'+league[0]+'_hist_data_'+year[0:2]+'_'+year[3:]+'_away.csv' 
    
    home_df = pd.read_csv(home_path, index_col=0)
    away_df = pd.read_csv(away_path, index_col=0)
    home_index_list = list(home_df.index)
    away_index_list = list(away_df.index)
    team_list = []

    for elem in home_index_list:
      team_list.append(elem.split('_')[0])

    team_list = list(set(team_list))

    for team in team_list:

      #create home_file in folder SGD_Data/<year>/<league>/home/<team>
      #create away_file //
      home_path = data_path+year+'/'+league[0]+'/'+'home' + '/' + team + '.csv'
      away_path = data_path+year+'/'+league[0]+'/'+'away' + '/' + team + '.csv'

      
      curr_home_dict = dict()
      curr_away_dict = dict()

      home_entries = home_df[[team in elem for elem in home_df.index]]
      away_entries = away_df[[team in elem for elem in away_df.index]]

      
      #Reformat all columns that are not float to float
      """
      home_entries.ix[:, 'possession'] = [float(p[0:-1]) if p[-1] =='%' else p for p in home_entries.ix[:, 'possession']]
      home_entries.ix[:, 'passsuccess'] = [float(p[0:-1]) if p[-1] =='%' else p for p in home_entries.ix[:, 'passsuccess']]

      away_entries.ix[:, 'possession'] = [float(p[0:-1]) if p[-1] =='%' else p for p in away_entries.ix[:, 'possession']]
      away_entries.ix[:, 'passsuccess'] = [float(p[0:-1]) if p[-1] =='%' else p for p in away_entries.ix[:, 'passsuccess']]

      
      print(home_entries['possession'])
      print(home_entries['passsuccess'])

      print(away_entries['possession'])
      print(away_entries['passsuccess'])
      """
      
      print(team, year)
      for i in home_entries.keys():
        for ii, entry in enumerate(home_entries[i]):
          try:
            if(entry == 'None'): home_entries[i].iloc[ii] = np.mean([float(home_entries[i].iloc[iii]) for iii in range(ii)]) #; print(team, entry, ii, "None");
          except:
            print(team, year, entry, i)

      for i in away_entries.keys():
        for ii, entry in enumerate(away_entries[i]):
          try:
            if(entry == 'None'): away_entries[i].iloc[ii] = np.mean([float(away_entries[i].iloc[iii]) for iii in range(ii)]) #; print(team, entry, ii, "None");
          except:
            print(team, year, entry, i)


      #print(home_entries)


      
      #Compute the rolling average across all rows
      try:      
        home_final = home_entries.rolling(len(home_entries), 1, center = False).mean()
        away_final = away_entries.rolling(len(away_entries), 1, center = False).mean()
      except:
        print(team, year, entry, i)

      #if(home_total.empty): home_total = deepcopy(home_final)
      #else:
      home_total = pd.concat([home_total, home_final])

      #if(away_total.empty): away_total = deepcopy(away_final)
      #else:
      away_total = pd.concat([away_total, away_final]) 



      #home_final.to_csv(home_path)
      #away_final.to_csv(away_path)

      #print(home_entries)
      #print(away_entries.values())
      
    

home_total.to_csv("sgd_home.csv")
away_total.to_csv("sgd_away.csv")


