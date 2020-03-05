from psycopg2 import sql

from models import models
from db import ConnectorDB


class AbstractDAO:
    connector = ConnectorDB()

    def _get_name_table(self):
        name_table = ''
        for char in self.__class__.__name__.rstrip('DAO'):
            if char.isupper():
                name_table += '_' + char.lower()
            else:
                name_table += char
        name_table = name_table.lstrip('_')

        return name_table

    def _get_names_fields(self, obj):
        names_fields = []
        for field, value in vars(obj).items():
            if not value:
                continue
            names_fields.append(field)

        return names_fields

    def create(self, obj):
        with self.connector as cursor:
            name_table = self._get_name_table()

            names_fields = self._get_names_fields(obj)
            query = sql.SQL('''INSERT INTO {} ({}) VALUES({})
                            RETURNING *''').format(
                sql.Identifier(name_table),
                sql.SQL(', ').join(map(sql.Identifier, names_fields)),
                sql.SQL(', ').join(map(sql.Placeholder, names_fields)))
            cursor.execute(query, vars(obj))

            for field, value in cursor.fetchall()[0].items():
                obj.__dict__[field] = value

    def update(self, obj):
        with self.connector as cursor:
            name_table = self._get_name_table()

            names_fields = self._get_names_fields(obj)

            query = sql.SQL('UPDATE {} SET ({}) = ({})  WHERE {} = {}').format(
                sql.Identifier(name_table),
                sql.SQL(', ').join(map(sql.Identifier, names_fields)),
                sql.SQL(', ').join(map(sql.Placeholder, names_fields)),
                sql.Identifier(names_fields[0]),
                sql.Placeholder(names_fields[0]))
            cursor.execute(query, vars(obj))

    def delete(self, obj):
        with self.connector as cursor:
            name_table = self._get_name_table()

            names_fields = self._get_names_fields(obj)

            query = sql.SQL('DELETE FROM {} WHERE {} = {}').format(
                sql.Identifier(name_table),
                sql.Identifier(names_fields[0]),
                sql.Placeholder(names_fields[0]))
            cursor.execute(query, vars(obj))


class CustomerDAO(AbstractDAO):
    def get_customer_by_id(self, customer_id):
        with self.connector as cursor:
            connection, cursor = self._get_connection()
            cursor.execute('SELECT * FROM customer WHERE id = %s',
                           (customer_id,))
            customer = cursor.fetchone()

            return models.Customer(*customer)


class ReportFoodDAO(AbstractDAO):
    pass


class ReportSizesBodyDAO(AbstractDAO):
    pass


class NormalFoodDAO(AbstractDAO):
    pass
