import mysql.connector
import sqlite3

def check_null(db_name, table_name, columns):
    # Connect to the database
    conn = mysql.connector.connect(host='localhost',port= 3306,user='root',password='root',database='test')

    # Create a cursor object to execute SQL queries
    cursor = conn.cursor()

    
    #Check if number_columns already present or not (helps when passing multiple queries)
    cursor.execute(f"select column_name from INFORMATION_SCHEMA.COLUMNS where table_name = '{table_name}'and table_schema = '{db_name}';")
    existing_columns = [column[0] for column in cursor.fetchall()]

    if 'number_columns' not in existing_columns:    
        query = f"ALTER TABLE {table_name} ADD COLUMN number_columns INT AUTO_INCREMENT PRIMARY KEY;"
        cursor.execute(query)

    
    # Get the list of column names when all columns to be searched
    if(columns == '*'):
        cursor.execute(f"select column_name from INFORMATION_SCHEMA.COLUMNS where table_name = '{table_name}' and table_schema = '{db_name}';")
        columns = cursor.fetchall()
        str_columns = ', '.join([column[0] for column in columns])

         # Formulate the SQL query
        query = f"SELECT number_columns, {str_columns} FROM {table_name} WHERE {' OR '.join([f'{col[0]} IS NULL' for col in columns])}"
      
    else:
        str_columns = ', '.join(columns)
        print(str_columns)
        query = f"SELECT number_columns, {str_columns} FROM {table_name} WHERE {' OR '.join([f'{col} IS NULL' for col in columns])}"
         
        
    # # Execute the query
    cursor.execute(query)

    # Fetch the results
    null_rows = cursor.fetchall()
    
    
    # If there are null values, print the column names and row positions
    if null_rows:
        null_columns = set()
        for row in null_rows:
            for i, value in enumerate(row[1:]):
                if value is None:
                    null_columns.add((columns[i], row[0]))

        print("Null values found in:")
        for column, row_position in null_columns:
            print(f"Column: {column}, Row Position: {row_position}")
    else:
        print("No null values found in any column.")


    # Close the connection
    conn.close()


# Example usage
db_name = "test"
table_name = "dummy_table"
columns = '*'

check_null(db_name, table_name, columns)
