import os

import psycopg2
from psycopg2 import sql
from psycopg2 import errors
from psycopg2.extras import RealDictCursor
from psycopg2 import OperationalError

import config
from db.exceptions import ConnectDBError

SUPER_DBNAME = 'postgres'
SUPER_DBUSER = 'postgres'
SUPER__DBPASSWORD = '33hfpfASD'
SUPER_DBHOST = '127.0.0.1'
SUPER_DBPORT = '5432'

QUERIES_DIR = os.path.join(os.path.dirname(__file__), 'sql_queries')


class ConnectorDB:

    def __init__(self,
                 dbname=config.DBNAME,
                 user=config.DBUSER,
                 password=config.DBPASSWORD,
                 host=config.DBHOST,
                 port=config.DBPORT,
                 autocommit=False):

        self.dbname = dbname
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.cursor = None
        self.connection = None
        self.autocommit = autocommit

    def __enter__(self):
        try:
            connection = psycopg2.connect(dbname=self.dbname,
                                          user=self.user,
                                          password=self.password,
                                          host=self.host,
                                          port=self.port)
        except OperationalError:
            raise ConnectDBError('Error of connection to DB.')

        connection.autocommit = self.autocommit
        cursor = connection.cursor(cursor_factory=RealDictCursor)
        self.connection = connection
        self.cursor = cursor

        return cursor

    def __exit__(self, exc_type, exc_value, traceback):
        self.connection.commit()
        self.cursor.close()
        self.connection.close()


def initialize_db():
    connector = ConnectorDB(dbname=SUPER_DBNAME,
                            user=SUPER_DBUSER,
                            password=SUPER__DBPASSWORD,
                            host=SUPER_DBHOST,
                            port=SUPER_DBPORT,
                            autocommit=True)
    with connector as cursor:
        path_init_database = os.path.join(QUERIES_DIR, 'init_database.sql')
        path_init_user = os.path.join(QUERIES_DIR, 'init_user.sql')
        path_init_tables = os.path.join(QUERIES_DIR, 'init_tables.sql')

        try:
            with open(path_init_database) as query_init_database:
                query_init_database = sql.SQL(
                    query_init_database.read()).format(
                    dbname=sql.Identifier(config.DBNAME))
                cursor.execute(query_init_database)
        except errors.DuplicateDatabase:
            pass

        try:
            with open(path_init_user) as query_init_user:
                query_init_user = sql.SQL(
                    query_init_user.read()).format(
                    dbuser=sql.Identifier(config.DBUSER),
                    dbname=sql.Identifier(config.DBNAME))
                cursor.execute(query_init_user,
                               {'dbpassword': config.DBPASSWORD})
        except errors.DuplicateObject:
            pass
    connector = ConnectorDB()

    with connector as cursor:
        with open(path_init_tables) as query_init_tables:
            cursor.execute(query_init_tables.read())


initialize_db()
