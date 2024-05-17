# Introduction to Batch Processing
### What is Batch Processing
Is when we process jobs or data per batch, it could be weekly, daily, hourly, and so on. It often used more that Stream Processing.
Advantages:
* Easy to manage
* Can retry failed jobs
* Scale of process
Disadvantage:
* Delay

***Technologies***: Python script, SQL, Spark, Flink.

### What is Spark
Spark is a data processing engine, it was written with Scala but with Python can use Pypark. It has cluster that contains machines that could process data and run jobs from data in Data Lake (ex. csv in s3 or GCS) and upload it again to the Data Lake.

***When to use Spark:***
* Typical process would be process data in DWH to DWH, it can be done in SQL tho with tools like Hive and Presto/Athena.
* But, if you can express your batch jobs as SQL, we should use Spark. 

# Installing spark on linux
### Login to VM
Refer to week1 how to ssh VM
```
ssh de-zoomcamp
```

### Install Java (must ver 8 or 11)
```
wget https://download.java.net/java/GA/jdk11/9/GPL/openjdk-11.0.2_linux-x64_bin.tar.gz
```
```
tar xzfv openjdk-11.0.2_linux-x64_bin.tar.gz
```
```
// put this to .bashrc too, dont forget to 'source .bashrc' and log again
export JAVA_HOME="${HOME}/week5/jdk-11.0.2"
export PATH="${JAVA_HOME}/bin:${PATH}"
```
```
java --version
```
Output should be:
```
openjdk 11.0.2 2019-01-15
OpenJDK Runtime Environment 18.9 (build 11.0.2+9)
OpenJDK 64-Bit Server VM 18.9 (build 11.0.2+9, mixed mode)
```
Remove pkg:
```
rm openjdk-11.0.2_linux-x64_bin.tar.gz
```

### Install Spark
```
wget https://archive.apache.org/dist/spark/spark-3.3.2/spark-3.3.2-bin-hadoop3.tgz
```
```
tar xzfv spark-3.3.2-bin-hadoop3.tgz
```
```
rm spark-3.3.2-bin-hadoop3.tgz
```
```
// put this to .bashrc too, dont forget to 'source .bashrc' and log again
export SPARK_HOME="${HOME}/week5/spark-3.3.2-bin-hadoop3"
export PATH="${SPARK_HOME}/bin:${PATH}"
```
```
which pyspark
spark-shell

val data = 1 to 10000
val distData = sc.parallelize(data)
distData.filter(_ < 10).collect()
```

### Setup Pyspark
Open vscode and ssh to de-zoomcamp, forward a port 8888 (cos u use VM).
```
cd week5/notebooks
export PYTHONPATH="${SPARK_HOME}/python/:$PYTHONPATH"
export PYTHONPATH="${SPARK_HOME}/python/lib/py4j-0.10.9.5-src.zip:$PYTHONPATH"
```
run `jupyter notebook` copy the link to browser to open it. Make a nwe file and test with:
```
import pyspark
pyspark.__version__
pyspark.__file__
```
run this code after that to download csv and read:
```
!wget https://s3.amazonaws.com/nyc-tlc/misc/taxi+_zone_lookup.csv

from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .master("local[*]") \
    .appName('test') \
    .getOrCreate()

df = spark.read \
    .option("header", "true") \
    .csv('taxi+_zone_lookup.csv')

df.show()

df.write.parquet('zones')
```
One more, forward port 4040 and open `localhost:4040`, you will see spark jobs.
This is how to forward port without VSCode, add this into ~/.ssh/config file:
```
LocalForward 8888 localhost:8888
LocalForward 4040 localhost:4040

```

# Spark SQL and DataFrames


### First look at Spark/Pyspark
Spark have cluster of machine, so one machine process 1 file, if there's 1 big file and machine 1 process one, the other machine will become idle. So we should do **Partition**!
***Steps***:
1) create new notebook `2_pyspark` and import.
2) download an unzip data from fhvhv_tripdata_2021-01.csv.
3) Load the dataset and show, you can see your jobs that has been run in Spark `local:4040`
4) Take onlt 1001 rows of dataset, save to `head.csv`.
5) Turn pandas DF to Spark DF, align with correct data type each column.
6) do **Partition** and convert it to .parquet, it will take some time o run. We can see active jobs in Spark!
7) `cd week5/notebooks/fhvhv/2021/01` run `ls -lh | wc -l`, can see 26 or 24 files.


### Spark DataFrames

**Actions vs Transormation**
Transformation - Lazy (not executed immediately)
* Selecting column
* Filtering
* Joins
* Group by, and so on

Action - Eager (executed immediately)
* show, take, head
* write, and so on

***Steps***:
1) read parquet files with spark df, we can also do filtering like this:
```
df.select('pickup_datetime', 'dropoff_datetime', 'PULocationID', 'DOLocationID') \
  .filter(df.hvfhs_license_num == 'HV003')
```
2) make a fuction name `crazy_stuff` if its divisible by 7 or 3 from `dispatching_base_num`, we return something start with s or a or e.
3) turn `crazy_stuff` function into udf or *user defined function*
4) Insert the udf to the dataframe as we safe it into a new column named `base_id`


### Preparing Yellow and Green Taxi Data
***Steps***:
1) Make a bash script to automatically download trip data each year and month `download_trip_data.sh`, run with:
```
chmod +x download_trip_data.sh
./download_trip_data.sh yellow 2020 #yellow,green,2020,2021
```
2) can see downloaded structure with `tree`
```
tree data
```
3) Make a new notebook `3_taxi_schema` import spark session and specify schema for each column datatypes with Spark.
4) For each taxi type (yellow, green) and year (2020, 2021). Read the dataframe with Spark, with specified schema (dtype)
5) For each taxi type (yellow, green) and year (2020, 2021). Do partition to 4 and convert them into .parquet file.
6) save to `data/pq/{taxi_type}/{year}/{month}`.


### SQL with Spark
In this step we will create a Pyspark version of week4 script `dm_monthly_zone_revenue.sql` that is written in dbt before. It is to combine both service type and and how much the revenue into one table in BigQuery `fact_trips`.

***Steps***:
1) Make a new notebook `4_spark_sql` and as usual import and start spark Session.
2) read all parquet files before with Spark, we will notice the column difference between yellow and green. So, rename!
> yellow is tpep_pickup_datetime and green is lpep_pickup_datetime
3) After rename make a code to search the common column between both dataframe to make it look clean and sorted.
4) For both dataframe with common columns, make new column name `service_type` to show if its either Green or Yellow with SQL Spark function.
5) combine both DF with `union` and register the DataFrame into a table, in order for SQL can read that.
6) Then, the main function with SQL to get total revenue for each *service type* (yellow, green) for each *month* and for each *revenue location*.
7) Finally, save the table to Parquet without partition (only 1 file using coalesce)


# Spark Internals
## Spark Cluster
Cluster is local [*] if you see when you start Spark session.

**Cluster executor**
* We write code and have a driver that submit a job (ex. Airflow task, dags, PC).
* Then driver submit the job to Cluster (this is like an office), we give it to master (4040), then who will do the jobs are executors. So, master is the leaders who submit jobs to the executors.
* Executor do pull data from Cloud, then process data (ex. DataFrame with partitions). One executor process one partition and save the data somewhere like S3 or GCS.
> previously ppl use Hadoop/HDFS where the data stored inside each executor (yes, it increase redundancy). But now even large files is no problem since Spark Cluster and Cloud Storage is in the same data center.

## GroupBy in Spark
this part we will see how to do GroupBy with Spark

***Steps***:
1) make a new notebook `5_groupby_join` and as usual to import and start the session.
2) Read the parquet we had before in `data/pq/{taxi_type}/{year}/{month}` with Spark and register them into tables.
3) Make an SQL function for each Yellow and Green DataFrame, can see read logic below in `SQL Function` section.
4) From the result of the function before, we repartition it into 20 files parquet files for each taxi type.
5) Command if you want to see hows the data inside
```
df_green_revenue.take(5) #take first 5 rows in tuple
df_green_revenue.show()  #show first 20 DataFrame
```
6) Save it into `data/report/revenue/{taxi_type}`.

### SQL Function
```
SELECT 
    date_trunc('hour', pickup_datetime) AS hour, 
    PULocationID AS zone,

    SUM(total_amount) AS amount,
    COUNT(1) AS number_records
FROM
    green or yellow
WHERE
    lpep_pickup_datetime >= '2020-01-01 00:00:00'
GROUP BY
    1, 2
```
It literally read hour from `pickup_datetime` and also zone from `PULocationID` (this one is Integer). Also has function to calculate the total amount (we already sum this before eg. fare, tip, etc) and count how many records or rows number we have from each **Hour and Zone, aka Key**, this one is where GroupBy takes place.
Also we select where `pickup_datetime` occurs from Jan 1st, 2020 cos this dataset is from 2020 and 2021.

If you see `local:4040` Spark, the job diagram, it will have 2 stages:
1) S1: preparation with GroupBy
For each partition, it comes to executors (GroupBy) and output are subresults.
>[[H1,Z1,100,5],[H1,Z2,200,10]],[[H1,Z1,50,2],[H1,Z2,250,12]],[[H3,Z1,200,10]]

2) S2: reshuffling
Shuffles the records we have in each partition (subresults). **Key** would be sumthing like *H1,Z1*, **value** would be *100,50*.
> p1 = [[H1,Z1,100,5],[H1,Z1,50,2],[H3,Z1,200,10]] and p2 = [[H1,Z2,200,10],[H1,Z2,250,12]]. Value would be [350,17] and [450,22].
> We want to reshuffle data as little as possible as its expensive. Plus, if you add OrderBy too, it will become 3 stages, fyi.


## Join in Spark
This is join in Spark.
* join large tables: btw if we use this Join after GroupBy before, stages in Spark would be 3, with an additional reshuffle stage to do external merge sort.
add photo

* join large and small table: no additional reshuffle as the small table (eg. zones) was sent and stay inside the executors.
add photo

### Join two large tables
this part we will see how to Join yellow revenue and green revenue before with Spark. Output will be like: [hour, zone, revenue yellow, records yellow, revenue green, records green]
***Steps***:
1) Read parquet files before from `data/report/revenue/{taxi_type}`.
2) Rename columns `amount` to `{taxi_type}_amount` and `number_records` to `{taxi_type}_number`.
3) Join Green and Yellow Spark DataFrame on hour and zone (key). Also we use `outer` to just display Null if we have records that is in Green but not in Yellow, vice versa. So records still show even sometimes we have null in the column either from Yellow or Green.
4) Save joined dataframe to parquet in `data/report/revenue/total`. It will be like this
```
DataFrame[hour: timestamp, zone: int, green_amount: double, green_number_records: bigint, yellow_amount: double, yellow_number_records: bigint]
```

### Join large table + small table
this part we will see how to Join joined revenue before with zone table before with Spark. Zone be like:
```
DataFrame[LocationID: string, Borough: string, Zone: string, service_zone: string]
```
***Steps***:
1) Read the parquet zone and I rename column Zone to `detailed_zone` to avoid confusion between both table.
2) Join both DataFrame if `joined.zone == zones.LocationID`, this is because `zone` in joined revenue is basically `locationID` in zones, they are both number.
3) After that drop both LocationID and Zone as they are number and we already know the actual zone with `detailed_zone`. Rows after join both be like this:
```
Row(hour=datetime.datetime(2020, 1, 1, 0, 0), green_amount=None, green_number_records=None, yellow_amount=8.8, yellow_number_records=1, Borough='Brooklyn', detailed_zone='Bay Ridge', service_zone='Boro Zone')
```


# Resilient Distributed Dataset (RDD)
RDD is a low level logic and not so popular these days, its the bottom of Spark DataFrame so we can enjoy nice API and functions. It has several operations like: `map, filter, reduceByKey, mapFilter, and RDD to DF (DF to RDD)`. We use green taxi dataset in parquet this time `data/pq/green/*/*` (df_green).

### Intro to RDD Steps:
***Steps***:
1) make a new notebook `6_rdds`. Import as usual.

2) `DF to RDD`: read the parquet with Spark DF, select columns, and turn it into RDD or `rdd`.

3) `filter`: make function `filter_outliers` to filter date before 2020. Like:
```
Row(lpep_pickup_datetime=datetime.datetime(2020, 1, 23, 13, 10, 15), PULocationID=74, total_amount=44.97)
```
It is a function that return either True or False.

4) `map`: add function `prepare_for_grouping` to group values to (key, value) aka ((hour.zone),(amount,count)). Count from 1.
map is a function that applied to every element or rows of the RDD (not partition).

5) `reduceByKey`: add function `calculate_revenue` to calc revenue aka amount and also count. As example: [(key1, val1),(key1, val2),(key1, val3),(key2, val1),(key2,val2)] to [(key1, val1, val2, val3)] and [(key2, val1, val2)]
> (key, value) - reduce - (key, reduced-value)

6) another `map`: is a function named `unwrap` just how to clean the the position of the row into ((hour,zone)(revenue,count))

7) Dont forget to specify the datatypes of the column (timestamp, int, double)

8) `RDD to DF`: function named `toDF`. 

9) This is how the full RDD operations take place:
```
df_result = rdd \
    .filter(filter_outliers) \
    .map(prepare_for_grouping) \
    .reduceByKey(calculate_revenue) \
    .map(unwrap) \
    .toDF(result_schema)
```

10) This is how the output looks like, and write the result to `tmp/green-revenue`:
```
Row(hour=datetime.datetime(2020, 1, 20, 15, 0), zone=67, revenue=79.5, count=3)
```

### RDD mapPartition:
MapPartition is like map, but it is a function that process not whole but per part. This is suitable for like Machine Learning when sometimes prediction will only take 1 part instead of whole, if the file is big like (ex 1TB, partition 100MB)
> RDD partition - mapPartition - RDD Partition

***Steps***:
1) take the previous Spark DF df_green, select some columns, and turn the DataFrame to RDD, take 10 rows, then turn it again to pandas DF.
> this shows how it easy to switch between RDD, pandas DF, spark DF

2) Make a function `model_predict` that predicts the duration of a trip from the trip distance (ex duration = distance*5)

3) Make a function `apply_model_in_batch` to apply prev model per batch. The `pd.DataFrame` materializes the entire DataFrame in memory. The `yield row` write each row to the resulting RDD and then it will flatten in the end.

4) Turn the result to Spark DF and drop column named `index`. Then we can see the predicted duration.
> note: our partition is not super balanced and repartitioning is an expensive operation.
