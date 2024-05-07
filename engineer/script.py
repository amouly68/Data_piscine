import pandas as pd
from sqlalchemy import create_engine
import sqlalchemy

def load(path, tableName):
    engine = create_engine("postgresql://amouly:mysecretpassword@localhost:5432/piscineds")
    try:
        # Lecture du CSV par morceaux
        chunksize = 50000  # Ajustez cette valeur selon la mémoire disponible
        for chunk in pd.read_csv(path, chunksize=chunksize):
            data_types = {
                "event_time": sqlalchemy.DateTime(),
                "event_type": sqlalchemy.types.String(length=255),
                "product_id": sqlalchemy.types.Integer(),
                "price": sqlalchemy.types.Float(),
                "user_id": sqlalchemy.types.BigInteger(),
                "user_session": sqlalchemy.types.UUID(as_uuid=True)
            }
            chunk.to_sql(tableName, engine, index=False, dtype=data_types, if_exists='append')
        print(f"Table {tableName} created")
    except Exception as error:
        print(f"An error occurred: {error}")
    finally:
        engine.dispose()

if __name__ == "__main__":
    load("csv_files/customer/data_2022_oct.csv", "data_2022_oct")

