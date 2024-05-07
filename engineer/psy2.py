import pandas as pd
import psycopg2
from io import StringIO
import logging


def create_table(cursor, table_name):
    """Create the table with the specific schema."""
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
    cursor.execute(create_table_sql)

def load(path, tableName):
    conn = psycopg2.connect("dbname='piscineds' user='amouly' host='localhost' password='mysecretpassword'")
    cursor = conn.cursor()

    logging.basicConfig(filename='data_load.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
    
    try:
        create_table(cursor, tableName)
        conn.commit()
        
        df = pd.read_csv(path)
        logging.info(f"Number of rows in DataFrame: {len(df)}")
        print(f"Number of rows in DataFrame: {len(df)}")

        buffer = StringIO()
        df.to_csv(buffer, index=False, header=False, sep='\t')
        buffer.seek(0)

        cursor.copy_from(buffer, tableName, sep='\t', null='')

        conn.commit()

        cursor.execute(f"SELECT COUNT(*) FROM {tableName}")
        rows_count = cursor.fetchone()[0]
        logging.info(f"Number of rows in the table {tableName}: {rows_count}")
        print(f"Number of rows in the table {tableName}: {rows_count}")

    except Exception as error:
        logging.error(f"An error occurred: {error}")
        conn.rollback() 
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    load("csv_files/customer/data_2022_oct.csv", "data_2022_oct")
