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
        self.dbcursor.execute("CREATE TABLE CrawlContents(\
            domain TEXT,\
            subject_ TEXT,\
            id TEXT,\
            title TEXT,\
            href TEXT,\
            img TEXT,\
            content TEXT)"\
            )

    def get_cursor(self):
        return self.dbcursor

    def put_content(self, content):
        self.dbcursor.execute(f"INSERT INTO CrawlContents VALUES(\
            :domain,\
            :subject_, \
            :id, \
            :title,\
            :href,\
            :img_url,\
            :body)",\
                {
                'domain':content.site_domain,\
                'subject_': content.subject,\
                'id': content.contents_id,\
                'title':content.title,\
                'href': content.url,\
                'img_url': content.img_url,\
                'body': content.body\
                }\
            )
        self.dbfile.commit()

    def select_all(self):
        self.dbcursor.execute("SELECT * FROM NaverNewsContents")
        for row in self.dbcursor:
            print(row)

    def close(self):
        self.dbcursor.close()

if __name__ == "__main__":
    db = DB()
    db.create_db()