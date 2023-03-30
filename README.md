# Automate Data Pipelines

Project combines song metadata and song listen log files to surface analytics. JSON data stored in S3 is fed to a datat warehouse through a data warehouse defined in Apache Airflow. Redshift is used to stage the stage data before insertion into suitable tables for analysis. Data quality checks are performed before the pipeline finishes executing. End result is a Redshift cluster with data organised into a star schema with fact and dimension tables. Star schema is suitable for this application since denormalisatio is easy, queries are straightforward and aggregations are fast. 

Goal: create high grade data pipelines that are dynamic and built from reusable tasks, can be monitored, and allow easy backfills.

The source data resides in S3 and needs to be processed in Sparkify's data warehouse in Amazon Redshift. The source datasets consist of JSON logs that tell about user activity in the application and JSON metadata about the songs the users listen to.

## Requirements

* Create custom operations to perform necessary tasks such as staging the data, filling the data warehouse, and running checks on the data as the final step
* Custom operaters should consitute the functional piece of the data pipeline

Example DAG:
![image](https://user-images.githubusercontent.com/6599253/224577520-9538a06a-92e8-4598-b626-51dd5b5db501.png)

## Datasets
Two datasets hosted in S3 are used:
* Log data: `s3://udacity-dend/log_data`
* Song data: `s3://udacity-dend/song_data`

## Configure Airflow
In airflow.cfg (~/airflow) update `dags_folder` and `plugins_folder` to the project subdirectories. Set load_examples = False.

## Configure Environment
Create `DB/PASSWORD` in `redshift.cfg`

## Create IAM role, Redshift Cluster, configure TCP Connectivity and create Redshift tables
` $ python create_redshift_cluster.py --query_file create_tables.sql

# Start Airflow
```
 $ airflow initdb
 $ airflow scheduler
 $ airflow webserver
```

# Tear down
Delete IAM role and Redshift cluster
` $ python create_cluster.py --delete`
