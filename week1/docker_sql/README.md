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

SQL Refresher
```
# join yellow taxi and zones tables 1
# to know the yellow taxi location zone with zones tables 
SELECT
	tpep_pickup_datetime,
	tpep_dropoff_datetime,
	total_amount,
	CONCAT(zpu."Borough", '/', zpu."Zone") AS "pickup_loc", #ex: Manhattan/Central Park
	CONCAT(zdo."Borough", '/', zdo."Zone") AS "dropoff_loc"
FROM 
	yellow_taxi_trips t,
	zones zpu,
	zones zdo
WHERE
	t."PULocationID" = zpu."LocationID" AND t."DOLocationID" = zdo."LocationID"
LIMIT 100

# join yellow taxi and zones tables 2
# to know the yellow taxi location zone with zones tables 
SELECT
	tpep_pickup_datetime,
	tpep_dropoff_datetime,
	total_amount,
	CONCAT(zpu."Borough", '/', zpu."Zone") AS "pickup_loc",
	CONCAT(zdo."Borough", '/', zdo."Zone") AS "dropoff_loc"
FROM 
	yellow_taxi_trips t JOIN zones zpu
		ON t."PULocationID" = zpu."LocationID"
	JOIN zones zdo
		ON t."DOLocationID" = zdo."LocationID"
LIMIT 100

# checking locationID in yellow_taxi present in zones
SELECT
	tpep_pickup_datetime,
	tpep_dropoff_datetime,
	total_amount,
	"PULocationID",
	"DOLocationID"
FROM 
	yellow_taxi_trips t
WHERE
	-- "DOLocationID" is NULL
	"PULocationID" NOT IN (SELECT "LocationID" FROM zones)
LIMIT 100

# delete 142 from zones locaionID
DELETE FROM zones WHERE "LocationID" = 142

# using LEFT JOIN (yellow_taxi) to still show 142 with empty zone (..) instead of not showing it
SELECT
	tpep_pickup_datetime,
	tpep_dropoff_datetime,
	total_amount,
	CONCAT(zpu."Borough", '/', zpu."Zone") AS "pickup_loc",
	CONCAT(zdo."Borough", '/', zdo."Zone") AS "dropoff_loc"
FROM 
	yellow_taxi_trips t LEFT JOIN zones zpu
		ON t."PULocationID" = zpu."LocationID"
	LEFT JOIN zones zdo
		ON t."DOLocationID" = zdo."LocationID"
LIMIT 100

# order date and see which date is more busy with order by
SELECT
	CAST(tpep_dropoff_datetime AS DATE) as "day",
	COUNT(1) as "count"
    MAX(total_amount),
	MAX(passenger_count)
FROM 
	yellow_taxi_trips t
GROUP BY
	CAST(tpep_dropoff_datetime AS DATE)
-- ORDER BY "day" ASC
ORDER BY "count" DESC

# grouping by multiple fields
SELECT
	CAST(tpep_dropoff_datetime AS DATE) as "day",
	"DOLocationID",
	COUNT(1) as "count",
	MAX(total_amount),
	MAX(passenger_count)
FROM 
	yellow_taxi_trips t
GROUP BY
    -- day and "DOLocationID"!
	1,2
ORDER BY 
	"day" ASC,
	"DOLocationID" ASC

```