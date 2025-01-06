from operators.base import BasePorjectOperator
    
class MySQLInsertOperator(BasePorjectOperator):
    def __init__(self, *args, insert_sql, table, connector, **kwargs):
        self.insert_sql = insert_sql
        self.table = table
        self.connector = connector
        super().__init__(task_id = table)

    def run_task(self):
        with open(self.insert_sql) as file:
            query = file.read()
        self.connector.execute_commit_query(query)
            