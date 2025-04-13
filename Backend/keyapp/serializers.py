from rest_framework import serializers
from .models import Transcript

class TranscriptSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transcript
        fields = ['id', 'title', 'json_content', 'keywords', 'created_at']
        read_only_fields = ['keywords', 'created_at']