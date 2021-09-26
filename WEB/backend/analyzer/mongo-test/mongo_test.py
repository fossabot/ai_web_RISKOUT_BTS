import json
from datetime import datetime
from pymongo import MongoClient
from pymongo.collection import ReturnDocument
from pymongo.cursor import CursorType


class DBHandler:
    def __init__(self):
        host = "localhost"
        port = "27017"
        self.client = MongoClient(host, int(port))

    def insert_item_one(self, data, db_name=None, collection_name=None):
        result = self.client[db_name][collection_name].insert_one(data).inserted_id
        return result

    def insert_item_many(self, datas, db_name=None, collection_name=None):
        result = self.client[db_name][collection_name].insert_many(datas).inserted_ids
        return result

    def find_item_one(self, condition=None, db_name=None, collection_name=None):
        result = self.client[db_name][collection_name].find_one(condition)
        #result = self.client[db_name][collection_name].find_one(condition, {"_id": False})
        return result

    def find_item(self, condition=None, db_name=None, collection_name=None):
        result = self.client[db_name][collection_name].find(condition, {"_id": False}, no_cursor_timeout=True, cursor_type=CursorType.EXHAUST)
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

def main():
    mongo = DBHandler()
    data = """
    {
        "site_url": "http://news.kmib.co.kr/article/view.asp?arcid=0016296291",
        "thumbnail_url": "http://image.kmib.co.kr/online_image/2021/0923/2021092317230249209_1632385382_0016296291.jpg",
        "category": "news",
        "title": "‘오징어 게임’서 노출된 내 번호 “밤낮으로 괴로워…”",
        "contentBody": "전 세계에서 넷플릭스 순위 1위를 휩쓸고 있는 한국 오리지널 시리즈 ‘오징어 게임’에 개인이 사용 중인 휴대폰 번호가 그대로 노출돼 피해자가 고통을 호소하고 있다.\\n피해자 A씨는 23일 머니투데이와의 인터뷰에서 ‘오징어 게임’ 방영 이후 일상생활이 어려울 정도로 24시간 문자와 전화가 쉴 새 없이 오고 있다고 밝혔다.\\n영문을 몰랐던 A씨는 지인들을 통해 본인의 번호가 드라마에 유출된 사실을 알게 됐다고 전했다.\\n이어 A씨는 “10년도 더 된 번호가 이리 되자 황당하다”며 “최근까지 삭제한 전화번호만 4000개가 넘는다.\\n밤낮으로 시간 개념도 없이 호기심에 오는 연락에 휴대폰 배터리가 반나절이면 방전되어 버릴 정도”라며 괴로움을 토로했다.",
        "summarized": "전 세계에서 넷플릭스 순위 1위를 휩쓸고 있는 한국 오리지널 시리즈 시리즈 '오징어 게임'에 개인이 사용 중인 휴대폰 번호가 그대로 노출돼 피해자가 고통을 호소하고 있으며 피해자 A씨는 23일 머니투데이와의 인터뷰에서 '오징어 게임' 방영 이후 일상생활이 어려울 정도로 24시간 문자와 전화가 쉴 새 없이 오고 있다고 밝혔다.",
        "positivity": 0.3113776445388794,
        "entities":
          {
            "ORG": [
              "넷플릭스"
            ],
            "CVL": [
              "피해자",
              "오징어",
              "지인"
            ],
            "TIM": [
              "밤낮"
            ]
          }
    }
    """
    data = json.loads(data)
    data['_id'] = mongo.get_next_sequence('analyzed_counter', 'riskout', 'counter')
    data['created_at'] = datetime.utcnow().strftime('%y-%m-%d %H:%M:%S')
    print(mongo.insert_item_one(data, "riskout", "analyzed"))

    #result = mongo.find_item_one({"_id": 1}, "riskout", "analyzed")
    #print(result)
    #print(json.dumps(mongo.find_item_one({"category": "news"}, "riskout", "analyzed")))



if __name__ == '__main__':
    main()
