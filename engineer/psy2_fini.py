import os
import sys
import pandas as pd
import psycopg2
from io import StringIO
import logging

def create_table_if_not_exists(cursor, table_name):
    """Create the table with the specific schema if it does not exist."""
    cursor.execute(f"SELECT EXISTS(SELECT * FROM information_schema.tables WHERE table_name='{table_name}');")
    if cursor.fetchone()[0]:
        logging.info(f"Table {table_name} already exists. Skipping creation and data import.")
        return False
    else:
        create_table_sql = f"""
        CREATE TABLE {table_name} (
            event_time TIMESTAMPTZ NOT NULL,
            event_type TEXT,
            product_id INTEGER,
            price FLOAT,
            user_id BIGINT,
            user_session UUID
        );
        """
        cursor.execute(create_table_sql)
        return True

def load_data_from_csv(path, tableName, cursor):
    """Load data from CSV to the specified table."""
    df = pd.read_csv(path)
    buffer = StringIO()
    df.to_csv(buffer, index=False, header=False, sep='\t')
    buffer.seek(0)
    cursor.copy_from(buffer, tableName, sep='\t', null='')
    logging.info(f"Data loaded into {tableName} successfully.")

def import_csvs(directory):
    # Setup database connection
    conn = psycopg2.connect("dbname='piscineds' user='amouly' host='localhost' password='mysecretpassword'")
    cursor = conn.cursor()

    # Setup logging
    logging.basicConfig(filename='bulk_data_load.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

    # Process each CSV file in the directory
    for filename in os.listdir(directory):
        if filename.endswith(".csv"):
            table_name = filename[:-4]  # Remove '.csv' from filename to use as table name
            path = os.path.join(directory, filename)
            logging.info(f"Processing file: {filename}")
            if create_table_if_not_exists(cursor, table_name):
                load_data_from_csv(path, table_name, cursor)
                conn.commit()
                logging.info(f"Data committed to the table {table_name}.")
            else:
                logging.info(f"Skipping import for {table_name} as table already exists.")
        else:
            logging.info(f"Skipping non-CSV file: {filename}")

    cursor.close()
    conn.close()

if __name__ == "__main__":
    import_csvs("./csv_files/customer")