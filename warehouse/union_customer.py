import psycopg2
import logging

# Configuration du logging
logging.basicConfig(filename='Work_on_customer.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def create_merged_table():
    dbname = "piscineds"
    user = "amouly"
    password = "mysecretpassword"
    host = "localhost"
    port = "5432"
    
    try:
        conn = psycopg2.connect(
            dbname=dbname,
            user=user,
            password=password,
            host=host,
            port=port
        )
        cursor = conn.cursor()
        logging.info("Connected to the database successfully!")

        sql_script = """
        CREATE TABLE IF NOT EXISTS customers AS
        SELECT * FROM data_2022_dec
        UNION ALL
        SELECT * FROM data_2022_nov
        UNION ALL
        SELECT * FROM data_2022_oct
        UNION ALL
        SELECT * FROM data_2023_jan;
        """
        
        cursor.execute(sql_script)
        conn.commit()
        logging.info("Table 'customers' created and data merged successfully.")

        cursor.execute("SELECT COUNT(*) FROM customers;")
        count = cursor.fetchone()[0]
        logging.info(f"Total rows in 'customers' table: {count}")
        
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        conn.rollback()
        
    finally:
        if conn:
            cursor.close()
            conn.close()
            logging.info("Database connection closed.")

if __name__ == "__main__":
    create_merged_table()
