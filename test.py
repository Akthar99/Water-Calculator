import sqlite3

class Datebase:
    def __init__(self):
        pass
    @staticmethod
    def runQuery(sql, data=None, receive=False):
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        if data:
            cursor.execute(sql, data)
        else:
            cursor.execute(sql)
        
        if receive:
            return cursor.fetchall()
        else:
            connection.commit()
        
        connection.close()

    def get_and_print_wait_time(self):
        query = f"SELECT wait_time FROM waterTable"
        self.remain_wait_time = self.runQuery(query, None, True)
        print(self.remain_wait_time)
    def all_in_database(self):
        query = f"SELECT * FROM waterTable"
        print(self.runQuery(query, None, True))

    def insert_into_database(self):
        query = f"INSERT INTO waterTable (wait_time) VALUES (3)"
        self.runQuery(query) 
database = Datebase()
database.all_in_database()