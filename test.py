with open("./dags/sql/data_mart.sql") as file:
            sql_query = file.read()

print(sql_query)