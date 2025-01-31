from airflow import DAG

from utils.default_args import DEFAULT_ARGS
from utils.gen_tasks import gen_tasks

with DAG(
    dag_id="data_marts",
    default_args=DEFAULT_ARGS,
    tags=["data_marts"],
    catchup=False
) as dag:
    gen_tasks(dag, 'marts')