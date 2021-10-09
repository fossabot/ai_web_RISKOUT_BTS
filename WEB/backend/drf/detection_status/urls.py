from django.urls import path
from .views import AnalyzedDataView

urlpatterns = [
    path('analyze/', AnalyzedDataView.as_view(), name='analyze'),
]
