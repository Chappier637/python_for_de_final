from adapters.pg_adapter import PostgresAdapter


# Начальная миграция данных в Postgres
def pg_init_migration():
    pg_conn = PostgresAdapter()
    with open("/opt/airflow/dags/queries/pg_migration.sql") as file:
        sql_query = file.read()
    rows = pg_conn.execute_commit_query(sql_query)