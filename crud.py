""" 
    @Author: Deven Gupta
    @Date: 24-08-2024
    @Last Modified by: Deven Gupta
    @Last Modified time: 24-08-2024
    @Title : Python program to Perform CRUD in MSSQL using python

"""

import pyodbc
import os
from dotenv import load_dotenv

load_dotenv()
class DatabaseManager:
    SYSTEM_DATABASES = {'master', 'tempdb', 'model', 'msdb'}
    
    def __init__(self, server, username, password):
        self.connection_string = f'DRIVER={{ODBC Driver 18 for SQL Server}};SERVER={server};UID={username};PWD={password};TrustServerCertificate=yes'

    def connect(self, database=None):
        """
        Description :
            This function is used to Establish a connection to the SQL Server instance or specific database
        Parameters :
            database : name of database
        return :
            connection 
            
         """
        conn_str = f'{self.connection_string};DATABASE={database}' if database else self.connection_string
        return pyodbc.connect(conn_str,autocommit=True)

    def create_database(self, cursor, db_name):
        """
        Description :
            This function is used to Create database
        Parameters :
            cursor : To execute query
            db_name : name of database
        return :
            None 
            
        """
        if db_name in self.SYSTEM_DATABASES:
            print("Cannot create system database.")
            return
        try:
            cursor.execute(f"CREATE DATABASE {db_name}")
            print(f"Database '{db_name}' created successfully!")
        except Exception as e:
            print(f"Error: {e}")

    def drop_database(self, cursor, db_name):
        """
        Description :
            This function is used to Drop an existing database.
        Parameters :
            cursor : To execute query
            db_name : name of database
        return :
            None 
        """
        if db_name in self.SYSTEM_DATABASES:
            print("Cannot drop system database.")
            return
        try:
            cursor.execute(f"DROP DATABASE {db_name}")
            print(f"Database '{db_name}' dropped successfully!")
        except Exception as e:
            print(f"Error: {e}")

    def list_databases(self, cursor):
        """
        Description :
            This function is used to List all databases on the SQL Server instance.
        Parameters :
            cursor : To execute query
        return :
            None 
        """
        try:
            cursor.execute("SELECT name FROM sys.databases WHERE name NOT IN ('master', 'tempdb', 'model', 'msdb')")
            databases = cursor.fetchall()
            print("Databases:")
            for db in databases:
                print(db.name)
        except Exception as e:
            print(f"Error: {e}")

    def create_table(self, cursor):
        """
        Description :
            This function is used to Create a table with user-defined columns.
        Parameters :
            cursor : To execute query
        return :
            None 
        """
        table_name = input("Enter the name of the table to create: ")
        columns = []
        while True:
            column_name = input("Enter column name (or 'done' to finish): ")
            if column_name.lower() == 'done':
                break
            column_type = input(f"Enter data type for column '{column_name}' (e.g., INT, NVARCHAR(100)): ")
            columns.append(f"{column_name} {column_type}")
        
        columns_sql = ', '.join(columns)
        create_table_sql = f"CREATE TABLE {table_name} ({columns_sql})"
        
        try:
            cursor.execute(create_table_sql)
            print(f"Table '{table_name}' created successfully!")
        except Exception as e:
            print(f"Error: {e}")

    def drop_table(self, cursor):
        """
        Description :
            This function is used to Drop a table.
        Parameters :
            cursor : To execute query
        return :
            None 
        """
        table_name = input("Enter the name of the table to drop: ")
        drop_table_sql = f"DROP TABLE {table_name}"
        try:
            cursor.execute(drop_table_sql)
            print(f"Table '{table_name}' dropped successfully!")
        except Exception as e:
            print(f"Error: {e}")

    def insert_data(self, cursor):
        """
        Description :
            This function is used to Insert data into a table.
        Parameters :
            cursor : To execute query
        return :
            None 
        """
        table_name = input("Enter the name of the table to insert data into: ")
        
        # Retrieve column names to construct insert statement
        cursor.execute(f"SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '{table_name}'")
        columns = [row.COLUMN_NAME for row in cursor.fetchall()]
        
        column_names = ', '.join(columns)
        placeholders = ', '.join(['?' for _ in columns])
        insert_data_sql = f"INSERT INTO {table_name} ({column_names}) VALUES ({placeholders})"
        
        values = [input(f"Enter value for column '{col}': ") for col in columns]
        
        try:
            cursor.execute(insert_data_sql, values)
            cursor.connection.commit()
            print("Data inserted successfully!")
        except Exception as e:
            print(f"Error: {e}")

    def query_data(self, cursor):
        """
        Description :
            This function is used to Show data from a table.
        Parameters :
            cursor : To execute query
        return :
            None 
        """
        table_name = input("Enter the name of the table to query: ")
        query_sql = f"SELECT * FROM {table_name}"
        try:
            cursor.execute(query_sql)
            rows = cursor.fetchall()
            for row in rows:
                print(row)
        except Exception as e:
            print(f"Error: {e}")

    def perform_database_operations(self, database):
        """
        Description :
            This function is used to Perform operations on a specific database.
        Parameters :
            database : name of database
        return :
            None 
        """
        while True:
            print(f"\nOperations for Database '{database}'")
            print("1. Create Table")
            print("2. Drop Table")
            print("3. Insert Data")
            print("4. Query Data")
            print("5. Back to Main Menu")

            choice = input("Enter your choice (1-5): ")

            conn = self.connect(database)
            cursor = conn.cursor()
                
            if choice == '1':
                self.create_table(cursor)
            
            elif choice == '2':
                self.drop_table(cursor)
            
            elif choice == '3':
                self.insert_data(cursor)
            
            elif choice == '4':
                self.query_data(cursor)
            
            elif choice == '5':
                break
            
            else:
                print("Invalid choice. Please enter a number between 1 and 5.")

def main():
    server = 'localhost'
    username = os.getenv('DB_USERNAME')
    password = os.getenv('DB_PASSWORD')

    db_manager = DatabaseManager(server, username, password)

    while True:
        print("\nDatabase Management Menu")
        print("1. Create Database")
        print("2. Drop Database")
        print("3. List Databases")
        print("4. Perform Operations on a Database")
        print("5. Exit")

        choice = input("Enter your choice (1-5): ")

        if choice == '1':
            db_name = input("Enter the name of the database to create: ")
            conn = db_manager.connect()
            cursor = conn.cursor()
            db_manager.create_database(cursor, db_name)
            conn.commit()
    
        elif choice == '2':
            db_name = input("Enter the name of the database to drop: ")
            conn = db_manager.connect()
            cursor = conn.cursor()
            db_manager.drop_database(cursor, db_name)
            conn.commit()
        
        elif choice == '3':
            conn = db_manager.connect()
            cursor = conn.cursor()
            db_manager.list_databases(cursor)
        
        elif choice == '4':
            db_name = input("Enter the name of the database to perform operations on: ")
            if db_name not in DatabaseManager.SYSTEM_DATABASES:
                db_manager.perform_database_operations(db_name)
            else:
                print("Cannot perform operations on a system database.")
        
        elif choice == '5':
            print("Exiting...")
            break
        
        else:
            print("Invalid choice. Please enter a number between 1 and 5.")

if __name__ == "__main__":
    main()
