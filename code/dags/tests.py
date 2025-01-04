from datetime import datetime

from airflow import DAG
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.providers.mysql.hooks.mysql import MySqlHook
from airflow.decorators import task, dag
from adapters.mysql_adaper import MySQLAdapter
from utils.gen_tasks import gen_tasks, iter_tasks_directory
from airflow.operators.python import PythonOperator
from pyspark.sql import SparkSession
from pyspark.sql.types import StringType, StructType, IntegerType, DateType, StructField
import os

def get_connection_uri(conn):
    """
    Создает валидный URI из параметров хука.

    Args:
        conn: Соединение, полученное из хука.

    Returns:
        str: Строка URI для подключения к СУБД.
    """
    conn_type_jdbc_mapping = {
        "postgres": "postgresql",
        "mysql": "mysql"
    }
    conn_type = conn_type_jdbc_mapping[conn.conn_type]
    login = conn.login
    password = conn.password
    host = conn.host
    port = conn.port
    db = conn.schema
    extras_list = [f"{k}={v}" for k, v in conn.extra_dejson.items()]
    extras = f"&{'&'.join(extras_list)}" if extras_list else ''
    return f"jdbc:{conn_type}://{host}:{port}/{db}?user={login}&password={password}{extras}"


def spark_test():
    source_url = get_connection_uri(PostgresHook.get_connection('pg'))
    print(source_url)



with DAG(
    dag_id="test",
    start_date=datetime(2025, 1, 1),
    catchup=False,
    tags=["test"],
) as dag:
    test = PythonOperator(
        task_id = 'test',
        python_callable=spark_test
    )

    test