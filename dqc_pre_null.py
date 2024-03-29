import mysql.connector
import sqlite3

def check_null(db_name, table_name, columns):
    # Connect to the database
    
    conn = mysql.connector.connect(host='localhost',port= 3306,user='root',password='root',database='test')

    # Create a cursor object to execute SQL queries
    cursor = conn.cursor()

    # Get the list of column names when all columns to be searched
    if(columns == '*'):
        cursor.execute(f"select column_name from INFORMATION_SCHEMA.COLUMNS where table_name = {table_name}and table_schema = {db_name};")
        tuple_columns = cursor.fetchall()
        str_columns = ', '.join([column[0] for column in tuple_columns])

         # Formulate the SQL query
        query = f"SELECT {str_columns} FROM {table_name} WHERE {' OR '.join([f'{col[0]} IS NULL' for col in tuple_columns])}"
        
    
    else:
        str_columns = ', '.join(columns)
        query = f"SELECT {str_columns} FROM {table_name} WHERE {' OR '.join([f'{col} IS NULL' for col in columns])}"


    # # Execute the query
    cursor.execute(query)

    # # Fetch the results
    null_rows = cursor.fetchall()
    print(null_rows)

    # If there are null values, print
    if null_rows:
        print("Null Values Found in {}".format(table_name))
    else:
        print("All is well")

    # Close the connection
    conn.close()


# Example usage
db_name = "test"
table_name = "dummy_table"
columns = ['id','age']

check_null(db_name, table_name, columns)
