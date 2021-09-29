import sqlite3

import os

class DB:
    def __init__(self):
        path= os.path.dirname(os.path.abspath(__file__))
        self.filename = path + "/database.db"
        self.dbfile = sqlite3.connect(self.filename)
        self.dbcursor = self.dbfile.cursor()

        self.create_db()

    def create_db(self):
        try:
            self.dbcursor.execute("SELECT * FROM CrawlContents")
        except Exception:
            self.dbcursor.execute("CREATE TABLE CrawlContents(\
                title TEXT,\
                href TEXT,\
                img TEXT,\
                content TEXT,\
                category TEXT,\
                domain TEXT,\
                subject_ TEXT,\
                id TEXT,\
                isAnalyzed INTEGER)"\
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
            :id,\
            :isAnalyzed)",\
                {
                'title':content.title,
                'href': content.url,
                'img_url': content.img_url,
                'body': content.body,
                'category':content.category,
                'domain':content.site_domain,
                'subject_': content.subject,
                'id': content.contents_id,
                'isAnalyzed': 0
                }
            )
        self.dbfile.commit()

    def select_all(self):
        self.dbcursor.execute("SELECT * FROM CrawlContents")
        for row in self.dbcursor:
            print(row)

    def select_id(self):
        self.dbcursor.execute("SELECT id FROM CrawlContents")
        raw_id_data = self.dbcursor.fetchall()
        id_list = []

        for id_ in raw_id_data:
            id_list.append(id_[0])

        return id_list

    def select_isAnalyzed(self):
        self.dbcursor.execute("SELECT isAnalyzed FROM CrawlContents")
        raw_isanalyzed_data = self.dbcursor.fetchall()
        isanalyzed_list = []

        for isAnalyzed in raw_isanalyzed_data:
            isanalyzed_list.append(isAnalyzed)
        
        return isanalyzed_list

    def un_analyzed_amount(self):
        self.dbcursor.execute("SELECT isAnalyzed FROM CrawlContents")
        data = self.dbcursor.fetchall()
        return len(data)

    def close(self):
        self.dbcursor.close()

if __name__ == "__main__":
    db = DB()
    print(db.un_analyzed_amount())
