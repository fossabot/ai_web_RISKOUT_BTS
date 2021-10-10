from django.shortcuts import render
from rest_framework import generics, permissions, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .serializers import AnalyzedDataSerializer
from .mongo import DBHandler
from pymongo import TEXT as mongoText

from datetime import datetime, timedelta
import requests
import json

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
                        "id": idx,
                        "title": key_sentence,
                        "author": content["author"],
                        "trueScore": round(content["true_score"], 2),
                        "emotionFilled": round(content["positivity"], 2),
                        "date": content["created_at"]
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

