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


# SERVER_URL = 'http://localhost:8000/'
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

        try:
            summarized = requests.post(url, data=document, timeout=20)

            if summarized.status_code == 200:
                try:
                    self.content_dict['summarized'] = json.loads(summarized.text)['summarized'][0]
                except Exception as e:
                    print(f"Error occured while summarizing data : {e}")
                    self.content_dict['summarized'] = None

            else:
                print(f"Error occured while fetching summarized data : {e}")
                self.content_dict['summarized'] = None

        except Exception as e:
            print(f"Error occured while fetching summarized data : {e}")
            self.content_dict['summarized'] = None


    def getPositivity(self):
        url = SERVER_URL + 'sentiment'
        document = {"document": self.content_dict['contentBody']}
        document = json.dumps(document)
        try:
            positivity = requests.post(url, data=document, timeout=20)

            if positivity.status_code == 200:
                try:
                    self.content_dict['positivity'] = json.loads(positivity.text)['score'][0]
                except Exception as e:
                    print(f"Error occured while getting positivity : {e}")
                    self.content_dict['positivity'] = None
            else:
                print(f"Error occured while fetching positivity data : {e}")
                self.content_dict['positivity'] = None

        except Exception as e:
            print(f"Error occured while fetching positivity data : {e}")
            self.content_dict['positivity'] = None



    def getEntities(self):
        url = SERVER_URL + 'ner'
        document = {"document": self.content_dict['contentBody']}
        document = json.dumps(document)
        try:
            entities = requests.post(url, data=document, timeout=20)

            if entities.status_code == 200:
                try:
                    self.content_dict['entities'] = json.loads(entities.text)['ner'][0]
                except Exception as e:
                    print(f"Error occured while getting entities : {e}")
                    self.content_dict['entities'] = None
            else:
                print(f"Error occured while fetching entities : {e}")
                self.content_dict['entities'] = None

        except Exception as e:
            print(f"Error occured while fetching entities : {e}")
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


def process_data(res_data):
    try:
        res_data["summarized"] = json.loads(res_data["res_text"])["summarized"][0]

    except Exception as e:
        print(f"Error occured while summarizing data : {e}")
    
    return res_data


async def post_data(url, session, id, document):
    result = {"id": id, "res_text": None, "summarized": None}

    try:
        async with session.post(url, json=document, timeout = 7200) as res:
            result["res_text"] = await res.text()

    except Exception as e:
        print(f"Error occured while fetching summarized data : {e}")
    
    return result


async def process(url, session, pool, id, document):
    data = await post_data(url, session, id, document)
    print(data)
    return await asyncio.wrap_future(pool.submit(process_data, data))


async def dispatch(req_list):
    pool = ProcessPoolExecutor()
    async with aiohttp.ClientSession() as session:
        coros = (process(url=req["url"], session=session, pool=pool, id=req["id"], document=req["document"]) for req in req_list)
        return await asyncio.gather(*coros)


def dataRanker(data):
    print('[*] Data ranker Started!')

    if not len(data):
        return data

    url = SERVER_URL + 'keysentences'
    document = {"document": []}
    ranked_data = []
    sentences = []

    for tup in data:
        document["document"].append(tup[0])
    
    document = json.dumps(document)

    try:
        ranked = requests.post(url, data=document, timeout=20)

        if ranked.status_code == 200:
            try:
                for sentence in json.loads(ranked.text)['keysentences']:
                    sentences.append(sentence["sentence"])

            except Exception as e:
                print(f"Error occured while ranking data : {e}")
                quit()
        else:
            print(f"Error occured while fetching ranking data : http status code : {ranked.status_code}")
            quit()

    except Exception as e:
        print(f"Error occured while fetching ranking data : {e}")
        quit()


    for sentence in sentences:
        for tup in data:
            if tup[0] == sentence:
                ranked_data.append(tup)

    return ranked_data


def extractor(data):
    print('[*] Extractor Started!\n')

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
    validated_contents= []
    mongo = DBHandler()

    for i in range(len(contents)):
        hasNone = False

        for key in contents[i]:
            if contents[i][key] is None:
                hasNone = True
                break

        if not hasNone:
            contents[i]['_id'] = mongo.get_next_sequence('analyzed_counter', 'riskout', 'counter')
            contents[i]['created_at'] = (datetime.utcnow() + timedelta(hours=9))
            validated_contents.append(contents[i])

    try:
        mongo.insert_item_many(validated_contents, "riskout", "analyzed")
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

    date_list = []
    important_data_list = []
    
    for tup in raw_data:
        if tup[9] not in date_list:
            date_list.append(tup[9])
    
    today = (datetime.utcnow() + timedelta(hours=9)).strftime('%y_%m_%d')

    for date in date_list:
        cur.execute("SELECT * FROM CrawlContents WHERE isAnalyzed = 0 AND created_at = ?", (date,))
        if date != today:
            important_data_list.extend(dataRanker(cur.fetchall()))
            cur.execute("UPDATE CrawlContents SET isAnalyzed = 1 WHERE isAnalyzed = 0 AND created_at = ?", (date,))
            conn.commit()
        else:
            important_data_list.extend(dataRanker(cur.fetchall()))

    print(f"[*] Serving {len(important_data_list)} pages to Extractor...")

    contents = extractor(important_data_list)
    dbInserter(contents)

    cur.close()
    conn.close()

    end_time = time()
    elasped_time = round((end_time - start_time), 3)
    print(f"\n\nelasped_time : {elasped_time}\n\n")


if __name__ == '__main__':
    main()