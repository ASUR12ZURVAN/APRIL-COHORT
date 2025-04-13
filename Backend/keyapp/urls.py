from django.urls import path
from .views import TranscriptAPIView, TranscriptDetailAPIView

urlpatterns = [
    path('transcripts/', TranscriptAPIView.as_view(), name='transcript-list'),
    path('transcripts/<int:pk>/', TranscriptDetailAPIView.as_view(), name='transcript-detail'),
]