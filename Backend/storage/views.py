from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import user, call, Ticket, Lead
from .serializers import UserSerializer, CallSerializer, TicketSerializer, LeadSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


from transformers import pipeline


sentiment_pipeline = pipeline("sentiment-analysis",device=-1)
classifier = pipeline(
    "sentiment-analysis",
    model="distilbert-base-uncased-finetuned-sst-2-english",
    revision="714eb0f"
)


# -------- USER --------
@api_view(['POST'])
def create_user(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_all_users(request):
    users = user.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_user(request, pk):
    try:
        usr = user.objects.get(pk=pk)
    except user.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    serializer = UserSerializer(usr)
    return Response(serializer.data)

@api_view(['DELETE'])
def delete_user(request, pk):
    try:
        usr = user.objects.get(pk=pk)
    except user.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    usr.delete()
    return Response({'message': 'User deleted'}, status=status.HTTP_204_NO_CONTENT)


# -------- CALL --------
@api_view(['POST'])
def create_call_with_sentiment(request):
    # Extract all fields except avg_sentiment
    input_data = request.data.copy()

    # Check required fields
    required_fields = ['caller_number', 'call_duration', 'call_instance', 'transcript', 'audio_link']
    missing = [field for field in required_fields if field not in input_data]
    if missing:
        return Response({'error': f'Missing fields: {", ".join(missing)}'}, status=status.HTTP_400_BAD_REQUEST)

    # Analyze sentiment from transcript
    transcript_text = input_data['transcript']
    result = sentiment_pipeline(transcript_text)[0]
    sentiment = f"{result['label']} ({result['score']:.2f})"

    # Add avg_sentiment to data before serialization
    input_data['avg_sentiment'] = sentiment

    serializer = CallSerializer(data=input_data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_all_calls(request):
    calls = call.objects.all()
    serializer = CallSerializer(calls, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_call(request, pk):
    try:
        call_instance = call.objects.get(pk=pk)
    except call.DoesNotExist:
        return Response({'error': 'Call not found'}, status=status.HTTP_404_NOT_FOUND)
    serializer = CallSerializer(call_instance)
    return Response(serializer.data)
@api_view(['GET'])
def get_calls_by_caller_number(request, caller_number):
    calls = call.objects.filter(caller_number=caller_number)
    if not calls.exists():
        return Response({'error': 'No calls found for this caller number'}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = CallSerializer(calls, many=True)
    return Response(serializer.data)

@api_view(['DELETE'])
def delete_call(request, pk):
    try:
        call_instance = call.objects.get(pk=pk)
    except call.DoesNotExist:
        return Response({'error': 'Call not found'}, status=status.HTTP_404_NOT_FOUND)
    call_instance.delete()
    return Response({'message': 'Call deleted'}, status=status.HTTP_204_NO_CONTENT)


# -------- TICKET --------
@api_view(['POST'])
def create_ticket(request):
    serializer = TicketSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_all_tickets(request):
    tickets = Ticket.objects.all()
    serializer = TicketSerializer(tickets, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_ticket(request, pk):
    try:
        ticket_instance = Ticket.objects.get(pk=pk)
    except Ticket.DoesNotExist:
        return Response({'error': 'Ticket not found'}, status=status.HTTP_404_NOT_FOUND)
    serializer = TicketSerializer(ticket_instance)
    return Response(serializer.data)

@api_view(['DELETE'])
def delete_ticket(request, pk):
    try:
        ticket_instance = Ticket.objects.get(pk=pk)
    except Ticket.DoesNotExist:
        return Response({'error': 'Ticket not found'}, status=status.HTTP_404_NOT_FOUND)
    ticket_instance.delete()
    return Response({'message': 'Ticket deleted'}, status=status.HTTP_204_NO_CONTENT)


# -------- LEAD --------
@api_view(['POST'])
def create_lead(request):
    serializer = LeadSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_all_leads(request):
    leads = Lead.objects.all()
    serializer = LeadSerializer(leads, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_lead(request, pk):
    try:
        lead_instance = Lead.objects.get(pk=pk)
    except Lead.DoesNotExist:
        return Response({'error': 'Lead not found'}, status=status.HTTP_404_NOT_FOUND)
    serializer = LeadSerializer(lead_instance)
    return Response(serializer.data)

@api_view(['DELETE'])
def delete_lead(request, pk):
    try:
        lead_instance = Lead.objects.get(pk=pk)
    except Lead.DoesNotExist:
        return Response({'error': 'Lead not found'}, status=status.HTTP_404_NOT_FOUND)
    lead_instance.delete()
    return Response({'message': 'Lead deleted'}, status=status.HTTP_204_NO_CONTENT)
