from datetime import datetime

from airflow import DAG
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.providers.mysql.hooks.mysql import MySqlHook
from airflow.decorators import task, dag
from adapters.mysql_adaper import MySQLAdapter
from utils.gen_tasks import gen_tasks, iter_tasks_directory
from airflow.operators.python import PythonOperator
import os

def generation_test():
    for dir_path, _, files_list in os.walk("/opt/airflow"):
        parent_path, dir_name = os.path.split(dir_path)
        _, parent_dir_name = os.path.split(parent_path)

        for file_name in files_list:
            print(dir_name, parent_dir_name, file_name)
    print('-----------------------END OF TEST------------------------')

with DAG(
    dag_id="data_marts",
    start_date=datetime(2025, 1, 1),
    catchup=False,
    tags=["data_marts"],
) as dag:
    gen_tasks(dag, 'marts')