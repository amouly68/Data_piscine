import pandas as pd
import matplotlib.pyplot as plt



data_test = pd.read_csv('Test_knight.csv')
fig, axes = plt.subplots(6, 5, figsize=(15, 15))  # Adjust figsize as needed

for i, ax in enumerate(axes.flat):
    column_name = data_test.columns[i]
    data_test[column_name].hist(ax=ax, bins=50, color='green',  )
    ax.set_title(column_name)
    ax.grid(False)
    ax.legend(['knight'], loc='upper right')

plt.tight_layout()
plt.show()


data = pd.read_csv('Train_knight.csv')
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


