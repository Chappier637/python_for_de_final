from adapters.pg_adapter import PostgresAdapter


# Возвращает тапл данных, из заданной таблицы по заданным колонкам
def pg_fetch_table(table_name, columns):
    columns_string = ', '.join(f'"{col}"' for col in columns)
    sql_query = f"SELECT {columns_string} FROM {table_name}"
    pg_conn = PostgresAdapter()
    rows = pg_conn.execute_custom_query(sql_query)
    return rows

