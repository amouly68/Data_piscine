#!/usr/bin/env python3

import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from sklearn.decomposition import PCA


def normalize_data(data):
    """
    Normalize the data using MinMaxScaler.

    Parameters:
    data (pd.DataFrame): DataFrame containing the data.

    Returns:
    pd.DataFrame: Normalized data.
    """
    scaler = MinMaxScaler()
    normalized_data = scaler.fit_transform(data)
    normalized_data = pd.DataFrame(normalized_data, columns=data.columns)
    return normalized_data

def calculate_variances(data_file):
    """
    Calculate the variance of each skill and accumulate the variances.

    Parameters:
    data_file (str): Path to the CSV file containing the data.

    Returns:
    pd.Series: A Series containing the variances of each skill.
    pd.Series: A Series containing the cumulative sum of the variances.
    """
    data = pd.read_csv(data_file)
    
    # Normalize the data
    if 'knight' in data.columns:
        data['knight'] = data['knight'].map({'Jedi': 0, 'Sith': 1})
        features = data.drop(columns=['knight'])
    else:
        features = data
    
    normalized_data = normalize_data(features)

    # Standardize the data
    sc = StandardScaler()
    sc.fit(normalized_data)
    std_data = sc.transform(normalized_data)

    
    # PCA
    pca = PCA()
    pca.fit_transform(std_data)
    sorted_variances = pca.explained_variance_ratio_
    
    # Calculate the cumulative sum of the variances
    cumulative_variances_percentage = sorted_variances.cumsum()
    cumulative_variances_percentage *= 100
    
    return sorted_variances, cumulative_variances_percentage

def plot_variances(cumulative_variances_percentage):
    """
    Plot the cumulative sum of variances.

    Parameters:
    cumulative_variances_percentage (pd.Series): A Series containing the cumulative sum of the variances as a percentage.
    """
    plt.figure(figsize=(10, 6))
    plt.plot(range(1, len(cumulative_variances_percentage) + 1), cumulative_variances_percentage, marker='o', linestyle='-', color='b')
    plt.axhline(y=90, color='r', linestyle='--', label='90% Variance')
    plt.title('Cumulative Sum of Variances')
    plt.xlabel('Number of Components (Skills)')
    plt.ylabel('Cumulative Variance Percentage')
    plt.legend()
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: ./variance_analysis.py <data_file>")
        sys.exit(1)
    
    data_file = sys.argv[1]
    sorted_variances, cumulative_variances_percentage = calculate_variances(data_file)
    
    # Print sorted variances
    print("Sorted Variances:")
    print(sorted_variances)
    
    # Print cumulative variances percentage
    print("\nCumulative Variances Percentage:")
    print(cumulative_variances_percentage)
    
    plot_variances(cumulative_variances_percentage)
