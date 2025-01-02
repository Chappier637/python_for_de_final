from adapters.mysql_adaper import MySQLAdapter


# Вставляет данные в таргет таблицу по таргет колонкам
def sale_analisys():
    msql_conn = MySQLAdapter()
    with open("/opt/airflow/dags/sql/data_mart.sql") as file:
        sql_query = file.read()
    rows = msql_conn.execute_commit_query(sql_query)