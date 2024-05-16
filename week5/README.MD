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
