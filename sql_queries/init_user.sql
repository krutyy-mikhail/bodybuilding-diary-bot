CREATE USER {dbuser} WITH ENCRYPTED PASSWORD %(dbpassword)s;

GRANT ALL PRIVILEGES ON DATABASE {dbname} TO {dbuser};