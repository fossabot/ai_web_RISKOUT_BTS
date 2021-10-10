from django.urls import path
from .views import *

urlpatterns = [
    path('analyze/', AnalyzedDataView.as_view(), name='analyze'),
    path('trends/', TrendsDataView.as_view(), name='trends'),
    path('wordcloud/', AnalyzedDataView.as_view(), name='wordcloud'),
    path('article/volume/', AnalyzedDataView.as_view(), name='true_counter'),
    path('sentiment/bar/', AnalyzedDataView.as_view(), name='sentiment_bar'),
    path('sentiment/pie/', AnalyzedDataView.as_view(), name='sentiment_pie'),

]
