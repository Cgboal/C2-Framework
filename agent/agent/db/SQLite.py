import sqlite3
from ..settings import BASE_DIR


class Helper(object):

    def __init__(self):
        self.db_path = BASE_DIR + "/agent/db/agent.db"
        print self.db_path
        self.create_tables()
        self.conn = sqlite3.connect(self.db_path)


    def get_config(self, key):
        c = self.conn.cursor()
        query = "SELECT value FROM config where key='%s'" % key

        value = c.execute(query).fetchone()

        c.close()
        if value:
            return list(value)[0]
        else:
            return None
    def set_config(self, k, v):
        c = self.conn.cursor()
        query = "INSERT OR REPLACE INTO config (id, key,  value) values ((SELECT id from config where key = '%s'),'%s', '%s')" % (k, k, v)
        status = c.execute(query)
        self.conn.commit()
        c.close()
        return status

    def create_tables(self):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        create_config_table = """CREATE TABLE IF NOT EXISTS config (id INTEGER PRIMARY KEY, key TEXT UNIQUE, value TEXT)"""
        queries = [create_config_table]
        map(lambda x: c.execute(x), queries)
        c.close()
        conn.close()

    def dump_config(self):
        c = self.conn.cursor()

        for row in c.execute('SELECT * FROM config').fetchall():
            print row

