# import pymysql

class MariaDB:
    def __init__(self) -> None:
        # self.conn = pymysql.connect()
        pass

    def select(self, sql):
        with self.conn.cursor() as cur:
            cur.execute(sql)
        return
