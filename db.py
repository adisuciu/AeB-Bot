import psycopg2
from common import log
import os

url = os.environ.get('DATABASE_URL', "localhost")
user = os.environ.get('DATABASE_USER', "postgres")
password = os.environ.get('DATABASE_PASSWORD', "password")
port = os.environ.get('DATABASE_PASSWORD', "5432")
db = os.environ.get('DATABASE_DATABASE',"postgres")

def connect():
    return psycopg2.connect(user=user,
                            password=password,
                            host=url,
                            port=port,
                            database=db)


def nuke():
    runcmd("delete from links *")
    pass


def create_if_doesnt_exist():
    connection = connect()
    verify_table_query = """select * from pg_tables where tablename='links'"""
    cursor = connection.cursor()
    cursor.execute(verify_table_query)
    tables = cursor.fetchall()
    if len(tables) == 1:
        return

    log("TABLE DOESN'T EXIST .. CREATING")
    create_table_query = '''CREATE TABLE LINKS
             (id TEXT PRIMARY KEY     NOT NULL,
             value           TEXT    NOT NULL); '''
    runcmd(create_table_query)


def runcmd(query, vars=None):
    count = 0
    try:
        connection = connect()
        cursor = connection.cursor()
        cursor.execute(query, vars)
        connection.commit()
        count = cursor.rowcount
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error while running PostgreSQL cmd %s - errorcode %s" % (query, error))
    finally:
        # closing database connection.
        if (connection):
            cursor.close()
            connection.close()
    return count


def insert(id, value):
    postgres_insert_query = """ INSERT INTO LINKS (ID, VALUE) VALUES (%s,%s)"""
    record_to_insert = (id, value)
    runcmd(postgres_insert_query, record_to_insert)


def update(id, value):
    sql_update_query = """Update LINKS set VALUE = %s where id = %s"""
    record_to_update = (value, id)
    runcmd(sql_update_query, record_to_update)


def delete(id):
    sql_delete_query = """Delete from LINKS where id = %s"""
    record_to_delete = (id,)
    runcmd(sql_delete_query, record_to_delete)


def select(id):
    dict = {}
    try:
        connection = connect()
        cursor = connection.cursor()
        if id=="*":
            postgreSQL_select_Query = "select * from LINKS"
        else:
            postgreSQL_select_Query = "select * from LINKS where id = %s"

        cursor.execute(postgreSQL_select_Query, id)
        all_links = cursor.fetchall()
        for link in all_links:
            dict[link[0]]=link[1]

    except (Exception, psycopg2.Error) as error:
        print("Error while fetching data from PostgreSQL", error)

    finally:
        # closing database connection.
        if (connection):
            cursor.close()
            connection.close()
    return dict
