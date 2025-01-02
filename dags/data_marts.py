from datetime import datetime

from airflow import DAG
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.providers.mysql.hooks.mysql import MySqlHook
from airflow.decorators import task, dag
from adapters.mysql_adaper import MySQLAdapter


@dag(
    dag_id="data_marts",
    start_date=datetime(2025, 1, 1),
    catchup=False,
    tags=["data_marts"],
)
def analysis_dag():
    @task(task_id = 'analysis_task')
    def analysis_task():
        msql_conn = MySQLAdapter()
        with open("/opt/airflow/dags/sql/data_mart.sql") as file:
            sql_query = file.read()
        rows = msql_conn.execute_commit_query(sql_query)
    
    analysis_task()

analysis_dag()