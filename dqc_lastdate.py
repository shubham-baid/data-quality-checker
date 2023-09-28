import mysql.connector
import sqlite3
from datetime import date


def check_last_date(db_name,table_name):
   
    # Connect to the database
    conn = mysql.connector.connect(host='localhost',port= 3306,user='root',password='root',database='test')

    # Create a cursor object to execute SQL queries
    cursor = conn.cursor()

    
    # Form query to fetch column name and data
    query = """select column_name, data_type 
    from INFORMATION_SCHEMA.COLUMNS 
    where table_name = '{}'
    and table_schema = '{}';""".format(table_name,db_name)
    
    # Execute the query to get column names and types
    cursor.execute(query)
    column_list = cursor.fetchall()

    # Iterate through the result to find the date column
    date_column = None
    for column_name, data_type in column_list:
        if 'date' in data_type.lower():
            date_column = column_name
            break
    
    # If a date column is found, check if current date is present
    if date_column:
        current_date = date.today()
        date_query = f"""
            SELECT COUNT(*)
            FROM {table_name}
            WHERE {date_column} = %s;
        """
        cursor.execute(date_query, (current_date,))
        count = cursor.fetchone()[0]

        if count == 0:
            print(f"Alert: Current date ({current_date}) is not present in the data.")
        else: 
            print('System up to date.')
    
    else:
        print(f"No date column found in the table {table_name}")

    # Close the cursor and connection
    cursor.close()
    conn.close()


# Example usage
db_name = 'test'
table_name = 'dummy_table'

check_last_date(db_name, table_name)
