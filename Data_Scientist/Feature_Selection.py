#!/usr/bin/env python3

import sys
import pandas as pd
import numpy as np
from statsmodels.stats.outliers_influence import variance_inflation_factor
from sklearn.preprocessing import StandardScaler, MinMaxScaler

def normalize_and_standardize_data(data):
    """
    Normalize and standardize the data.

    Parameters:
    data (pd.DataFrame): DataFrame containing the data.

    Returns:
    pd.DataFrame: Normalized and standardized data.
    """
    # # Normalization
    # normalizer = MinMaxScaler()
    # normalized_data = normalizer.fit_transform(data)
    
    # Standardization
    scaler = StandardScaler()
    standardized_data = scaler.fit_transform(data)
    
    standardized_data = pd.DataFrame(standardized_data, columns=data.columns)
    return standardized_data

def calculate_vif_and_tolerance(data):
    """
    Calculate the VIF and tolerance for each feature in the dataset.

    Parameters:
    data (pd.DataFrame): DataFrame containing the data.

    Returns:
    pd.DataFrame: DataFrame containing features, their VIF, and tolerance.
    """
    vif_data = pd.DataFrame()
    vif_data["Feature"] = data.columns
    vif_data["VIF"] = [variance_inflation_factor(data.values, i) for i in range(len(data.columns))]
    vif_data["Tolerance"] = 1 / vif_data["VIF"]
    return vif_data

def remove_high_vif_features(data, threshold=5.0):
    """
    Remove features with VIF greater than the specified threshold.

    Parameters:
    data (pd.DataFrame): DataFrame containing the data.
    threshold (float): VIF threshold.

    Returns:
    pd.DataFrame: DataFrame with features having VIF less than the threshold.
    pd.DataFrame: DataFrame containing features removed due to high VIF.
    pd.DataFrame: DataFrame containing features kept with VIF less than the threshold.
    """
    removed_features = pd.DataFrame(columns=["Feature", "VIF", "Tolerance"])
    kept_features = pd.DataFrame(columns=["Feature", "VIF", "Tolerance"])
    
    while True:
        vif_data = calculate_vif_and_tolerance(data)
        max_vif = vif_data["VIF"].max()
        if max_vif > threshold:
            feature_to_remove = vif_data.sort_values("VIF", ascending=False).iloc[0]
            removed_features = pd.concat([removed_features, feature_to_remove.to_frame().T], ignore_index=True)
            data = data.drop(columns=[feature_to_remove["Feature"]])
        else:
            kept_features = vif_data.sort_values("VIF", ascending=False)
            break
    
    return data, removed_features, kept_features

def main(data_file):
    """
    Main function to read data, normalize, standardize it, and calculate VIF and tolerance.

    Parameters:
    data_file (str): Path to the CSV file containing the data.
    """
    data = pd.read_csv(data_file)
    
    # Convert 'knight' to numerical if present
    if 'knight' in data.columns:
        data['knight'] = data['knight'].map({'Jedi': 0, 'Sith': 1})
    
    # Normalize and standardize the data
    features = data.drop(columns=['knight']) if 'knight' in data.columns else data
    standardized_data = normalize_and_standardize_data(features)
    
    # Calculate and remove high VIF features
    filtered_data, removed_features, kept_features = remove_high_vif_features(standardized_data)
    
    print(f"\nFeatures removed due to high VIF:")
    print(removed_features)
    
    print("\nFinal features with VIF less than 5:")
    print(kept_features)

    print("\nShap of the DF with VIF less than 5:")
    print(filtered_data.shape)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: ./vif_analysis.py <data_file>")
        sys.exit(1)
    
    data_file = sys.argv[1]
    main(data_file)
