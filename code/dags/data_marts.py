from datetime import datetime

from airflow import DAG
# from airflow.providers.postgres.hooks.postgres import PostgresHook
# from airflow.providers.mysql.hooks.mysql import MySqlHook
# from airflow.decorators import task, dag
from utils.gen_tasks import gen_tasks, iter_tasks_directory



with DAG(
    dag_id="data_marts",
    start_date=datetime(2025, 1, 1),
    catchup=False,
    tags=["data_marts"],
) as dag:
    gen_tasks(dag, 'marts')