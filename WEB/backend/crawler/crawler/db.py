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
            title TEXT,\
            href TEXT,\
            img TEXT,\
            content TEXT,\
            category TEXT,\
            domain TEXT,\
            subject_ TEXT,\
            id TEXT)"\
            )

    def get_cursor(self):
        return self.dbcursor

    def put_content(self, content):
        self.dbcursor.execute(f"INSERT INTO CrawlContents VALUES(\
            :title,\
            :href,\
            :img_url,\
            :body,\
            :category,\
            :domain,\
            :subject_,\
            :id)",\
                {
                'title':content.title,
                'href': content.url,
                'img_url': content.img_url,
                'body': content.body,
                'category':content.category,
                'domain':content.site_domain,
                'subject_': content.subject,
                'id': content.contents_id
                }
            )
        self.dbfile.commit()

    def select_all(self):
        self.dbcursor.execute("SELECT * FROM CrawlContents")
        for row in self.dbcursor:
            print(row)

    def close(self):
        self.dbcursor.close()

if __name__ == "__main__":
    db = DB()
    db.create_db()