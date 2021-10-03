from django.urls import path
from .views import AnalyzedDataView

urlpatterns = [
    path('api/analyzed/', AnalyzedDataView.as_view(), name='register'),
]
