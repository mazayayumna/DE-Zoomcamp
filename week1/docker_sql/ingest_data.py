import os
import pandas as pd
from sqlalchemy import create_engine
from time import time
import argparse

def main(params):
    user = params.user
    password = params.password
    host = params.host
    port = params.port
    db = params.db
    table_name = params.table_name
    url = params.url
    csv_name = 'output.csv'

    os.system(f"wget {url} -O {csv_name}.gz")
    os.system(f"gzip -d {csv_name}")

    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')

    df_iter = pd.read_csv(csv_name, iterator=True, chunksize=100000)
    df = next(df_iter)
    df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
    df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)
    df.head(n=0).to_sql(name=table_name, con=engine, if_exists='replace')
    df.to_sql(name=table_name, con=engine, if_exists='append')

    while True:
        t_start = time()
        df = next(df_iter)
        df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
        df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)
        df.to_sql(name=table_name, con=engine, if_exists='append')
        t_end = time()

        print('inserted chunk, took %.3f second' %(t_end - t_start))


if  __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Ingest CSV data to Postgre')

    parser.add_argument('--user',       help='username for postgre')
    parser.add_argument('--password',   help='password for postgre')
    parser.add_argument('--host',       help='host for postgre')
    parser.add_argument('--port',       help='port for postgre')
    parser.add_argument('--db',         help='database name for postgre')
    parser.add_argument('--table_name', help='table name where we write the result')
    parser.add_argument('--url',        help='url of the csv file')

    args = parser.parse_args()
    main(args)






