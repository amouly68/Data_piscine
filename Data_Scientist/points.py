import pandas as pd
import matplotlib.pyplot as plt



train = pd.read_csv('Train_knight.csv')
test = pd.read_csv('Test_knight.csv')
jedi = train[train['knight'] == 'Jedi']
sith = train[train['knight'] == 'Sith']

jedi.describe()
sith.describe()
# find the colomns where sith has values >  250
# Supposons que 'data' est votre DataFrame
cols = [col for col in sith.columns[:-1] if (sith[col] > 250).any()]
cols

jed = jedi[cols]
sit = sith[cols]
jed.describe()
sit.describe()
jed_visio = jedi[['Empowered', 'Stims', 'Push', 'Deflection', 'Sensitivity', 'Awareness']]  
jed_visio.describe()
sith_visio = sith[['Empowered', 'Stims', 'Push', 'Deflection', 'Sensitivity', 'Awareness']]
sith_visio.describe()




fig, axes = plt.subplots(2, 2, figsize=(15, 10))

for i, ax in enumerate(axes.flat):
    if i < 2:
        if i == 0:
            colx = 'Empowered'
            coly = 'Stims'
            leg_place = 'upper left'
        else:
            colx = 'Push'
            coly = 'Deflection'
            leg_place = 'upper right'
        ax.scatter(jedi[colx], jedi[coly], c='blue', label='Jedi')
        ax.scatter(sith[colx], sith[coly], c='red', label='Sith')
    else:
        if i == 2:
            colx = 'Empowered'
            coly = 'Stims'
            leg_place = 'upper left'
        else:
            colx = 'Push'
            coly = 'Deflection'
            leg_place = 'upper right'
        ax.scatter(test[colx], test[coly], c='green', label='Knight')
    ax.set_xlabel(colx)
    ax.set_ylabel(coly)
    ax.legend(loc=leg_place)

plt.tight_layout()
plt.show()
