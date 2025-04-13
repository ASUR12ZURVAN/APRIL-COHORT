from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Transcript
from .serializers import TranscriptSerializer
from .services import extract_keywords

class TranscriptAPIView(APIView):
    def get(self, request):
        transcripts = Transcript.objects.all()
        serializer = TranscriptSerializer(transcripts, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = TranscriptSerializer(data=request.data)
        if serializer.is_valid():
            transcript = serializer.save()
            transcript.keywords = extract_keywords(transcript.json_content)
            transcript.save()
            return Response(TranscriptSerializer(transcript).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TranscriptDetailAPIView(APIView):
    def get(self, request, pk):
        transcript = Transcript.objects.get(pk=pk)
        serializer = TranscriptSerializer(transcript)
        return Response(serializer.data)

# Create your views here.
