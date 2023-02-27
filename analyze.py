import pandas as pd
import pickle

dicty = pickle.load(open('results_big3.pickle', 'rb'))
count_zero = 0
for x in dicty:
    if dicty[x]==0:
        count_zero+=1

print('got ' + str(count_zero) + ' wrong, they are: ')
print([x for x in dicty if dicty[x]==0])


print('got ' + str(len(dicty)-count_zero) + ' right')
df = pd.DataFrame.from_dict(dicty, orient='index')
df = df.loc[df[0]>0]
print(pd.DataFrame(df[0].value_counts()).sort_index())
print(df[0].describe())