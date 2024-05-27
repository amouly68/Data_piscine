import pandas as pd
import matplotlib.pyplot as plt

train = pd.read_csv('Train_knight.csv')
test = pd.read_csv('Test_knight.csv')
train1 = pd.read_csv('Train_knight_part1.csv')
test1 = pd.read_csv('Test_knight_part1.csv')

#compare the values of train and train1
train.describe()
train.head()

train1.describe()
train1.head()


#compare the values of test and test1
test.describe()
test1.describe()

#ADD variance on each colomn
test1.var()

#var cumulée
test1.var().cumsum()

#percentage of variance /var cumulée
test1.var().cumsum()/test1.var().cumsum().iloc[-1]*100
