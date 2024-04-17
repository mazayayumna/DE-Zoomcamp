import os
import pandas as pd
from sqlalchemy import create_engine
from time import time

def ingest_callable(user, password, host, port, db, table_name, csv_file):
    print(table_name, csv_file)

    os.system(f"gzip -d {csv_file}")

    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')
    engine.connect()
    print('connection established!, inserting data...')

    t_start = time()
    df_iter = pd.read_csv(os.path.splitext(csv_file)[0], iterator=True, chunksize=100000)
    df = next(df_iter)
    df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
    df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)
    df.head(n=0).to_sql(name=table_name, con=engine, if_exists='replace')
    df.to_sql(name=table_name, con=engine, if_exists='append')
    t_end = time()
    print('inserted the first chunk, took %.3f second' %(t_end - t_start))

    while True:
        t_start = time()
        df = next(df_iter)
        df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
        df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)
        df.to_sql(name=table_name, con=engine, if_exists='append')
        t_end = time()

        print('inserted chunk, took %.3f second' %(t_end - t_start))