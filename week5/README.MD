# Introduction to Batch Processing
### What is Batch Processing
### What is Spark

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
