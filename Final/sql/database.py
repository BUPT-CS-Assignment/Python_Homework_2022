import sqlite3

class database:
    conn = None
    cur = None

    def __init__(self, name = 'data/data.db'):
        self.connect(name)

    def connect(self,name):
        self.conn = sqlite3.connect(name)
        self.cur = self.conn.cursor()

    def exec(self,sql):
        res = self.cur.execute(sql)
        self.conn.commit()
        return res

    def select(self,sql):
        self.cur.execute(sql)
        res = self.cur.fetchall()
        self.conn.commit()
        return res

    def commit(self):
        self.conn.commit()
    
    def close(self):
        self.cur.close()
        self.conn.close()




    