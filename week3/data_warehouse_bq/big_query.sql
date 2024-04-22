-- video 1 sql
-- Query public available table
SELECT station_id, name FROM
    bigquery-public-data.new_york_citibike.citibike_stations
LIMIT 100;

-- My own dataset is not too big, only 2021 january, size wont change that much
SELECT * FROM `ny-rides-mazaya.trips_data_all.trip_data_csv` LIMIT 10;

-- Create a non partitioned table from external table
CREATE OR REPLACE TABLE ny-rides-mazaya.trips_data_all.trip_data_csv_non_partitoned AS
SELECT * FROM ny-rides-mazaya.trips_data_all.trip_data_csv;

-- Create a partitioned table from external table
CREATE OR REPLACE TABLE ny-rides-mazaya.trips_data_all.trip_data_csv_partitoned
PARTITION BY
  DATE(tpep_pickup_datetime) AS
SELECT * FROM ny-rides-mazaya.trips_data_all.trip_data_csv;

-- Impact of partition
-- Scanning 20.15MB of data
SELECT DISTINCT(VendorID)
FROM ny-rides-mazaya.trips_data_all.trip_data_csv_non_partitoned
WHERE DATE(tpep_pickup_datetime) BETWEEN '2021-01-01' AND '2021-01-26';

-- Scanning ~16.7 MB of DATA
SELECT DISTINCT(VendorID)
FROM ny-rides-mazaya.trips_data_all.trip_data_csv_partitoned
WHERE DATE(tpep_pickup_datetime) BETWEEN '2021-01-01' AND '2021-01-26';

-- Let's look into the partitons
SELECT table_name, partition_id, total_rows
FROM `trips_data_all.INFORMATION_SCHEMA.PARTITIONS`
WHERE table_name = 'trip_data_csv_partitoned'
ORDER BY total_rows DESC;

-- Creating a partition and cluster table
CREATE OR REPLACE TABLE ny-rides-mazaya.trips_data_all.trip_data_csv_partitoned_clustered
PARTITION BY DATE(tpep_pickup_datetime)
CLUSTER BY VendorID AS
SELECT * FROM ny-rides-mazaya.trips_data_all.trip_data_csv;

-- Query scans 16.7 MB
SELECT count(*) as trips
FROM ny-rides-mazaya.trips_data_all.trip_data_csv_partitoned
WHERE DATE(tpep_pickup_datetime) BETWEEN '2021-01-01' AND '2021-01-26'
  AND VendorID=1;

-- Query scans 16.7 MB
SELECT count(*) as trips
FROM ny-rides-mazaya.trips_data_all.trip_data_csv_partitoned_clustered
WHERE DATE(tpep_pickup_datetime) BETWEEN '2021-01-01' AND '2021-01-26'
  AND VendorID=1;