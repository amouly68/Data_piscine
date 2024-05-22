#!/usr/bin/env python
import pandas as pd
from sklearn.model_selection import train_test_split
import sys

def split_data(input_file, train_file='Training_knight.csv', validation_file='Validation_knight.csv', test_size=0.2, random_state=42):
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
    
    train_data, validation_data = train_test_split(data, test_size=test_size, random_state=random_state)
    
    train_data.to_csv(train_file, index=False)
    validation_data.to_csv(validation_file, index=False)
    print(f"Les données ont été divisées et sauvegardées dans {train_file} et {validation_file}.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: ./split.py <input_file>")
        sys.exit(1)
    
    input_file = sys.argv[1]
    input_file = 'Train_knight.csv'
    split_data(input_file)