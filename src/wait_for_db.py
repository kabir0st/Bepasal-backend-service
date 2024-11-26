import time
import psycopg2
from psycopg2 import OperationalError
import os


def wait_for_db():
    db_name = os.getenv('DB_NAME')
    db_user = os.getenv('DB_USER')
    db_password = os.getenv('DB_PASSWORD')
    db_host = 'db'
    db_port = '5432'

    # Wait for the PostgreSQL server to be up
    while True:
        try:
            conn = psycopg2.connect(
                dbname='postgres',  # Connect to the default database
                user=db_user,
                password=db_password,
                host=db_host,
                port=db_port)
            conn.close()
            print("Database server is up!")
            break
        except OperationalError:
            print("Database server not ready, waiting...")
            time.sleep(5)

    # After the server is up, check if the database exists and create it if not
    create_database(db_name, db_user, db_password, db_host, db_port)


def create_database(db_name, db_user, db_password, db_host, db_port):
    try:
        conn = psycopg2.connect(dbname='postgres',
                                user=db_user,
                                password=db_password,
                                host=db_host,
                                port=db_port)
        conn.autocommit = True  # Enable autocommit to execute CREATE DATABASE
        with conn.cursor() as cursor:
            cursor.execute(
                f"SELECT 1 FROM pg_database WHERE datname = '{db_name}'")
            exists = cursor.fetchone()
            if not exists:
                print(f"Database '{db_name}' does not exist. Creating...")
                cursor.execute(f"CREATE DATABASE {db_name}")
                print(f"Database '{db_name}' created!")
            else:
                print(f"Database '{db_name}' already exists.")
    except OperationalError as e:
        print(f"Error creating database: {e}")
    finally:
        conn.close()


if __name__ == "__main__":
    wait_for_db()
