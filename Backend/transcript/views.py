from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .services import analyze_call_transcript
from .serializers import TranscriptSerializer

class TranscriptAPI(APIView):
    def post(self, request):
        serializer = TranscriptSerializer(data=request.data)
        if serializer.is_valid():
            raw_text = serializer.validated_data['raw_text']
            structured = analyze_call_transcript(raw_text)
            
            response_data = {
                'conversation': structured,
                'customer_lines': [
                    turn['text'] for turn in structured 
                    if turn['speaker'] in ('Customer', 'Client')
                ]
            }
            return Response(response_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)