import sqlite3
from main import Time as time

class Datebase:
    def __init__(self):
        self.time = time()
    @staticmethod
    def runQuery(sql, receive=False):
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        if receive:
            return cursor.fetchall()
        else:
            cursor.execute(sql)
        connection.commit()

        connection.close()


    def get_and_print_wait_time(self):
        query = f"insert into waterTable values ({self.time.datetime()}, 3, 2, 3)"
        print(str(self.time.datetime()))
        self.runQuery(sql=query)
    def all_in_database(self):
        query = f"SELECT * FROM waterTable"
        print(self.runQuery(query, None, True))

    def insert_into_database(self):
        query = f"INSERT INTO waterTable (wait_time) VALUES (3)"
        self.runQuery(query) 
database = Datebase()
database.get_and_print_wait_time()