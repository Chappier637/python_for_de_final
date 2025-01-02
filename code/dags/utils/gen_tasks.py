import yaml
import os
from operators.python_insert_operator import MySQLInsertOperator
from adapters.mysql_adaper import MySQLAdapter

CONFIG_EXT = ('.yml', '.yaml')

def create_task(config):
    table = config.get('table')
    sql = config.get('sql')
    task_type = config.get('task_type')
    if task_type == 'insert':
        connector = MySQLAdapter()
        task = MySQLInsertOperator(table = table, insert_sql=sql, connector=connector)
        return task
    else:
        raise NotImplementedError()
        
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
    configs = [config for config, dir_name, parent_dir_name, yaml_file_name in iter_tasks_directory(tasks_dir)]
    for config in configs:
        task = create_task(config)
        task



