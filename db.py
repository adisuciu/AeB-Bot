import psycopg2
from common import log
import os

url = os.environ.get('DATABASE_URL', "localhost")
user = os.environ.get('DATABASE_USER', "postgres")
password = os.environ.get('DATABASE_PASSWORD', "password")
port = os.environ.get('DATABASE_PASSWORD', "5432")
db = os.environ.get('DATABASE_DATABASE', "postgres")


def connect():
    if url == "localhost":
        return psycopg2.connect(
            user=user,
            password=password,
            host=url,
            port=port,
            database=db
        )
    else:
        return psycopg2.connect(url, sslmode='require')


def nuke(db):
    runcmd("DELETE FROM %s *") % (db)
    pass


def create_if_doesnt_exist(db):
    connection = connect()
    verify_table_query = """SELECT * FROM pg_tables WHERE tablename='%s'""" % (db)
    cursor = connection.cursor()
    cursor.execute(verify_table_query)
    tables = cursor.fetchall()
    if len(tables) == 1:
        return True

    log("TABLE %s DOESN'T EXIST .. CREATING" % (db))
    create_table_query = '''
            CREATE TABLE %s
            (
                id      TEXT PRIMARY KEY NOT NULL,
                value   TEXT NOT NULL
            ); ''' % (db)
    runcmd(create_table_query)
    return False


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


def insert(db, id, value):
    postgres_insert_query = """ INSERT INTO %s (ID, VALUE) VALUES (%s,%s)""" % (db, "%s", "%s")
    record_to_insert = (id, value)
    runcmd(postgres_insert_query, record_to_insert)


def update(db, id, value):
    sql_update_query = """UPDATE %s set VALUE = %s where id = %s""" % (db, "%s", "%s")
    record_to_update = (value, id)
    runcmd(sql_update_query, record_to_update)


def delete(db, id):
    sql_delete_query = """DELETE FROM %s WHERE id = %s""" % (db, "%s")
    record_to_delete = (id,)
    runcmd(sql_delete_query, record_to_delete)


def select(db, id):
    dict = {}
    try:
        connection = connect()
        cursor = connection.cursor()
        if id == "*":
            postgreSQL_select_Query = "SELECT * FROM %s" % (db)
        else:
            postgreSQL_select_Query = "SELECT * FROM %s where id = %s" % (db, "%s")

        cursor.execute(postgreSQL_select_Query, (id,))
        all_links = cursor.fetchall()
        for link in all_links:
            dict[link[0]] = link[1]

    except (Exception, psycopg2.Error) as error:
        print("Error while fetching data from PostgreSQL", error)

    finally:
        # closing database connection.
        if (connection):
            cursor.close()
            connection.close()
    return dict
