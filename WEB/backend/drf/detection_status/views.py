from django.shortcuts import render
from rest_framework import generics, permissions, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .serializers import AnalyzedDataSerializer
from .mongo import DBHandler
from pymongo import TEXT as mongoText

from datetime import datetime, timedelta
from collections import defaultdict


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
            
            if serializer.data.get("category") not in ["news", "social"]:
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
            query["created_at"] = {"$gte" : (now - timedelta(hours=period))}

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
            contents[i]['created_at'] = contents[i]['created_at'].strftime('%y-%m-%d %H:%M:%S')
        
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
