import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import pointbiserialr


data = pd.read_csv('Train_knight.csv')

data['knight'] = data['knight'].map({'Jedi': 1, 'Sith': 0})
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

#heatmap
plt.figure(figsize=(10, 10))
plt.matshow(data.corr(method='spearman'), fignum=1, cmap='Reds_r')
plt.xticks(range(data.shape[1]), data.columns, fontsize=14, rotation=90)
plt.yticks(range(data.shape[1]), data.columns, fontsize=14)
plt.colorbar()
plt.show()
