import numpy as np
import pandas as pd
import pickle
from sklearn.multiclass import OneVsRestClassifier
from sklearn.linear_model import SGDClassifier
import re

from sklearn import metrics
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.cross_validation import train_test_split
from sklearn.svm import SVC


#Gives a score based on how much the schedule names match the game data table row labels list
def name_fix(temp_name, namelist):

    """
    #temp_name = temp_name.split('FC')[0]
    m = (re.findall('[A-Z][a-z]+', temp_name))
    if(len(m) > 1): m = m[0]+m[1]     

    name = [elem for elem in namelist if m in elem]
    
    if(len(name) != 1): print(temp_name, name, m)
    """

    #Special case:
    if(temp_name == 'EspanyolBarcelona'): return 'RCDEspanyol'
    
    score = []
    for elem in namelist:
        count = 0
        i = 0
        curr_word = ''
        letters = list(temp_name)
        while i < len(letters):
            curr_word += letters[i]
            if((curr_word in elem)): 
                if(count < len(curr_word)): count = len(curr_word)
            elif(len(curr_word) != 1): curr_word = ''; i-=1
            i+=1    

        score.append(count)
    
    #if(temp_name != namelist[np.argmax(score)]): print(temp_name, namelist[np.argmax(score)])
    
    return namelist[np.argmax(score)]




home_path = 'sgd_home.csv'
away_path = 'sgd_away.csv'


#Read in full match stats
home_df = pd.read_csv(home_path, index_col=0)
away_df = pd.read_csv(away_path, index_col=0)

#Read in match information
with open('match_dates_and_scores.pickle', 'rb') as f:
 results, match_dates = pickle.load(f)

count, total = 0, 0
x, y, X_train, X_test, y_train, y_test, half_time = [], [], [] ,[], [], [], []
test_train_limit = match_dates[0]+ int((match_dates[-1]-match_dates[0])*(4/5))

for date in match_dates:
    for match in results[date]:
        total +=1
        temp_vec = 0
        try:
            #print('----------------------------------') #, date,': ', match[0], match[1], match[3])
            #print(home_df.loc[match[0]+'_'+str(date), :])
            #print(away_df.loc[match[1]+'_'+str(date), :])

            match_id_list_home = list(home_df.index)
            match_id_list_away = list(away_df.index)
            match_id_list_home = list(set([elem.split('_')[0] for elem in match_id_list_home]))
            match_id_list_away = list(set([elem.split('_')[0] for elem in match_id_list_away]))

            home_name = name_fix(match[0], match_id_list_home)
            away_name = name_fix(match[1], match_id_list_away)

            try:
                temp_vec = [[float(elem) for elem in (home_df.loc[home_name+'_'+str(date), :]).as_matrix()]]
            except:
                count +=1
                continue #print(count, ' | HOME ERROR:', date,': ', match[0], match[1], match[3])

            try:    
                temp_vec.append([float(elem) for elem in away_df.loc[away_name+'_'+str(date), :].as_matrix()])
            except:
                count +=1
                continue #print(count, ' | AWAY ERROR:', date,': ', match[0], match[1], match[3])

            if(temp_vec != 0):
                if(date < test_train_limit):
                    x.append(temp_vec)
                    y.append(list(match[3]))
                    half_time.append(list(match[2]))

            
        except:
            count +=1
            print(count, ' | ERROR:', date,': ', match[0], match[1], match[3])
            pass

print("Errors: ", count,"\nTotal: ", total)        
#print(len(temp_vec))
#print(temp_vec)
#print(len(X_train), len(X_test), len(y_train), len(y_test))
#print(X_train[1])
#print(X_test[1])
#print(y_train[1])
#print(y_test[1])
#Failed on:
#Espanyol, Bor.Monchengladbach, Atletico Madrid, Bournemouth    

x = np.array(x)
y = np.array(y)

#Classifier
print(x.shape)
x = np.nan_to_num(x.reshape(x.shape[0], x.shape[1]*x.shape[2]))

mlb = MultiLabelBinarizer()
y = mlb.fit_transform(y)

half_time = [[2*i, 2*ii] for i, ii in half_time]

mlb2 = MultiLabelBinarizer(classes = mlb.classes_)
half_time = mlb2.fit_transform(half_time)


X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.2)

print(X_train.shape)

clf = OneVsRestClassifier(SGDClassifier(loss='modified_huber', penalty='elasticnet',
                                          alpha=1e-4, n_iter=5, random_state=42,
                                          shuffle=True, n_jobs=-1) )

#clf = OneVsRestClassifier(SVC(probability=True))


clf.fit(X_train, y_train)


with open('saved_SGD_&_train_test_data.pkl', 'wb') as fid:
    pickle.dump((clf, X_train, X_test, y_train, y_test, half_time), fid, protocol = 2)    

"""
with open('saved_SGD_&_train_test_data.pkl', 'rb') as fid:
    clf, X_train, X_test, y_train, y_test, half_time = pickle.load(fid)


pred = clf.predict(X_test)

base_score = 0
score= 0
total = 0

for i in range(len(pred)):
    total+=1
    if(np.array_equal(pred[i], y_test[i])): score += 1
    if(np.array_equal(half_time[i], y_test[i])): base_score +=1
    #print(pred[i], " | ", y_test[i])

print(score, base_score)
print(total)
"""
