import sqlite3
from sqlite3.dbapi2 import OperationalError

import os

class DB:
    def __init__(self):
        path= os.path.dirname(os.path.abspath(__file__))
        self.filename = path + "/database.db"
        self.dbfile = sqlite3.connect(self.filename)
        self.dbcursor = self.dbfile.cursor()
        try:
            self.create_db()
        except OperationalError:
            pass

    def create_db(self):
        self.dbcursor.execute("CREATE TABLE NaverNewsContents(\
            title TEXT,\
            href TEXT,\
            img TEXT,\
            content TEXT)"\
            )

    def get_cursor(self):
        return self.dbcursor

    def put_content(self, content):
        self.dbcursor.execute(f"INSERT INTO NaverNewsContents VALUES(\
            :title,\
            :href,\
            :img_url,\
            :body)",\
                {'title':content.title,\
                'href': content.url,\
                'img_url': content.img_url,\
                'body': content.body\
                }\
            )
        self.dbfile.commit()

        # print(f'INSERT INTO NaverNewsContents VALUES({content.title}, \
        #     {content.url},\
        #     {content.img_url},\
        #     {content.body}')

    def select_all(self):
        self.dbcursor.execute("SELECT * FROM NaverNewsContents")
        for row in self.dbcursor:
            print(row)

    def close(self):
        self.dbcursor.close()

if __name__ == "__main__":
    db = DB()
    db.create_db()