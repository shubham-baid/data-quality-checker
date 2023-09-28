import mysql.connector
import sqlite3

def date_min_max(db_name,table_name):
   
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

    # Iterate through the result to find the date column
    date_column = None
    for column_name, data_type in cursor:
        if 'date' in data_type.lower():
            date_column = column_name
            break
    
    
    # If a date column is found, get the minimum and maximum values

    if date_column:
        date_query = f"""
            SELECT MIN({date_column}), MAX({date_column})
            FROM {table_name}
        """
        cursor.execute(date_query)
        min_date, max_date = cursor.fetchone()

        print(f"Minimum date: {min_date}")
        print(f"Maximum date: {max_date}")
    else:
        print(f"No date column found in the table {table_name}")

    # Close the cursor and connection
    cursor.close()
    conn.close()


# Example usage
db_name = 'test'
table_name = 'dummy_table'

date_min_max(db_name, table_name)

