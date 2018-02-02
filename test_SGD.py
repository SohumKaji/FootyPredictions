import numpy as np
import pandas as pd
import pickle
from sklearn.multiclass import OneVsRestClassifier
from sklearn.linear_model import SGDClassifier

def score_func(pred, actual):
    score = 0

    #10 points for exact score
    if(np.array_equal(pred, actual)):
        #print("10 Points:", pred, actual)
        return 10

    #2 points for 1 correct score
    #Subtract 1 array from the other, as they are not identical
    #the result is either 2 or 4 nonzero elements, 2 indicates a match
    if(np.count_nonzero(pred-actual) == 2):
        score +=2

    #5 points for correct total goals
    if(total_goals(pred) == total_goals(actual)):
        score +=5

    #print(score, " Points:", pred, actual)
    return score

def total_goals(goals):

    total_goals = sum([elem*i for i, elem in enumerate(goals)])
    #print(goals, total_goals)
    return total_goals



with open('saved_SGD_&_train_test_data.pkl', 'rb') as fid:
    clf, X_train, X_test, y_train, y_test, base_model = pickle.load(fid)

pred = clf.predict(X_test)
pred = [2*elem if np.count_nonzero(elem) == 1 else elem for elem in pred]
base_model = [2*elem if np.count_nonzero(elem) == 1 else elem for elem in base_model]
y_test = [2*elem if np.count_nonzero(elem) == 1 else elem for elem in y_test]

base_score = 0
score= 0
total = 0
score_dict = dict({0: 0, 2: 0, 5: 0, 10: 0})
base_dict = dict({0: 0, 2: 0, 5: 0, 10: 0})


for i in range(len(pred)): #
    if(np.count_nonzero(pred[i]) not in [1,2]):
        #print("Pred:", i, pred[i])
        pred[i][np.random.choice(np.nonzero(pred[i])[0])] = 0

    if(np.count_nonzero(pred[i]) not in [1,2]):
        print("Pred:", i, pred[i])

        
    #if(np.count_nonzero(base_model[i]) not in [1,2]): print("Base:", i, base_model[i])
    total+=1
    temp = score_func(pred[i], y_test[i])
    score_dict[temp] +=1
    score += temp

    temp = score_func(base_model[i], y_test[i])
    base_dict[temp] +=1
    base_score += temp
    #print(pred[i], " | ", y_test[i])


print("----------------")
print("Total Score")
print("----------------")
print("SGD:  ", score)
print("Base: ", base_score)
print("Matches: ", total)
print("----------------")
print("Stats: ")
print(score_dict)
print(base_dict)

print("y_train")
for i, elem in enumerate(y_train):
    if(np.count_nonzero(elem) not in [1,2]): print("y_train", i, elem)

#if(np.array_equal(pred[i], y_test[i])): 
