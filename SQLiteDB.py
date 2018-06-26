from config import *
from generic_DB import GenericDB

import sqlite3


class SQLiteDB(GenericDB):

    def __init__(self):
        self.dbconn = None

    def open(self, *args, **kwargs):
        self.dbconn = sqlite3.connect(DATABASE)
        return self

    def close(self):
        self.dbconn.commit()
        return self.dbconn.close()

    def connection(self, *args, **kwargs):
        pass

    def table_exist(self, table=TABLE):
        c = self.dbconn.cursor()
        c.execute('SELECT * FROM sqlite_master WHERE type=\'table\' AND name=?', (table,))

        return c.fetchone()# is not None

    def table_type(self, table=TABLE):
        assert False

    def drop_table(self, table=TABLE):
        c = self.dbconn.cursor()
        c.execute('DROP TABLE IF EXISTS ' + table)
        return True

    def create_table(self, format, table=TABLE):
        schema = ', '.join(map(lambda e: e[0], format))

        c = self.dbconn.cursor()
        c.execute('CREATE TABLE IF NOT EXISTS ' + table + ' (' + schema + ') ')
        return True

    def append_line(self, line, table=TABLE):
        v = '(?' + ', ?'*(len(line)-1) + ') '

        c = self.dbconn.cursor()
        c.execute('INSERT INTO ' + table + ' VALUES ' + v, line)
        return True

    def append_lines(self, tab, table=TABLE):
        v = '(?' + ', ?'*(len(tab[0])-1) + ') '

        c = self.dbconn.cursor()
        c.executemany('INSERT INTO ' + table + ' VALUES ' + v, tab)
        return True


if __name__ == '__main__':
    with SQLiteDB() as sql:
        print(sql.table_exist('coucou'))
        sql.create_table([('ligne', int), ('autre', float)], 'coucou')
        sql.append_line([1, 2], 'coucou')
        sql.append_lines([[1, 2], [3, 4]], 'coucou')
        print(sql.table_exist('coucou'))
        sql.drop_table('coucou')
