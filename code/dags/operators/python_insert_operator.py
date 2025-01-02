from airflow.models import BaseOperator

class BasePorjectOperator(BaseOperator):
    def __init__(self, *args, pool=None, labels=None, severity="high", **kwargs):
        self.labels = labels
        self.severity = severity
        super().__init__(pool=pool, *args, **kwargs)
    
    def execute(self, context):
        return self.run_task()
    
    def run_task(self):
        raise NotImplementedError()
    
class MySQLInsertOperator(BasePorjectOperator):
    def __init__(self, *args, insert_sql, table, connector, **kwargs):
        self.insert_sql = insert_sql
        self.table = table
        self.connector = connector
        super().__init__(task_id = table)

    # def create_insert_query(self):
    #     with open(self.insert_sql) as file:
    #         query = file.read()
    #     return insert_query

    def run_task(self):
        with open(self.insert_sql) as file:
            query = file.read()
        self.connector.execute_commit_query(query)
            