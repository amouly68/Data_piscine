#!/usr/bin/env python3

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.tree import DecisionTreeClassifier
from sklearn import tree
import sys

def main(train_file):
    # Load the data
    train = pd.read_csv(train_file)
    X = train.drop('knight', axis=1)
    Y = train.iloc[:, -1]

    # Initialize and fit the decision tree classifier
    tn = DecisionTreeClassifier(criterion='gini')
    tn.fit(X, Y)
    
    # Plot the decision tree
    plt.figure(figsize=(25, 20))
    _ = tree.plot_tree(tn, 
                       class_names=['0', '1'], 
                       filled=True)
    
    plt.show()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: ./decision_tree_script.py <train_file>")
        sys.exit(1)
    
    train_file = sys.argv[1]
    main(train_file)