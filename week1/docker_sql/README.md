Very basic docker commands to build and run image:
```
docker build -t test:pandas .
docker run -it test:pandas
docker ps
```

Start running POSTGRESQL:
```
docker run -it \
    -e POSTGRES_USER="root" \
    -e POSTGRES_PASSWORD="root" \
    -e POSTGRES_DB="ny_taxi" \
    -v $(pwd)/ny_taxi_postgres_data:/var/lib/postgresql/data \
    -p 5432:5432 \
    postgres:11
```
do not forget to
```
sudo chmod -R 744 $(pwd)/ny_taxi_postgres_data
```

Basic pgcli command
```
pgcli --help
pgcli -h localhost -p 5432 -u root -d ny_taxi #connect
\dt #list of tables
\d $(table_name) #ex:yellow_taxi_data, to list column and its dtype in the table
SELECT count(1) FROM $(table_name) # count number of rows
SELECT max(tpep_pickup_datetime), min(tpep_pickup_datetime), max(total_amount) FROM yellow_taxi_data
```

pgAdmin with docker basic command
```
# create network between postgre table and pgadmin
docker network create pg-network
docker run -it \
    -e POSTGRES_USER="root" \
    -e POSTGRES_PASSWORD="root" \
    -e POSTGRES_DB="ny_taxi" \
    -v $(pwd)/ny_taxi_postgres_data:/var/lib/postgresql/data \
    -p 5432:5432 \
    --network=pg-network \
    --name pg-database \
    postgres:11

# finally pgadmin in different terminal
docker run -it \
    -e PGADMIN_DEFAULT_EMAIL="admin@admin.com" \
    -e PGADMIN_DEFAULT_PASSWORD="root" \
    -p 8080:80 \
    --network=pg-network \
    --name pgadmin \
    dpage/pgadmin4

localhost:8080 
# on browser, pgadmin, browser, tab setting, open query tool in new tab
# host name: 127.0.0.1, connection name pg-database, view 100
SELECT * FROM public.yellow_taxi_data LIMIT 100
SELECT COUNT(1) FROM yellow_taxi_data
```

Using python script to ingest data instead of notebook + dockerizing
```
URL = "https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2021-01.csv.gz"

# DO NOT FORGET to create network first (read last step)
python ingest_data.py \
    --user=root \
    --password=root \
    --host=localhost \
    --port=5432 \
    --db=ny_taxi \
    --table_name=yellow_taxi_trips \
    --url=${URL}

docker build -t taxi_ingest:v001 .

docker run -it \
    --network=pg-network \
    taxi_ingest:v001 \
        --user=root \
        --password=root \
        --host=pg-database \
        --port=5432 \
        --db=ny_taxi \
        --table_name=yellow_taxi_trips \
        --url=${URL}
```

Replacing pgAdmin and Postgre docker with Docker-Compose (yaml)
```
docker-compose up       #turn on
docker-compose down     #turn off
docker-compose up -f    #turn off
```