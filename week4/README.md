# Intro to Analytics Engineering

## What is Analytics Engineering?
### Roles
1. Data Engineer prepares and maintains the infrastructure the data team needs.
2. Data Analyst uses data to answer questions and solve problems.
4. Analytics engineer is the role that tries to fill the gap: More software to Data Analyst and more Data to Data Engineer. The analytics engineer may be exposed to the following tools: 
    * Data Loading (Stitch...)
    * Data Storing (Data Warehouses)
    * Data Modeling (dbt, Dataform...)                              > we focus here
    * Data Presentation (BI tools like Looker, Mode, Tableau...)    > we focus here

### Tools for Data:
1. Massively parallel processing (MPP) databases
    * Lower the cost of storage 
    * BigQuery, Snowflake, Redshift...
2. Data-pipelines-as-a-service
    * Simplify the ETL process
    * Fivetran, Stitch...
3. SQL-first / Version control systems
    * Looker...
4. Self service analytics
5. Data governance

### ETL vs ELT
![etl-elt-striim](Striim-etl-elt.png)
![etl-elt-elitmind](elitmind-etl-elt.png)

# Introduction to dbt
***dbt*** stands for ***data build tool***. It's a transformation tool, transform raw data in Data Warehouse to transformed data which can be later used by Business Intelligence tools and any other data consumers. dbt also allows us to introduce good software engineering practices by defining a _deployment workflow_: Develop models, Test and document models, and Deploy models with _version control_ and _CI/CD_.

## dbt works
dbt works by defining a ***modeling layer*** that sits on top of our Data Warehouse. The modeling layer will turn _tables_ into ***models*** which we will then transform into _derived models_, which can be then stored into the Data Warehouse.
A ***model*** is a .sql file with a `SELECT` statement; no DDL or DML is used. dbt will compile the file and run it in our Data Warehouse.

## How to use dbt?
dbt has 2 main components: _dbt Core_ and _dbt Cloud_:
1. ***dbt Core***: open-source project that allows the data transformation.
    * Builds and runs a dbt project (.sql and .yaml files).
    * Includes SQL compilation logic, macros and database adapters.
    * Includes a CLI interface to run dbt commands locally.
    * Open-source and free to use.
2. ***dbt Cloud***: SaaS application to develop and manage dbt projects.
    * Web-based IDE to develop, run and test a dbt project.
    * Jobs orchestration.
    * Logging and alerting.
    * Intregrated documentation.
    * Free for individuals (one developer seat).
For integration with BigQuery, use dbt Cloud IDE, so a local installation of dbt core isn't required. For developing locally, use dbt Core + local Postgres database, which can be installed locally and connected to Postgres and run models through the CLI.