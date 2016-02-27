import sqlite3
import configparser


class Database:

    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read('config.ini')
        self.conn = sqlite3.connect(self.config['SQLITE']['Filename'])
        self.c = self.conn.cursor()
        self.table_name = 'stores'
        self.__create_table()

    def __create_table(self):
        self.c.execute('''CREATE TABLE IF NOT EXISTS {0} (
            id integer primary key, county text, town text,
            category text, sub_category text,
            store_name text, phone text, addr text,
            join_date text, leave_date text,
            unit text
        )'''.format(self.table_name))

    def insert(self, values):
        self.bulk_insert([values])

    def bulk_insert(self, values):
        sql = 'INSERT INTO {0} VALUES (?,?,?,?,?,?,?,?,?,?,?)'
        sql = sql.format(self.table_name)
        self.c.executemany(sql, values)
        self.conn.commit()

    def delete(self, id):
        sql = 'DELETE FROM {0} WHERE id IN ({1})'
        if type(id) is tuple or type(id) is list:
            id = ','.join('%d' % (v) for v in id)
        sql = sql.format(self.table_name, id)
        self.c.execute(sql)
        self.conn.commit()

    def ids(self):
        sql = 'SELECT id FROM {0}'
        sql = sql.format(self.table_name)
        self.c.execute(sql)
        return [x[0] for x in self.c.fetchall()]
