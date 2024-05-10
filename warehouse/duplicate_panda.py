import pandas as pd

def main():
    file_path = "/goinfre/amouly/piscineds/csv_files/customer/data_2022_oct.csv"
    df = pd.read_csv(file_path, nrows=100)
    # df = pd.read_csv(file_path)
    
    df['event_time'] = pd.to_datetime(df['event_time'])
    
    df.sort_values(by=['user_id', 'user_session', 'product_id', 'event_type', 'event_time'], inplace=True)


    df['is_duplicate'] = df.groupby(['user_id', 'user_session', 'product_id', 'event_type'])['event_time'].transform(
    lambda x: (x.diff(1).dt.total_seconds().abs() <= 1)
    )   

 

    duplicates = df[df['is_duplicate']].copy()
    duplicates.sort_values(by=['event_time'], inplace=True)
    df_cleaned = df[~df['is_duplicate']].copy()
    df_cleaned.drop(columns=['is_duplicate'], inplace=True)
    df_cleaned.sort_values(by=['event_time'], inplace=True)
    
    print("Number of rows in the original DataFrame: ", df.shape[0])
    print("Number of rows in the duplicates DataFrame: ", duplicates.shape[0])
    print("Number of rows in the cleaned DataFrame: ", df_cleaned.shape[0])


if __name__ == "__main__":
    main()
