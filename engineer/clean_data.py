import pandas as pd

data = pd.read_csv("csv_files/customer/data_2022_oct.csv")
data.head()
data.info()
data.describe()

item = pd.read_csv("csv_files/item/item.csv")
item.head()
cat = item["category_code"]
cat.value_counts()
item["category_code"].value_counts()
nombre_nan = item["category_code"].isna().sum()
nombre_autre = item["category_code"].notna().sum()
autre = item["category_code"].value_counts().sum()
total = autre + nombre_nan
