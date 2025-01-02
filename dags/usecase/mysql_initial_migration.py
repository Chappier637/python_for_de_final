from adapters.mysql_adaper import MySQLAdapter


def mysql_init_migration():
    msql_conn = MySQLAdapter()
    with open("/opt/airflow/dags/sql/mysql_migration.sql") as file:
        sql_query = file.read()
    rows = msql_conn.execute_commit_query(sql_query)