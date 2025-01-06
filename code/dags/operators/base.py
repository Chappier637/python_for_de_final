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
    