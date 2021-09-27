import os
import unicodedata
import sqlite3
import requests
import json

SERVER_URL = 'https://osamhack2021-ai-web-riskout-bts-jjqv7j5vgfj7pw-8000.githubpreview.dev/'

current_abs_path= os.path.dirname(os.path.abspath(__file__))
db_path = current_abs_path + "/database.db"
conn = sqlite3.connect(db_path)


class Content:
    """
    * Cloned from crawler.model -> Content.py

    기존 RAW 데이터에 Analyzed된 데이터까지 포함함
    """
    def __init__(self, extracted):
        self.content_dict = extracted
        """
        id: (mongoDB에 insert 되기 직전에 생성됨)
        created_at: (mongoDB에 insert 되기 직전에 생성됨)

        site_url, thumbnail_url, category, title, contentBody: extracted 에서 추출

        summarized, positivity, entities: analyze 호출 이후 할당
        """
        
        self.getSummarized()
        self.getPositivity()
        self.getEntities()
        self.content_dict['isAnalyzed'] = True
    

    def getSummarized(self):
        url = SERVER_URL + 'summarize'
        document = {"document": self.content_dict['contentBody']}
        document = json.dumps(document)
        summarized = requests.post(url, data=document)

        if summarized.status_code == 200:
            self.content_dict['summarized'] = json.loads(summarized.text)['summarized']
        else:    
            self.content_dict['summarized'] = None


    def getPositivity(self):
        url = SERVER_URL + 'sentiment'
        document = {"document": self.content_dict['contentBody']}
        document = json.dumps(document)
        positivity = requests.post(url, data=document)

        if positivity.status_code == 200:
            self.content_dict['positivity'] = json.loads(positivity.text)['score']
        else:    
            self.content_dict['positivity'] = None


    def getEntities(self):
        url = SERVER_URL + 'ner'
        document = {"document": self.content_dict['contentBody']}
        document = json.dumps(document)
        entities = requests.post(url, data=document)

        if entities.status_code == 200:
            self.content_dict['entities'] = json.loads(entities.text)['ner']
        else:    
            self.content_dict['entities'] = None


def extractor(data):
    contents = []

    # for tup in data:
    tup = data
    extracted = {}
    extracted['title'] = tup[0]
    extracted['site_url'] = tup[1]
    extracted['thumbnail_url'] = tup[2]
    extracted['contentBody'] = unicodedata.normalize('NFKC', tup[3]) # 공백 문자가 \xa0 로 인식되는 문제 해결
    extracted['category'] = tup[4]

    content = Content(extracted)
    contents.append(content)

    return contents


def main():
    cur = conn.cursor()
    cur.execute("SELECT * FROM CrawlContents")
    raw_data = cur.fetchall()
    contents = extractor(raw_data[0])
    # contents = extractor(raw_data)
    print(contents[0].content_dict)


if __name__ == '__main__':
    main()
