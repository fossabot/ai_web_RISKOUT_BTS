import sqlite3
from sqlite3.dbapi2 import OperationalError

import os

class DB:
    def __init__(self):
        path= os.path.dirname(os.path.abspath(__file__))
        self.dbfile = sqlite3.connect(path + "/database.db")
        self.dbcursor = self.dbfile.cursor()
        try:
            self.create_db()
        except OperationalError:
            pass

    def create_db(self):
        self.dbcursor.execute("CREATE TABLE NaverNewsContents(id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, href TEXT, img TEXT, content TEXT)")

    def get_cursor(self):
        return self.dbcursor

    def put_content(self, content):
        self.dbcursor.execute(f'INSERT INTO NaverNewsContent VALUES({content.title}, {content.url}, {content.img_url}, {content.body})')
        self.dbcursor.commit()