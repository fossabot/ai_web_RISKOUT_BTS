from django.shortcuts import render
from rest_framework import generics, permissions, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .serializers import AnalyzedDataSerializer
from .mongo import DBHandler

from datetime import datetime, timedelta
from collections import defaultdict


class AnalyzedDataView(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = AnalyzedDataSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        category = None
        period = None

        if serializer.is_valid():
            # Check category
            # print(serializer.data)
            
            if serializer.data.get("category") not in ["news", "social"]:
                return Response({"category": ["Invalid parameter."]}, status=status.HTTP_400_BAD_REQUEST)
            else:
                category = serializer.data.get("category")
            
            # Check period
            if type(serializer.data.get("period")) != int or not (0 <= serializer.data.get("period") <= (24 * 7)):
                return Response({"period": ["Invalid parameter."]}, status=status.HTTP_400_BAD_REQUEST)
            else:
                period = serializer.data.get("period")
            
            return Response(self.getAnalyzedData(category, period))
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def getAnalyzedData(self, category, period):
        mongo = DBHandler()
        db_result = None
        response = {
            "contentsLength": 0,
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

        if period == 0:
            db_result = mongo.find_item(
                { }, 
                "riskout", 
                "analyzed"
            )
            
        else:
            now = datetime.utcnow() + timedelta(hours=9)
            
            db_result = mongo.find_item(
                {
                    "created_at": {'$gte' : (now - timedelta(hours=period))},
                    "category":category
                }, 
                "riskout", 
                "analyzed"
            )


        response["contents"] = self.datetimeFormatter([v for _, v in enumerate(db_result)]) if (db_result.count()) else []
        response["contentsLength"] = len(response["contents"])
        response["filterTags"] = self.getFilterTags(response["filterTags"], response["contents"])

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

        return tags
