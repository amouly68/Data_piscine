import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA


# Load the data
train = pd.read_csv('Train_knight.csv')
test = pd.read_csv('Test_knight.csv')
train = train.drop(columns=['knight'])


sc = StandardScaler()
sc.fit(train)
train_std = sc.transform(train)
test_std = sc.transform(test)


pca = PCA()
train_pca = pca.fit_transform(train_std)
exp_var_ratio = pca.explained_variance_ratio_
exp_var_ratio

cum_sum = exp_var_ratio.cumsum()
cum_sum
