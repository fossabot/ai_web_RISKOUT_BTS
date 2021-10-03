from django.shortcuts import render
from rest_framework import generics, permissions, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .serializers import AnalyzedDataSerializer
from .mongo import DBHandler

from datetime import datetime, timedelta


class AnalyzedDataView(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = AnalyzedDataSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        category = None
        period = None

        if serializer.is_valid():
            # Check category
            if serializer.data.get("category") not in ["news", "social"]:
                return Response({"category": ["Invalid parameter."]}, status=status.HTTP_400_BAD_REQUEST)
            else:
                category = serializer.data.get("category")
            
            # Check period
            if type(serializer.data.get("period")) != int:
                if not (0 <= serializer.data.get("period") <= (24 * 7)):
                    return Response({"period": ["Invalid parameter."]}, status=status.HTTP_400_BAD_REQUEST)    
                return Response({"period": ["Invalid parameter."]}, status=status.HTTP_400_BAD_REQUEST)
            else:
                period = serializer.data.get("period")

            now = datetime.utcnow() + timedelta(hours=9)
            mongo = DBHandler()
            results = mongo.find_item(
                {
                    "created_at": {'$gte' : (now - timedelta(hours=period))},
                    "category":category
                }, 
                "riskout", 
                "analyzed"
            )

            for i in range(len(results)):
                results[i]['created_at'] = results[i]['created_at'].strftime('%y-%m-%d %H:%M:%S')
            
            return Response(results)

        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
