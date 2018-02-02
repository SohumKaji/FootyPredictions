import pickle


with open('match_dates_and_scores.pickle', 'rb') as f:
 results, match_dates = pickle.load(f)

print(match_dates[0:10])
#print(results[0:10])
