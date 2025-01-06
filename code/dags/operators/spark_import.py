from operators.base import BasePorjectOperator
from pyspark.sql import SparkSession
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.providers.mysql.hooks.mysql import MySqlHook
import logging

DRIVER_MAPPING = {
    'pg':'org.postgresql.Driver',
    'mysql':'com.mysql.cj.jdbc.Driver'
}

HOOK_MAPPING ={
    'pg':PostgresHook.get_connection('pg'),
    'mysql':MySqlHook.get_connection('mysql')
}

SPARK_JARS = "/opt/airflow/spark/jars/postgresql-42.2.18.jar,/opt/airflow/spark/jars/mysql-connector-java-8.3.0.jar"

def gen_connection_url(conn):
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

class SparkImportOperator(BasePorjectOperator):
    
    def __init__(self, *args, table, conn_id, target_conn_id, target_table, **kwargs):
        self.conn_id = conn_id
        self.table = table
        self.target_conn_id = target_conn_id
        self.target_table = target_table
        super().__init__(task_id = table)
        
    def run_task(self):
        spark = (
        SparkSession.builder
        .appName("Spark_import_app")
        .config("spark.jars", SPARK_JARS)
        .getOrCreate()
        )
        
        logging.info('Spark session created')
        
        df = (
            spark.read
            .format("jdbc")
            .option("url", gen_connection_url(HOOK_MAPPING.get(self.conn_id)))
            .option("driver", DRIVER_MAPPING.get(self.conn_id))
            .option("dbtable", self.table)
            .load()
        )
        
        logging.info('Data from source table received')
        
        (df.write 
            .format('jdbc') 
            .option('url', gen_connection_url(HOOK_MAPPING.get(self.target_conn_id)))
            .option('driver', DRIVER_MAPPING.get(self.target_conn_id))
            .option('dbtable', self.target_table)
            .mode('overwrite')
            .save()
            )
        
        logging.info(f'Import of {self.table} is successful')
        
        spark.stop()