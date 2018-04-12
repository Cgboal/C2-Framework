import sqlite3
from ..settings import BASE_DIR


class Helper(object):

    class Module:
        def __init__(self, uuid, name, image):
            self.uuid = uuid
            self.name = name
            self.image = image

    def __init__(self):
        self.db_path = BASE_DIR + "/agent/db/agent.db"
        self.create_tables()
        self.conn = sqlite3.connect(self.db_path)

    def create_tables(self):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        create_config_table = "CREATE TABLE IF NOT EXISTS config (id INTEGER PRIMARY KEY, key TEXT UNIQUE, value TEXT)"
        create_modules_table = "CREATE TABLE IF NOT EXISTS modules (id INTEGER PRIMARY KEY, uuid TEXT UNIQUE, name TEXT, image TEXT UNIQUE)"
        queries = [create_config_table, create_modules_table]
        map(lambda x: c.execute(x), queries)
        c.close()
        conn.close()

    def get_module(self, uuid):
        c = self.conn.cursor()
        query = "SELECT * FROM modules where uuid='%s'" % uuid

        value = c.execute(query).fetchone()

        c.close()
        if value:
            module = self.Module(value[1], value[2], value[3])
            return module
        else:
            return None

    def create_module(self, uuid, name, image):
        c = self.conn.cursor()
        query = "INSERT INTO modules (uuid, name, image) values ('%s', '%s', '%s')" % (uuid, name, image)
        status = c.execute(query)
        self.conn.commit()
        c.close()
        return status

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

    def dump_config(self):
        c = self.conn.cursor()

        for row in c.execute("SELECT * FROM config").fetchall():
            print row

