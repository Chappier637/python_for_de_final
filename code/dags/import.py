from airflow import DAG

from utils.default_args import DEFAULT_ARGS
from utils.gen_tasks import gen_tasks

with DAG(
    dag_id="import",
    default_args=DEFAULT_ARGS,
    tags=["import"],
    catchup=False
) as dag:
    gen_tasks(dag, 'import')