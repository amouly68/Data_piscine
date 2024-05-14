import pandas as pd
import matplotlib.pyplot as plt
import os
from scipy.stats import pointbiserialr

path = os.getcwd()
path = path + '/Data_Scientist'


path_test = path + '/Test_knight.csv'
data_test = pd.read_csv(path_test)
fig, axes = plt.subplots(6, 5, figsize=(15, 15))  # Adjust figsize as needed

for i, ax in enumerate(axes.flat):
    column_name = data_test.columns[i]
    data_test[column_name].hist(ax=ax, bins=50, color='green',  )
    ax.set_title(column_name)
    ax.grid(False)
    ax.legend(['knight'], loc='upper right')

plt.tight_layout()
plt.show()


path_train = path + '/Train_knight.csv'
data = pd.read_csv(path_train)
fig, axes = plt.subplots(6, 5, figsize=(15, 15))  # Adjust figsize as needed

data.head()
jedi = data[data['knight'] == 'Jedi']
sith = data[data['knight'] == 'Sith']

for i, ax in enumerate(axes.flat):
    column_name = data.columns[i]
    jedi[column_name].hist(ax=ax, bins=50, color='blue', label='Jedi', alpha=0.8)
    sith[column_name].hist(ax=ax, bins=50, color='red', label='Sith', alpha=0.5)

    ax.set_title(column_name)
    ax.grid(False)
    ax.legend()

plt.tight_layout()
plt.show()


data['knight'] = data['knight'].map({'Jedi': 1, 'Sith': 0})
# correlations = data.corr(method='spearman')
# knight_correlations = correlations['knight']
# absolute_correlations = knight_correlations.abs()
# sorted_correlations = absolute_correlations.sort_values(ascending=False)
# sorted_correlations


correl = {}
for col in data.columns[:-1]:  # Exclure la colonne 'knight' déjà encodée
    corr, p_value = pointbiserialr(data['knight'], data[col])
    correl[col] = corr

# Afficher les corrélations
for k, v in correl.items():
    print(f"Correlation between 'knight' and {k}: {v:.3f}")