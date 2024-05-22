#!/usr/bin/env python3

import sys
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix, precision_recall_fscore_support

def load_data(predictions_file, truth_file):
    with open(predictions_file, 'r') as f:
        predictions = f.read().splitlines()
    with open(truth_file, 'r') as f:
        truth = f.read().splitlines()
    return predictions, truth

def calculate_metrics(predictions, truth):
    labels = ['Jedi', 'Sith']
    cm = confusion_matrix(truth, predictions, labels=labels)
    precision, recall, f1_score, _ = precision_recall_fscore_support(truth, predictions, labels=labels)
    accuracy = np.sum(np.diag(cm)) / np.sum(cm)
    
    metrics = {
        'Jedi': {'precision': precision[0], 'recall': recall[0], 'f1_score': f1_score[0], 'total': np.sum(cm[0, :])},
        'Sith': {'precision': precision[1], 'recall': recall[1], 'f1_score': f1_score[1], 'total': np.sum(cm[1, :])},
        'accuracy': accuracy
    }
    
    return cm, metrics

def print_metrics(metrics):
    print(f"{'':<10}{'precision':<10}{'recall':<10}{'f1-score':<10}{'total':<10}")
    for label in ['Jedi', 'Sith']:
        m = metrics[label]
        print(f"{label:<10}{m['precision']:<10.2f}{m['recall']:<10.2f}{m['f1_score']:<10.2f}{m['total']:<10}")
    print(f"{'accuracy':<10}{metrics['accuracy']:<10.2f}{100}")

def plot_confusion_matrix(cm, labels):
    fig, ax = plt.subplots()
    cax = ax.matshow(cm, cmap=plt.cm.Blues)
    plt.colorbar(cax)
    for (i, j), z in np.ndenumerate(cm):
        ax.text(j, i, f'{z}', ha='center', va='center')
    ax.set_xlabel('Predicted')
    ax.set_ylabel('True')
    ax.set_xticklabels([''] + labels)
    ax.set_yticklabels([''] + labels)
    plt.show()

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: ./Confusion_Matrix.py predictions.txt truth.txt")
        sys.exit(1)
    
    predictions_file = sys.argv[1]
    truth_file = sys.argv[2]
    
    predictions, truth = load_data(predictions_file, truth_file)
    cm, metrics = calculate_metrics(predictions, truth)
    
    print_metrics(metrics)
    print(cm)
    plot_confusion_matrix(cm, ['Jedi', 'Sith'])
