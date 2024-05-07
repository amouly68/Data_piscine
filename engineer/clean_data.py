import pandas as pd

oct = pd.read_csv("csv_files/customer/data_2022_oct.csv")
oct.head()
oct.info()
oct.describe()

nov = pd.read_csv("csv_files/customer/data_2022_nov.csv")
nov.head()
nov.info()

dec = pd.read_csv("csv_files/customer/data_2022_dec.csv")
dec.head()
dec.info()

jan = pd.read_csv("csv_files/customer/data_2023_jan.csv")
jan.head()
jan.info()

item = pd.read_csv("csv_files/item/item.csv")
item.head()
cat = item["category_code"]
cat.value_counts()
item["category_code"].value_counts()
nombre_nan = item["category_code"].isna().sum()
nombre_autre = item["category_code"].notna().sum()
autre = item["category_code"].value_counts().sum()
total = autre + nombre_nan
