import os
import pandas as pd
import psycopg2
from io import StringIO
import logging
import argparse

def log_results(cursor, query, log_message):
    """Executes a query and logs the results in a readable format."""
    cursor.execute(query)
    results = cursor.fetchall()
    formatted_results = "\n".join([str(row) for row in results])
    logging.info(f"{log_message}:\n{formatted_results}")


def create_table_if_not_exists(cursor, table_name):
    """Create the table with the specific schema if it does not exist."""
    if table_name == "item":
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS item (
            product_id INTEGER,
            category_id BIGINT,
            category_code TEXT,
            brand TEXT
        );
        """
    else:
        create_table_sql = f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            event_time TIMESTAMPTZ NOT NULL,
            event_type TEXT,
            product_id INTEGER,
            price FLOAT,
            user_id BIGINT,
            user_session UUID
        );
        """
    cursor.execute(f"SELECT EXISTS(SELECT * FROM information_schema.tables WHERE table_name='{table_name}');")
    if cursor.fetchone()[0]:
        logging.info(f"Table {table_name} already exists. Skipping creation and data import.")
        return False
    else:
        cursor.execute(create_table_sql)
        return True

def load_data_from_csv(path, tableName, cursor):
    """Load data from CSV to the specified table."""
    df = pd.read_csv(path)

    df['category_id'] = pd.to_numeric(df['category_id'], errors='coerce').fillna(0).astype('int64')

    logging.info(f"Number of rows in DataFrame: {len(df)}")
    
    buffer = StringIO()
    df.to_csv(buffer, index=False, header=False, sep='\t')
    buffer.seek(0)
    cursor.copy_from(buffer, tableName, sep='\t', null='')
    logging.info(f"Data loaded into {tableName} successfully.")
    cursor.execute(f"SELECT COUNT(*) FROM {tableName}")
    count = cursor.fetchone()[0]
    logging.info(f"Number of rows in the table {tableName}: {count}")
    logging.info(f"First row of the dataframe:\n{df.head(1)}")
    log_results(cursor, f"SELECT * FROM {tableName} LIMIT 1", "First row of the table")
    logging.info(f"Last row of the dataframe:\n{df.tail(1)}")
    log_results(cursor, f"SELECT * FROM {tableName} ORDER BY ctid DESC LIMIT 1", "Last row in the table")


def import_csvs(directory):
    if not os.path.exists(directory):
        logging.error(f"The directory {directory} does not exist.")
        return

    conn = psycopg2.connect("dbname='piscineds' user='amouly' host='localhost' password='mysecretpassword'")
    cursor = conn.cursor()

    logging.basicConfig(filename='bulk_data_load.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

    for filename in os.listdir(directory):
        if filename.endswith(".csv"):
            table_name = filename[:-4]
            path = os.path.join(directory, filename)
            logging.info(f"Processing file: {filename}")
            if create_table_if_not_exists(cursor, table_name):
                load_data_from_csv(path, table_name, cursor)
                conn.commit()
            else:
                logging.info(f"Skipping import for {table_name} as table already exists.")
        else:
            logging.info(f"Skipping non-CSV file: {filename}")

    cursor.close()
    conn.close()

# if __name__ == "__main__":
#     parser = argparse.ArgumentParser(description="Load CSV files into PostgreSQL tables.")
#     parser.add_argument("directory", type=str, help="Directory containing CSV files.")
#     args = parser.parse_args()

#     import_csvs(args.directory)



if __name__ == "__main__":
    import_csvs("/goinfre/amouly/piscineds/csv_files/customer")
    import_csvs("/goinfre/amouly/piscineds/csv_files/item")