from datetime import datetime

from airflow import DAG
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.providers.mysql.hooks.mysql import MySqlHook
from airflow.operators.python import PythonOperator

from usecase.pg_initial_migration import pg_init_migration
from usecase.mysql_initial_migration import mysql_init_migration


with DAG(
    dag_id="initial_migration",
    start_date=datetime(2023, 12, 1),
    catchup=False,
    tags=["migration"],
) as dag:
        
        postres_migrate = PythonOperator(
        task_id="postgres_migrate",
        python_callable=pg_init_migration,
        )

        mysql_migrate = PythonOperator(
        task_id="mysql_migrate",
        python_callable=mysql_init_migration,
        )

postres_migrate >> mysql_migrate
