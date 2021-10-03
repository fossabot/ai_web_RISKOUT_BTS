import os
import unicodedata
import sqlite3
import requests
import json
from time import time
from datetime import datetime, timedelta
from pymongo import MongoClient
from pymongo.collection import ReturnDocument
from pymongo.cursor import CursorType


SERVER_URL = 'http://host.docker.internal:8000/'

current_abs_path= os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(os.path.dirname(current_abs_path), "crawler", "crawler", "database.db")
conn = sqlite3.connect(db_path)
cur = conn.cursor()


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
            try:
                self.content_dict['summarized'] = json.loads(summarized.text)['summarized'][0]
            except Exception as e:
                print(f"Error occured while summarizing data : {e}")
                self.content_dict['summarized'] = None

        else:    
            self.content_dict['summarized'] = None


    def getPositivity(self):
        url = SERVER_URL + 'sentiment'
        document = {"document": self.content_dict['contentBody']}
        document = json.dumps(document)
        positivity = requests.post(url, data=document)

        if positivity.status_code == 200:
            try:
                self.content_dict['positivity'] = json.loads(positivity.text)['score'][0]
            except Exception as e:
                print(f"Error occured while getting positivity : {e}")
                self.content_dict['positivity'] = None
        else:    
            self.content_dict['positivity'] = None


    def getEntities(self):
        url = SERVER_URL + 'ner'
        document = {"document": self.content_dict['contentBody']}
        document = json.dumps(document)
        entities = requests.post(url, data=document)

        if entities.status_code == 200:
            try:
                self.content_dict['entities'] = json.loads(entities.text)['ner']
            except Exception as e:
                print(f"Error occured while getting entities : {e}")
                self.content_dict['entities'] = None
        else:    
            self.content_dict['entities'] = None


class DBHandler:
    def __init__(self):
        host = "host.docker.internal"
        port = "8001"
        self.client = MongoClient(host, int(port))

    def insert_item_one(self, data, db_name=None, collection_name=None):
        result = self.client[db_name][collection_name].insert_one(data).inserted_id
        return result

    def insert_item_many(self, datas, db_name=None, collection_name=None):
        result = self.client[db_name][collection_name].insert_many(datas).inserted_ids
        return result

    def find_item_one(self, condition=None, db_name=None, collection_name=None):
        result = self.client[db_name][collection_name].find_one(condition)
        return result

    def find_item(self, condition=None, db_name=None, collection_name=None):
        result = self.client[db_name][collection_name].find(condition, no_cursor_timeout=True, cursor_type=CursorType.EXHAUST)
        return result

    def delete_item_one(self, condition=None, db_name=None, collection_name=None):
        result = self.client[db_name][collection_name].delete_one(condition)
        return result

    def delete_item_many(self, condition=None, db_name=None, collection_name=None):
        result = self.client[db_name][collection_name].delete_many(condition)
        return result

    def update_item_one(self, condition=None, update_value=None, db_name=None, collection_name=None):
        result = self.client[db_name][collection_name].update_one(filter=condition, update=update_value)
        return result

    def update_item_many(self, condition=None, update_value=None, db_name=None, collection_name=None):
        result = self.client[db_name][collection_name].update_many(filter=condition, update=update_value)
        return result

    def text_search(self, text=None, db_name=None, collection_name=None):
        result = self.client[db_name][collection_name].find({"$text": {"$search": text}})
        return result

    def get_next_sequence(self, counter_name=None, db_name=None, collection_name=None):
        result = self.client[db_name][collection_name].find_one_and_update({'_id': counter_name}, {'$inc': {'seq': 1}}, return_document=ReturnDocument.AFTER)
        result = int(result['seq'])
        return result


def extractor(data):
    print('\n[*] Extractor Started!\n')

    if len(data) < 1:
        print("[!] All pages have been analyzed.")
        cur.close()
        conn.close()
        quit()


    contents = []

    for idx, tup in enumerate(data):
        extracted = {}
        extracted['title'] = tup[0]
        extracted['site_url'] = tup[1]
        extracted['thumbnail_url'] = tup[2]
        extracted['contentBody'] = unicodedata.normalize('NFKC', tup[3]) # 공백 문자가 \xa0 로 인식되는 문제 해결
        extracted['category'] = tup[4]

        content = Content(extracted)
        contents.append(content.content_dict)
        
        cur.execute("UPDATE CrawlContents SET isAnalyzed = 1 WHERE id = ?", (tup[7], ))
        conn.commit()

        print(f"[+] Extractor: {idx + 1}/{len(data)}")

    return contents


def dbInserter(contents):
    mongo = DBHandler()
    for i in range(len(contents)):
        contents[i]['_id'] = mongo.get_next_sequence('analyzed_counter', 'riskout', 'counter')
        contents[i]['created_at'] = (datetime.utcnow() + timedelta(hours=9)).strftime('%y-%m-%d %H:%M:%S')
    
    try:
        mongo.insert_item_many(contents, "riskout", "analyzed")
        print('DB insertion success')
        mongo.client.close()
        return True

    except Exception as e:
        print("DB insert error occured :", e)
        mongo.client.close()
        return False


def main():
    start_time = time()

    cur.execute("SELECT * FROM CrawlContents WHERE isAnalyzed = 0")
    raw_data = cur.fetchall()
    contents = extractor(raw_data)
    dbInserter(contents)

    cur.close()
    conn.close()

    end_time = time()
    elasped_time = round((end_time - start_time), 3)
    print(f"\n\nelasped_time : {elasped_time}\n\n")


if __name__ == '__main__':
    main()
