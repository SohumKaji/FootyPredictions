import os
import pandas as pd
import numpy as np
from copy import deepcopy


pd.options.mode.chained_assignment = None # default = 'warn', was warning for False Positives

data_path = ''

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

      #home_file in folder SGD_Data/<year>/<league>/home/<team>
      #away_file //
      home_path = data_path+year+'/'+league[0]+'/'+'home' + '/' + team + '.csv'
      away_path = data_path+year+'/'+league[0]+'/'+'away' + '/' + team + '.csv'

      
      curr_home_dict = dict()
      curr_away_dict = dict()

      home_entries = home_df[[team in elem for elem in home_df.index]]
      away_entries = away_df[[team in elem for elem in away_df.index]]


      #Collect the match data from the different .csv files. Replace all 'None' values with the mean for that team of that value
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

      
      #Compute the rolling average across all rows
      try:      
        home_final = home_entries.rolling(len(home_entries), 1, center = False).mean()
        away_final = away_entries.rolling(len(away_entries), 1, center = False).mean()
      except:
        print(team, year, entry, i)

      
      home_total = pd.concat([home_total, home_final])
      away_total = pd.concat([away_total, away_final]) 

     
    

home_total.to_csv("sgd_home.csv")
away_total.to_csv("sgd_away.csv")


