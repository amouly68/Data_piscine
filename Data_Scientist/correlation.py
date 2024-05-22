import pandas as pd
import matplotlib.pyplot as plt
import os
from scipy.stats import pointbiserialr


path = os.getcwd()
path = path + '/Data_Scientist'

path_train = path + '/Train_knight.csv'
data = pd.read_csv('Train_knight.csv')

data['knight'] = data['knight'].map({'Jedi': 0, 'Sith': 1})
correlations = data.corr(method='spearman')
knight_correlations = correlations['knight']
absolute_correlations = knight_correlations.abs()
sorted_correlations = absolute_correlations.sort_values(ascending=False)
sorted_correlations
type(sorted_correlations)

correl = {}
for col in data.columns[:]: 
    corr, p_value = pointbiserialr(data['knight'], data[col])
    correl[col] = abs(corr)

sorted_correl = pd.Series({k: v for k, v in sorted(correl.items(), key=lambda item: item[1], reverse=True)})
sorted_correl