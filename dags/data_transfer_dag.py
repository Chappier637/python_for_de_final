from datetime import datetime
import yaml

from airflow import DAG
from airflow.operators.python import PythonOperator

from usecase.pg_select import pg_fetch_table
from usecase.mysql_insert_data import mysql_insert_data


# Возвращает конфиг таблиц и колонок для репликации данных
def load_replicate_config(config_file="/opt/airflow/dags/usecase/replicate_tables.yaml"):
    with open(config_file, 'r') as file:
        config = yaml.safe_load(file)  # For JSON, use json.load(file)
    return config

# Читает данные из Postgres таблицы по заданным колонкам и вставляет их в MySQL
def replicate_table(table, columns):
    fetch_result = pg_fetch_table(table, columns)
    mysql_insert_data(table_to_insert=table, 
                      rows=fetch_result, 
                      columns=columns)


with DAG(
    dag_id="transefer_postgres_mysql",
    start_date=datetime(2024, 12, 1),
    catchup=False,
    tags=["replication"],
) as dag:

    # Берем из конфига названия таблиц и колонок, который нужно копировать
    tables_to_replicate = load_replicate_config().get("tables_to_copy")

    # Создаем для каждой таблицы свой Даг, динамически
    previous_task = None
    for table in tables_to_replicate:
        current_task = PythonOperator(
            task_id=f"replicate_{table.get('table')}",
            python_callable=replicate_table,
            # Назавание таблицы и колонок передает как аргумент 
            op_args=[table.get("table"), table.get("columns")], 
        )

        # Этот блок задает последовательное выполнение дагов
        if previous_task:
            previous_task >> current_task
        previous_task = current_task
