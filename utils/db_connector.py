import mysql.connector
from mysql.connector import errorcode

def connect_database(user, password, host):
    try:
        conn = mysql.connector.connect(user=user, password=password, host=host)

        if conn.is_connected():
            return conn
        else:
            return None
        
    except mysql.connector.Error as e:
        
        error_details = {
            "error_code": e.errno,
            "sqlstate": e.sqlstate,
            "error_message": e.msg
        }
        return error_details
    
def load_databases(conn):
    query = "SHOW DATABASES"
    
    with conn.cursor() as cur:
        try:
            cur.execute(query)
            databases = cur.fetchall()

            return databases

        except mysql.connector.Error as e:
            error_details = {
            "error_code": e.errno,
            "sqlstate": e.sqlstate,
            "error_message": e.msg
            }
            return error_details

def load_tables(conn, database):
    query_tables = "SHOW TABLES"

    with conn.cursor() as cur:
        try:
            cur.execute(f"USE {database}")
            cur.execute(query_tables)
            tables = cur.fetchall()

            return tables

        except mysql.connector.Error as e:
            error_details = {
            "error_code": e.errno,
            "sqlstate": e.sqlstate,
            "error_message": e.msg
            }
            return error_details
        
def get_columns_name(conn, table):
    with conn.cursor() as cur:
        try:
            cur.execute(f"SHOW COLUMNS FROM {table}")
            columns = cur.fetchall()

            return columns

        except mysql.connector.Error as e:
            error_details = {
            "error_code": e.errno,
            "sqlstate": e.sqlstate,
            "error_message": e.msg
            }
            return error_details

def get_data(conn, table):
    with conn.cursor() as cur:
        try:
            cur.execute(f"SELECT * FROM {table}")
            data = cur.fetchall()

            return data

        except mysql.connector.Error as e:
            error_details = {
            "error_code": e.errno,
            "sqlstate": e.sqlstate,
            "error_message": e.msg
            }
            return error_details

def create_table(conn, table, attributes):
    with conn.cursor() as cur:
        try:
            sql = f"CREATE TABLE {table} ({', '.join(attributes)})"
            cur.execute(sql)
            return True  

        except mysql.connector.Error as e:
            error_details = {
                "error_code": e.errno,
                "sqlstate": e.sqlstate,
                "error_message": e.msg
            }
            return False, error_details 
