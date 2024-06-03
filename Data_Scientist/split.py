#!/usr/bin/env python
import pandas as pd
from sklearn.model_selection import train_test_split
import sys

def split_data(input_file, train_file='Training_knight_1.csv', validation_file='Validation_knight_1.csv', test_size=0.05, random_state=42):
    """
    Divise le fichier d'entrée en deux fichiers de sortie : un pour l'entraînement et un pour la validation.
    
    Parameters:
    - input_file: Chemin vers le fichier CSV d'entrée.
    - train_file: Chemin vers le fichier CSV de sortie pour l'entraînement.
    - validation_file: Chemin vers le fichier CSV de sortie pour la validation.
    - test_size: Proportion de données à utiliser pour la validation.
    - random_state: Graine pour le générateur de nombres aléatoires pour assurer la reproductibilité.
    """
    data = pd.read_csv(input_file)
    X = data.drop('knight', axis=1)
    Y = data.iloc[:, -1]
    
    X_train, X_test, Y_train, Y_test = train_test_split(X,Y, test_size=test_size, random_state=random_state)
    print (X_train.shape)
    print (X_test.shape)
    train_data = pd.concat([X_train, Y_train], axis=1)
    validation_data = pd.concat([X_test, Y_test], axis=1)

    train_data.to_csv(train_file, index=False)
    validation_data.to_csv(validation_file, index=False)
    print(f"Les données ont été divisées et sauvegardées dans {train_file} et {validation_file}.")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        print("Usage: no argument needed.")
        sys.exit(1)
    
    # input_file = sys.argv[1]
    input_file = 'Train_knight.csv'
    split_data(input_file)