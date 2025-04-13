from django.urls import path
from .views import TranscriptAPI

urlpatterns = [
    path('analyze/', TranscriptAPI.as_view(), name='transcript-analyze'),
]