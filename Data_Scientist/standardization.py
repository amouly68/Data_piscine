import pandas as pd
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt




train = pd.read_csv('Train_knight.csv')
test = pd.read_csv('Test_knight.csv')

# train['knight'] = train['knight'].map({'Jedi': 1, 'Sith': 0})

features = train.columns.drop('knight')
train.head()

scaler = StandardScaler()

train_scaled = scaler.fit_transform(train[features])
test_scaled = scaler.fit_transform(test[features])

train_scaled = pd.DataFrame(train_scaled, columns=features)
test_scaled = pd.DataFrame(test_scaled, columns=features)

train_scaled['knight'] = train['knight']



ex = train[train['Sensitivity'] == 17.99]
ex
ex_std = train_scaled.loc[360]
ex_std
ex1 = train_scaled.loc[214]
ex1

# #scatterplot with standardized data
jedi = train_scaled[train_scaled['knight'] == 'Jedi']
sith = train_scaled[train_scaled['knight'] == 'Sith']
fig, ax = plt.subplots()

ax.scatter(jedi['Empowered'], jedi['Stims'], c='blue', label='Jedi', alpha=0.8)
ax.scatter(sith['Empowered'], sith['Stims'], c='red', label='Sith', alpha=0.5)
ax.set_xlabel('Empowered')
ax.set_ylabel('Stims')
ax.legend(loc='upper left')
plt.show()