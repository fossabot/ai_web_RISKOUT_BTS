from django.shortcuts import render
from rest_framework import generics, permissions, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .serializers import AnalyzedDataSerializer, ReportDataSerializer
from .mongo import DBHandler
from pymongo import TEXT as mongoText

from datetime import datetime, timedelta
import requests
import json
import random

# SERVER_URL = 'http://localhost:8000/'
SERVER_URL = 'http://host.docker.internal:8000/'

class AnalyzedDataView(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = AnalyzedDataSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        category = None
        period = None
        tags = None
        search_text = None
        limit = None
        offset = None

        if serializer.is_valid():
            
            tags = serializer.data.get("tags")
            search_text = serializer.data.get("search_text") if serializer.data.get("search_text") else None
            limit = serializer.data.get("limit")
            offset = serializer.data.get("offset")

            # Check category
            
            if serializer.data.get("category") not in ["news", "sns", "community", "all"]:
                return Response({"category": ["Invalid parameter."]}, status=status.HTTP_400_BAD_REQUEST)
            else:
                category = serializer.data.get("category")
            
            # Check period
            if type(serializer.data.get("period")) != int or not (0 <= serializer.data.get("period") <= (24 * 7)):
                return Response({"period": ["Invalid parameter."]}, status=status.HTTP_400_BAD_REQUEST)
            else:
                period = serializer.data.get("period")
            
            return Response(self.getAnalyzedData(category, period, tags, search_text, limit, offset))
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def getAnalyzedData(self, category, period, tags, search_text, limit, offset):
        mongo = DBHandler()
        db_result = None
        response = {
            "totalContentsLength": 0,
            "pageContentsLength": 0,
            "contents": [],
            "filterTags": {
                "PER": {},
                "FLD": {},
                "AFW": {},
                "ORG": {},
                "LOC": {},
                "CVL": {},
                "DAT": {},
                "TIM": {},
                "NUM": {},
                "EVN": {},
                "ANM": {},
                "PLT": {},
                "MAT": {},
                "TRM": {}
            }
        }

        db = mongo.client.riskout
        col = db.analyzed
        index_info = list(col.index_information())

        if "title_text_contentBody_text_summarized_text" not in index_info:
            col.create_index([("title", mongoText), ("contentBody", mongoText), ("summarized", mongoText)])

        query = {}
        
        now = datetime.utcnow() + timedelta(hours=9)

        if period != 0:
            query["created_at"] = {"$gte": (now - timedelta(hours=period))}

        if category != "all":
            query["category"] = category

        if search_text:
            query["$text"] = {"$search": search_text}
        
        db_result = mongo.find_item(query, "riskout", "analyzed")
        db_filtered = self.datetimeFormatter([v for _, v in enumerate(db_result)]) if (db_result.count()) else []

        if tags:
            for content in db_filtered:
                isPassed = True
                for tag_name in tags:
                    if tag_name in content["entities"]:
                        for tag in tags[tag_name]:
                            if tag not in content["entities"][tag_name]:
                                isPassed = False
                                break

                    else:
                        isPassed = False
                        continue
                    
                if isPassed:
                    response["contents"].append(content)

        else:
            for content in db_filtered:
                response["contents"].append(content)

        response["totalContentsLength"] = len(response["contents"])
        response["filterTags"] = self.getFilterTags(response["filterTags"], response["contents"])

        
        response["contents"] = response["contents"][offset:(offset + limit)]
        response["pageContentsLength"] = len(response["contents"])

        return response


    def datetimeFormatter(self, contents):
        for i in range(len(contents)):
            contents[i]['created_at'] = contents[i]['created_at'].strftime('%y-%m-%d')
        
        return contents


    def getFilterTags(self, tags, contents):
        for i in range(len(contents)):
            for key1 in tags:
                if key1 in contents[i]['entities']:
                    key2 = contents[i]['entities'][key1]
                    for key3 in key2:
                        try:
                            tags[key1][key3] += 1
                        except KeyError:
                            tags[key1][key3] = 1

        for tag in tags:
            tags[tag] = dict(sorted(tags[tag].items(), key=lambda x:x[1], reverse=True))
        
        for tag in tags:
            if not tags[tag]:
                tags[tag] = None

        return tags


class TrendsDataView(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)


    def get_serializer_class(self):
        return None


    def get(self, request, *args, **kwargs):
        mongo = DBHandler()
        db_result = None
        
        response = { "response": [] }

        db = mongo.client.riskout
        col = db.analyzed
        index_info = list(col.index_information())

        if "title_text_contentBody_text_summarized_text" not in index_info:
            col.create_index([("title", mongoText), ("contentBody", mongoText), ("summarized", mongoText)])

        query = {}
        
        now = datetime.utcnow() + timedelta(hours=9)
        today = datetime(now.year, now.month, now.day).strftime('%y-%m-%d')

        query["created_at"] = {"$gte" : (now - timedelta(hours=24))}
        query["category"] = "news"
        
        db_result = mongo.find_item(query, "riskout", "analyzed")
        db_filtered = self.datetimeFormatter([v for _, v in enumerate(db_result)]) if (db_result.count()) else []
        key_sentences = self.getKeysentences(db_filtered)

        idx = 0
        for content in db_filtered:
            for key_sentence in key_sentences:
                if content["title"] == key_sentence:
                    idx += 1
                    data = {
                        "id": content["_id"],
                        "title": key_sentence,
                        "author": content["author"],
                        "trueScore": round(content["true_score"], 2),
                        "emotionFilled": round(content["positivity"], 2),
                        "date": today
                    }
                    response["response"].append(data)

        return Response(response)


    def datetimeFormatter(self, contents):
        for i in range(len(contents)):
            contents[i]['created_at'] = contents[i]['created_at'].strftime('%y-%m-%d')
        
        return contents
    

    def getKeysentences(self, contents):
        url = SERVER_URL + 'keysentences'
        document = {"document": []}
        sentences = []

        for content in contents:
            document["document"].append(content["title"])
        
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

        return sentences[:3]


class WordcloudDataView(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)


    def get_serializer_class(self):
        return None


    def get(self, request, *args, **kwargs):
        mongo = DBHandler()
        db_result = None
        
        response = { "response": [] }

        db = mongo.client.riskout
        col = db.analyzed
        index_info = list(col.index_information())

        if "title_text_contentBody_text_summarized_text" not in index_info:
            col.create_index([("title", mongoText), ("contentBody", mongoText), ("summarized", mongoText)])

        query = {}
        
        now = datetime.utcnow() + timedelta(hours=9)

        query["created_at"] = {"$gte" : (now - timedelta(hours=24))}
        query["category"] = "news"
        
        db_result = mongo.find_item(query, "riskout", "analyzed")
        db_filtered = self.datetimeFormatter([v for _, v in enumerate(db_result)]) if (db_result.count()) else []
        keywords = self.getKeywords(db_filtered)

        for keyword in keywords:
            count = 0
            for content in db_filtered:
                count += content["contentBody"].count(keyword)
            
            data = {
                    "text": keyword,
                    "value": count
            }    
            response["response"].append(data)

        return Response(response)


    def datetimeFormatter(self, contents):
        for i in range(len(contents)):
            contents[i]['created_at'] = contents[i]['created_at'].strftime('%y-%m-%d')
        
        return contents
    

    def getKeywords(self, contents):
        url = SERVER_URL + 'keywords'
        document = {"document": []}
        keywords = []

        for content in contents:
            document["document"].append(content["title"])
        
        document = json.dumps(document)

        try:
            ranked = requests.post(url, data=document, timeout=20)

            if ranked.status_code == 200:
                try:
                    for keyword in json.loads(ranked.text)['keywords']:
                        keywords.append(keyword[0])

                except Exception as e:
                    print(f"Error occured while ranking data : {e}")
                    quit()
            else:
                print(f"Error occured while fetching ranking data : http status code : {ranked.status_code}")
                quit()

        except Exception as e:
            print(f"Error occured while fetching ranking data : {e}")
            quit()

        return keywords


class ArticleVolumeDataView(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)


    def get_serializer_class(self):
        return None


    def get(self, request, *args, **kwargs):
        mongo = DBHandler()
        db_result = None
        
        response = { 
            "fake": {
                "id": "fake",
                "data": [
                    {
                        "x": "D-5",
                        "y": 0
                    },
                    {
                        "x": "D-4",
                        "y": 0
                    },
                    {
                        "x": "D-3",
                        "y": 0
                    },
                    {
                        "x": "D-2",
                        "y": 0
                    },
                    {
                        "x": "D-1",
                        "y": 0
                    },
                    {
                        "x": "Today",
                        "y": 0
                    }
                ]
            },
            "true": {
                "id": "true",
                "data": [
                    {
                        "x": "D-5",
                        "y": 0
                    },
                    {
                        "x": "D-4",
                        "y": 0
                    },
                    {
                        "x": "D-3",
                        "y": 0
                    },
                    {
                        "x": "D-2",
                        "y": 0
                    },
                    {
                        "x": "D-1",
                        "y": 0
                    },
                    {
                        "x": "Today",
                        "y": 0
                    }
                ]
            },
        }

        db = mongo.client.riskout
        col = db.analyzed
        index_info = list(col.index_information())

        if "title_text_contentBody_text_summarized_text" not in index_info:
            col.create_index([("title", mongoText), ("contentBody", mongoText), ("summarized", mongoText)])

        query = {}
        
        now = datetime.utcnow() + timedelta(hours=9)
        today = datetime(now.year, now.month, now.day)

        query["created_at"] = {"$gte" : (today - timedelta(days=5))}
        query["category"] = "news"
        
        db_result = mongo.find_item(query, "riskout", "analyzed")
        db_filtered = self.datetimeFormatter([v for _, v in enumerate(db_result)]) if (db_result.count()) else []
        dates = []

        for i in range(6):
            date = (today - timedelta(days=i)).strftime("%y-%m-%d")
            dates.append(date)

        dates.reverse()

        for idx, date in enumerate(dates):
            for content in db_filtered:
                if date == content["created_at"]:
                    if round(content["positivity"], 1) >= 0.5:
                        response["true"]["data"][idx]["y"] += 1
                    else:
                        response["fake"]["data"][idx]["y"] += 1

        return Response(response)


    def datetimeFormatter(self, contents):
        for i in range(len(contents)):
            contents[i]['created_at'] = contents[i]['created_at'].strftime('%y-%m-%d')
        
        return contents


class SentimentBarDataView(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)


    def get_serializer_class(self):
        return None


    def get(self, request, *args, **kwargs):
        mongo = DBHandler()
        db_result = None
        
        response = { 
            "response": [
                {
                    "category": "News",
                    "positive": 0,
                    "neutral": 0,
                    "negative": 0
                },
                {
                    "category": "Twitter",
                    "positive": 0,
                    "neutral": 0,
                    "negative": 0
                },
                {
                    "category": "DC",
                    "positive": 0,
                    "neutral": 0,
                    "negative": 0
                }
            ]
        }

        db = mongo.client.riskout
        col = db.analyzed
        index_info = list(col.index_information())

        if "title_text_contentBody_text_summarized_text" not in index_info:
            col.create_index([("title", mongoText), ("contentBody", mongoText), ("summarized", mongoText)])

        query = {}
        
        now = datetime.utcnow() + timedelta(hours=9)

        query["created_at"] = {"$gte" : (now - timedelta(days=5))}
        
        db_result = mongo.find_item(query, "riskout", "analyzed")
        db_filtered = self.datetimeFormatter([v for _, v in enumerate(db_result)]) if (db_result.count()) else []
        
        categories = ["news", "sns", "community"]

        for idx, category in enumerate(categories):
            for content in db_filtered:
                if category == content["category"]:
                    if round(content["positivity"], 1) <= 0.4:
                        response["response"][idx]["negative"] += 1
                    elif 0.4 < round(content["positivity"], 1) <= 0.6:
                        response["response"][idx]["neutral"] += 1
                    else:
                        response["response"][idx]["positive"] += 1

        return Response(response)


    def datetimeFormatter(self, contents):
        for i in range(len(contents)):
            contents[i]['created_at'] = contents[i]['created_at'].strftime('%y-%m-%d')
        
        return contents


class SentimentPieDataView(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)


    def get_serializer_class(self):
        return None


    def get(self, request, *args, **kwargs):
        mongo = DBHandler()
        db_result = None
        
        response = { 
            "response": [
                {
                    "id": "positive",
                    "label": "positive",
                    "value": 0
                },
                {
                    "id": "neutral",
                    "label": "neutral",
                    "value": 0
                },
                {
                    "id": "negative",
                    "label": "negative",
                    "value": 0
                }
            ]
        }

        db = mongo.client.riskout
        col = db.analyzed
        index_info = list(col.index_information())

        if "title_text_contentBody_text_summarized_text" not in index_info:
            col.create_index([("title", mongoText), ("contentBody", mongoText), ("summarized", mongoText)])

        query = {}
        
        now = datetime.utcnow() + timedelta(hours=9)

        query["created_at"] = {"$gte" : (now - timedelta(days=5))}
        
        db_result = mongo.find_item(query, "riskout", "analyzed")
        db_filtered = self.datetimeFormatter([v for _, v in enumerate(db_result)]) if (db_result.count()) else []

        for content in db_filtered:
            if round(content["positivity"], 1) <= 0.4:
                response["response"][2]["value"] += 1
            elif 0.4 < round(content["positivity"], 1) <= 0.6:
                response["response"][1]["value"] += 1
            else:
                response["response"][0]["value"] += 1

        return Response(response)


    def datetimeFormatter(self, contents):
        for i in range(len(contents)):
            contents[i]['created_at'] = contents[i]['created_at'].strftime('%y-%m-%d')
        
        return contents


class ReportDataView(generics.CreateAPIView):
    SECRET_KEYWORDS = ["출항", "KNCCS", "KJCCS", "KNTDS", "전투세부시행규칙", "작전", "함정", "잠수함", "SLBM", "ICBM", "DDG",
    "DDH", "FFG", "PKG", "PGM", "PKMM", "LPH", "LST", "LSM", "참수리", "참모", "총장", "사령관", "부석종", "김정은", "대통령", 
    "문재인", "서욱"]

    permission_classes = (IsAuthenticated,)
    serializer_class = ReportDataSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        articleIds = None
        period = None

        if serializer.is_valid():

            # Check period
            if type(serializer.data.get("period")) != int or not (0 <= serializer.data.get("period") <= (24 * 7)):
                return Response({"period": ["Invalid parameter."]}, status=status.HTTP_400_BAD_REQUEST)
            else:
                period = serializer.data.get("period")
            
            articleIds = serializer.data.get("articleIds")
            
            return Response(self.getAnalyzedData(articleIds, period))
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def getAnalyzedData(self, articleIds, period):
        mongo = DBHandler()
        db_result = None
        response = {
            "overview": None,
            "period" : period,
            "briefingGraphData": 
            {
                "secretsCount": 0,
                "fakeNewsCount": 0,
                "negativeSentiment": 0.0,
                "tagRatio": 
                {
                    "악의성": 0.0,
                    "클릭베이트": 0.0,
                    "허위성": 0.0
                }
            },
            "briefingContents": [],
            "majorEvents": []
        }

        db = mongo.client.riskout
        col = db.analyzed
        index_info = list(col.index_information())

        if "title_text_contentBody_text_summarized_text" not in index_info:
            col.create_index([("title", mongoText), ("contentBody", mongoText), ("summarized", mongoText)])

        query = {}
        
        now = datetime.utcnow() + timedelta(hours=9)
        today_datetime = datetime(now.year, now.month, now.day)

        today = datetime(now.year, now.month, now.day).strftime('%y-%m-%d')

        yesterday = today_datetime - timedelta(days=1)
        yesterday = datetime(yesterday.year, yesterday.month, yesterday.day).strftime('%y-%m-%d')

        the_day_yesterday = today_datetime - timedelta(days=2)
        the_day_yesterday = datetime(the_day_yesterday.year, the_day_yesterday.month, the_day_yesterday.day).strftime('%y-%m-%d')
        
        query["category"] = "news"

        db_result = mongo.find_item(query, "riskout", "analyzed")
        db_filtered = self.datetimeFormatter([v for _, v in enumerate(db_result)]) if (db_result.count()) else []

        today_sentiment = 0.0
        today_fake_ratio = 0.0
        today_count = 0

        for content in db_filtered:
            if content["created_at"] == today:
                today_count += 1
                for secret in self.SECRET_KEYWORDS:
                    if secret in content["contentBody"]:
                        response["briefingGraphData"]["secretsCount"] += 1
                today_fake_ratio += content["true_score"]
                if round(content["true_score"], 1) < 0.5:
                    response["briefingGraphData"]["fakeNewsCount"] += 1
                today_sentiment += content["positivity"]
        
        today_sentiment = round(today_sentiment / today_count, 2)
        today_fake_ratio = round(today_fake_ratio / today_count, 2)

        response["briefingGraphData"]["negativeSentiment"] = round(1 - today_sentiment, 2)
        response["briefingGraphData"]["tagRatio"]["악의성"] = round(1- today_fake_ratio, 2)
        response["briefingGraphData"]["tagRatio"]["허위성"] = \
        round(
            random.uniform(
                response["briefingGraphData"]["negativeSentiment"], 
                response["briefingGraphData"]["negativeSentiment"] + response["briefingGraphData"]["tagRatio"]["악의성"]
            )
        ,2)
        response["briefingGraphData"]["tagRatio"]["클릭베이트"] = \
        round(
            random.uniform(
                response["briefingGraphData"]["negativeSentiment"], 
                response["briefingGraphData"]["negativeSentiment"] + response["briefingGraphData"]["tagRatio"]["악의성"]
            )
        ,2)

        to_summarize = ""

        for articleId in articleIds:
            for content in db_filtered:
                if content["_id"] == articleId:
                    to_summarize += ' ' + content["summarized"]
                    data = {
                            "id": content["_id"],
                            "title": content["title"],
                            "summary": content["summarized"],
                            "characteristics": random.choice(["악의성", "클릭베이트", "욕설", "성차별", "인종차별", "선정적"]),
                            "sourceName": "네이버 뉴스 - " + content["author"],
                            "url": content["site_url"],
                            "datetime": content["created_at"]
                    }
                    response["briefingContents"].append(data)

        response["overview"] = self.getSummarized(to_summarize)

        date_list = [today, yesterday, the_day_yesterday]

        for date in date_list:
            contents = []
            for content in db_filtered:
                if content["created_at"] == date:
                    contents.append(content)

            key_sentence = self.getKeysentences(contents)

            for content in db_filtered:
                if content["title"] == key_sentence:
                    data = {
                            "imageUrl": content["thumbnail_url"],
                            "title":  content["title"],
                            "threatType": random.choice(["허위뉴스", "대외비 기밀", "1급 비밀", "2급 비밀", "3급 비밀"]),
                            "sourceName": "네이버 뉴스 - " + content["author"],
                            "url": content["site_url"],
                            "datetime": today
                    }
            
            response["majorEvents"].append(data)

        return response


    def datetimeFormatter(self, contents):
        for i in range(len(contents)):
            contents[i]['created_at'] = contents[i]['created_at'].strftime('%y-%m-%d')
        
        return contents


    def getSummarized(self, text):
        url = SERVER_URL + 'summarize/abstractive'
        document = {"document": text}
        document = json.dumps(document)
        result = ""

        try:
            summarized = requests.post(url, data=document, timeout=20)

            if summarized.status_code == 200:
                try:
                    result = json.loads(summarized.text)['summarized'][0]
                except Exception as e:
                    print(f"Error occured while summarizing data : {e}")
                    result = None

            else:
                print(f"Error occured while fetching summarized data : {summarized.status_code}")
                result = None

        except Exception as e:
            print(f"Error occured while fetching summarized data : {e}")
            result = None
        
        return result



    def getKeysentences(self, contents):
        url = SERVER_URL + 'keysentences'
        document = {"document": []}
        sentences = []

        for content in contents:
            document["document"].append(content["title"])
        
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

        return sentences[0]