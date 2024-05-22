import pandas as pd
from sklearn.preprocessing import StandardScaler

# Charger les données
train_data = pd.read_csv('/mnt/data/Train_knight.csv')
test_data = pd.read_csv('/mnt/data/Test_knight.csv')

# Vérifier la présence de la colonne 'knight'
if 'knight' not in train_data.columns or 'knight' not in test_data.columns:
    raise KeyError("La colonne 'knight' n'existe pas dans les données.")

# Sélectionner les colonnes à standardiser (toutes sauf 'knight')
features = train_data.columns.drop('knight')

# Créer le scaler
scaler = StandardScaler()

# Ajuster le scaler sur les données d'entraînement et transformer les données d'entraînement
train_data_scaled = scaler.fit_transform(train_data[features])
test_data_scaled = scaler.transform(test_data[features])

# Convertir les résultats en DataFrame et rétablir les colonnes
train_data_scaled = pd.DataFrame(train_data_scaled, columns=features)
test_data_scaled = pd.DataFrame(test_data_scaled, columns=features)

# Ajouter la colonne 'knight' non transformée aux DataFrames
train_data_scaled['knight'] = train_data['knight']
test_data_scaled['knight'] = test_data['knight']

# Afficher un aperçu des données standardisées
print(train_data_scaled.head())
print(test_data_scaled.head())