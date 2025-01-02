from adapters.mysql_adaper import MySQLAdapter


# Вставляет данные в таргет таблицу по таргет колонкам
def mysql_insert_data(table_to_insert, rows, columns):
    columns_string = ', '.join(f'`{col}`' for col in columns)
    placeholders = ', '.join(['%s'] * len(rows[0]))  # One placeholder for each column
    sql_query = f"REPLACE INTO `{table_to_insert}` ({columns_string}) VALUES ({placeholders})"
    msql_conn = MySQLAdapter()
    msql_conn.execute_commit_query(sql_query, rows)