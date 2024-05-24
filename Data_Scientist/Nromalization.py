#!/usr/bin/env python3

import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler

def standardize_data(data):
    """
    Standardize the data using StandardScaler.

    Parameters:
    data (pd.DataFrame): DataFrame containing the data.

    Returns:
    pd.DataFrame: Standardized data.
    """
    scaler = StandardScaler()
    standardized_data = scaler.fit_transform(data)
    standardized_data = pd.DataFrame(standardized_data, columns=data.columns)
    return standardized_data

def calculate_variances(data_file):
    """
    Calculate the variance of each skill after standardization,
    and accumulate the variances.

    Parameters:
    data_file (str): Path to the CSV file containing the data.

    Returns:
    pd.Series: A Series containing the variances of each skill.
    pd.Series: A Series containing the cumulative sum of the variances.
    """
    data = pd.read_csv(data_file)
    
    # Convert 'knight' to numerical if present
    if 'knight' in data.columns:
        data['knight'] = data['knight'].map({'Jedi': 0, 'Sith': 1})
    
    # Standardize the data
    standardized_data = standardize_data(data)
    
    # Calculate the variance of each skill in the standardized data
    standardized_variances = standardized_data.var()
    
    # Sort the variances in descending order
    sorted_standardized_variances = standardized_variances.sort_values(ascending=False)
    
    # Calculate the cumulative sum of the variances
    cumulative_standardized_variances = sorted_standardized_variances.cumsum()
    
    # Normalize the cumulative variances to get a percentage
    cumulative_standardized_variances_percentage = cumulative_standardized_variances / cumulative_standardized_variances.iloc[-1] * 100
    
    return sorted_standardized_variances, cumulative_standardized_variances_percentage

def plot_variances(cumulative_variances_percentage):
    """
    Plot the cumulative sum of variances.

    Parameters:
    cumulative_variances_percentage (pd.Series): A Series containing the cumulative sum of the variances as a percentage.
    """
    plt.figure(figsize=(10, 6))
    plt.plot(range(1, len(cumulative_variances_percentage) + 1), cumulative_variances_percentage, marker='o', linestyle='-', color='b')
    plt.axhline(y=90, color='r', linestyle='--', label='90% Variance')
    plt.title('Cumulative Sum of Variances (Standardized)')
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
    print("Sorted Variances (Standardized):")
    print(sorted_variances)
    
    # Print cumulative variances percentage
    print("\nCumulative Variances Percentage (Standardized):")
    print(cumulative_variances_percentage)
    
    plot_variances(cumulative_variances_percentage)

