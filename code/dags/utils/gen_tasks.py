import os

import yaml
from operators.mysql_insert import MySQLInsertOperator
from operators.spark_import import SparkImportOperator
from adapters.mysql_adapter import MySQLAdapter

CONFIG_EXT = ('.yml', '.yaml')

def create_task(config: dict):
    """This function creates task from configuration dictionary

    Args:
        config (dict): Dictionary with params for task
        Parameters:
            task_type: Type of future task. Must be insert or import
            table: For task_type=import it is a name of table in source database
                   For task_type=insert it is target table
            conn_id: ID of connector to source database
            target_conn_id: ID if connector to target database
            target_table: Name of table in target database 
            sql: SQL file addres for data tranformation

    Returns:
        Airflow task
    """    
    task_type = config.get('task_type')
    table = config.get('table')
    sql = config.get('sql')
    conn_id = config.get('conn_id')
    target_conn_id = config.get('target_conn_id')
    target_table = config.get('target_table')
    if task_type == 'insert':
        connector = MySQLAdapter()
        task = MySQLInsertOperator(table=table, insert_sql=sql, connector=connector)
        return task
    if task_type == 'import':
        task = SparkImportOperator(table=table, conn_id=conn_id, target_conn_id=target_conn_id, target_table=target_table)
        return task
    else:
        raise ValueError('task_type must be insert or import')
        
def iter_tasks_directory(d = 'marts'):
    tasks_dir = "/opt/airflow/tasks/" + d
    for dir_path, _, yaml_tasks_list in os.walk(tasks_dir):
        parent_path, dir_name = os.path.split(dir_path)
        _, parent_dir_name = os.path.split(parent_path)

        for yaml_file_name in yaml_tasks_list:
            if not yaml_file_name.endswith(CONFIG_EXT):
                continue
            with open(tasks_dir + '/' + yaml_file_name) as file:        
                config = yaml.safe_load(file)
            yield config, dir_name, parent_dir_name, yaml_file_name
        
def gen_tasks(dag, tasks_dir):
    """Generates tasks in DAG

    Args:
        dag (DAG): Airflow dag where tasks will be executed
        tasks_dir (string): Directory where tasks located
        
    """    
    configs = [config for config, dir_name, parent_dir_name, yaml_file_name in iter_tasks_directory(tasks_dir)]
    for config in configs:
        task = create_task(config)
        task



