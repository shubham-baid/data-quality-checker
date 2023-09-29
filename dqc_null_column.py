import sqlite3
import mysql.connector

def check_null_values_multiple_columns(db_name, table_name, column_names):
    try:
        # Connect to the database
        conn = mysql.connector.connect(host='localhost',port= 3306,user='root',password='root',database='test')

        # Create a cursor object to execute SQL queries
        cursor = conn.cursor()

        # Initialize a dictionary to store null counts
        null_counts = {}

        if(column_names == '*'):
            cursor.execute(f"select column_name from INFORMATION_SCHEMA.COLUMNS where table_name = '{table_name}' and table_schema = '{db_name}';")
            columns = cursor.fetchall()
            column_names = [column[0] for column in columns]
        
        for column_name in column_names:
            # Formulate the SQL query to count null values in the column
            query = f"SELECT COUNT(*) FROM {table_name} WHERE {column_name} IS null;"

            # Execute the query
            cursor.execute(query)

            # Fetch the result
            null_count = cursor.fetchone()[0]

            ## Store and print the number of null values for the column if non-zero
            if(null_count != 0):

                # Store the count in the dictionary
                null_counts[column_name] = null_count

                # Print the number of null values for the column
                print(f"Number of null values in column '{column_name}': {null_count}")

        # Close the connection
        conn.close()

    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
db_name = "test"
table_name = "dummy_table"
column_names = "*"  

check_null_values_multiple_columns(db_name, table_name, column_names)
