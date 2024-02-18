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
```