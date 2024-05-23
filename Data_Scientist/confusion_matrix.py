#!/usr/bin/env python3

import sys
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

def load_data(predictions_file, truth_file):
    """
    Load prediction and truth data from text files.

    Parameters:
    predictions_file (str): Path to the file containing predictions.
    truth_file (str): Path to the file containing ground truth labels.

    Returns:
    pd.DataFrame: A DataFrame with columns 'truth' and 'prediction'.
    """
    predictions = pd.read_csv(predictions_file, header=None, names=['prediction'])
    truth = pd.read_csv(truth_file, header=None, names=['truth'])
    data = pd.concat([truth, predictions], axis=1)
    return data

def classify(row):
    """
    Classify the prediction as VP, FP, FN, or VN.

    Parameters:
    row (pd.Series): A row of the DataFrame containing 'truth' and 'prediction'.

    Returns:
    str: Classification as 'VP', 'FP', 'FN', or 'VN'.
    """
    if row['prediction'] == 'Jedi' and row['truth'] == 'Jedi':
        return 'VP'
    elif row['prediction'] == 'Jedi' and row['truth'] == 'Sith':
        return 'FP'
    elif row['prediction'] == 'Sith' and row['truth'] == 'Jedi':
        return 'FN'
    elif row['prediction'] == 'Sith' and row['truth'] == 'Sith':
        return 'VN'

def calculate_confusion_matrix(data):
    """
    Calculate the confusion matrix values (VP, FP, FN, VN).

    Parameters:
    data (pd.DataFrame): DataFrame containing 'truth' and 'prediction' columns.

    Returns:
    np.array: A 2x2 numpy array representing the confusion matrix.
    """
    VP = data['matrix'].value_counts().get('VP', 0)
    FP = data['matrix'].value_counts().get('FP', 0)
    FN = data['matrix'].value_counts().get('FN', 0)
    VN = data['matrix'].value_counts().get('VN', 0)
    return np.array([[VP, FN], [FP, VN]])

def calculate_metrics(cm):
    """
    Calculate precision, recall, f1-score, and accuracy from the confusion matrix.

    Parameters:
    cm (np.array): Confusion matrix.

    Returns:
    dict: A dictionary containing metrics for Jedi and Sith classes, and accuracy.
    """
    VP, FN, FP, VN = cm[0, 0], cm[0, 1], cm[1, 0], cm[1, 1]
    precision_jedi = VP / (VP + FP) if (VP + FP) > 0 else 0
    recall_jedi = VP / (VP + FN) if (VP + FN) > 0 else 0
    f1_jedi = 2 * (precision_jedi * recall_jedi) / (precision_jedi + recall_jedi) if (precision_jedi + recall_jedi) > 0 else 0
    
    precision_sith = VN / (VN + FN) if (VN + FN) > 0 else 0
    recall_sith = VN / (VN + FP) if (VN + FP) > 0 else 0
    f1_sith = 2 * (precision_sith * recall_sith) / (precision_sith + recall_sith) if (precision_sith + recall_sith) > 0 else 0
    
    accuracy = (VP + VN) / (VP + FP + FN + VN) if (VP + FP + FN + VN) > 0 else 0
    
    metrics = {
        'Jedi': {'precision': precision_jedi, 'recall': recall_jedi, 'f1_score': f1_jedi, 'total': VP + FN},
        'Sith': {'precision': precision_sith, 'recall': recall_sith, 'f1_score': f1_sith, 'total': VN + FP},
        'accuracy': accuracy
    }
    
    return metrics

def print_metrics(metrics):
    """
    Print the calculated metrics.

    Parameters:
    metrics (dict): Dictionary containing the calculated metrics.
    """
    print(f"{'':<10}{'precision':<10}{'recall':<10}{'f1-score':<10}{'total':<10}")
    for label in ['Jedi', 'Sith']:
        m = metrics[label]
        print(f"{label:<10}{m['precision']:<10.2f}{m['recall']:<10.2f}{m['f1_score']:<10.2f}{m['total']:<10}")
    print(f"{'accuracy':<10}{metrics['accuracy']:<10.2f}{100}")

def plot_confusion_matrix(cm, labels):
    """
    Plot the confusion matrix using matplotlib.

    Parameters:
    cm (np.array): Confusion matrix.
    labels (list): List of class labels.
    """
    fig, ax = plt.subplots()
    cax = ax.matshow(cm, cmap=plt.cm.Blues)
    plt.colorbar(cax)
    for (i, j), z in np.ndenumerate(cm):
        ax.text(j, i, f'{z}', ha='center', va='center')
    ax.set_xlabel('Predicted')
    ax.set_ylabel('True')
    ax.set_xticks(np.arange(len(labels)))  # Set the positions of the x ticks
    ax.set_yticks(np.arange(len(labels)))  # Set the positions of the y ticks
    ax.set_xticklabels(labels)  # Set the labels of the x ticks
    ax.set_yticklabels(labels)  # Set the labels of the y ticks
    plt.show()


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: ./Confusion_Matrix.py predictions.txt truth.txt")
        sys.exit(1)
    
    predictions_file = sys.argv[1]
    truth_file = sys.argv[2]
    
    data = load_data(predictions_file, truth_file)
    data['matrix'] = data.apply(classify, axis=1)
    
    cm = calculate_confusion_matrix(data)
    metrics = calculate_metrics(cm)
    
    print_metrics(metrics)
    print(cm)
    plot_confusion_matrix(cm, ['Jedi', 'Sith'])
