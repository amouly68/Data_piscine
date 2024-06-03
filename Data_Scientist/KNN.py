#!/usr/bin/env python3

import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import f1_score, precision_score, recall_score, accuracy_score

def load_data(train_file, test_file):
    train = pd.read_csv(train_file)
    test = pd.read_csv(test_file)
    
    X_train = train.drop('knight', axis=1)
    y_train = train['knight']
    
    X_test = test.drop('knight', axis=1)
    y_test = test['knight']
    
    return X_train, y_train, X_test, y_test

def evaluate_knn(X_train, y_train, X_val, y_val, k_values):
    f1_scores = []
    precisions = []
    recalls = []
    accuracies = []

    for k in k_values:
        knn = KNeighborsClassifier(n_neighbors=k)
        knn.fit(X_train, y_train)
        y_pred = knn.predict(X_val)
        f1_scores.append(f1_score(y_val, y_pred, pos_label='Jedi'))
        precisions.append(precision_score(y_val, y_pred, pos_label='Jedi'))
        recalls.append(recall_score(y_val, y_pred, pos_label='Jedi'))
        accuracies.append(accuracy_score(y_val, y_pred))
    
    return f1_scores, precisions, recalls, accuracies

def find_best_k(f1_scores, k_values):
    best_k = k_values[np.argmax(f1_scores)]
    best_f1 = max(f1_scores)
    return best_k, best_f1

def plot_scores(k_values, f1_scores, precisions, recalls, accuracies):
    plt.figure(figsize=(12, 6))
    plt.plot(k_values, f1_scores, label='F1 Score', marker='o')
    # plt.plot(k_values, precisions, label='Precision', marker='x')
    # plt.plot(k_values, recalls, label='Recall', marker='s')
    plt.plot(k_values, accuracies, label='Accuracy', marker='d')
    plt.xlabel('k-value')
    plt.ylabel('Score')
    plt.title('KNN Performance for Different k-values')
    plt.legend()
    plt.grid(True)
    plt.show()

def save_predictions(X_train, y_train, X_test, output_file, best_k):
    knn = KNeighborsClassifier(n_neighbors=best_k)
    knn.fit(X_train, y_train)
    predictions = knn.predict(X_test)
    with open(output_file, 'w') as f:
        for pred in predictions:
            f.write(f"{pred}\n")

def main(train_file, test_file):
    X_train, y_train, X_test, y_test = load_data(train_file, test_file)
    
    # Split the training data into training and validation sets
    X_train_split, X_val_split, y_train_split, y_val_split = train_test_split(X_train, y_train, test_size=0.2, random_state=42)
    
    # Define k-values to evaluate
    k_values = list(range(1, 51))
    
    # Evaluate KNN
    f1_scores, precisions, recalls, accuracies = evaluate_knn(X_train_split, y_train_split, X_val_split, y_val_split, k_values)
    
    # Find the best k
    best_k, best_f1 = find_best_k(f1_scores, k_values)
    print(f"Best k: {best_k} with F1 Score: {best_f1}")
    
    # Plot the scores
    plot_scores(k_values, f1_scores, precisions, recalls, accuracies)
    
    # Save the predictions
    save_predictions(X_train, y_train, X_test, 'KNN.txt', best_k)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: ./knn_script.py <train_file> <test_file>")
        sys.exit(1)
    
    train_file = sys.argv[1]
    test_file = sys.argv[2]
    main(train_file, test_file)
