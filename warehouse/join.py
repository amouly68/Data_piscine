import pandas as pd

def main():
    data_path = "/goinfre/amouly/piscineds/csv_files/customer/data_2022_oct.csv"
    data = pd.read_csv(data_path, nrows=100)
    items_path = "/goinfre/amouly/piscineds/csv_files/item/item.csv"
    items = pd.read_csv(items_path)

    print("Data columns: ", data.columns)
    print("Data shape: ", data.shape)
    print("Items columns: ", items.columns)
    print("Items shape: ", items.shape)
    #duplicate item
    print("--------\n")
    print(items[items['product_id'] == 5861706])
    print(items[items['product_id'] == 37042])
    print("--------\n")
    print("Items duplicates: ", items.duplicated().sum())
    print("Items duplicates: ", items.duplicated(subset=['product_id']).sum())
    print("number of unique product_id: ", items['product_id'].nunique())
    print(items['product_id'].value_counts())
    items = items.drop_duplicates(subset=['product_id'])
    print("Items shape after drop duplicates: ", items.shape)

    joined = data.merge(items, how='left', left_on='product_id', right_on='product_id')
    print("Joined columns: ", joined.columns)
    print("Joined shape: ", joined.shape)    
    print(joined.head())


if __name__ == "__main__":
    main()