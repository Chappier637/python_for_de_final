from airflow.models.o import BaseOperator

class BasePorjectOperator(BaseOperator):
    def __init__(self, *args, pool=None, labels=None, severity="high", **kwargs):
        self.labels = labels
        self.severity = severity
        super().__init__(pool=pool, *args, **kwargs)
    
    def execute(self):
        return self.run_task()
    
    def run_task(self):
        raise NotImplementedError()
    
class PythonInsertOperator(BasePorjectOperator):
    def __init__(self, insert_sql, table):
