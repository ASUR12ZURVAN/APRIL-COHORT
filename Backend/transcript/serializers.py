from rest_framework import serializers

class TranscriptSerializer(serializers.Serializer):
    raw_text = serializers.CharField(write_only=True)
    conversation = serializers.ListField(
        child=serializers.DictField(), 
        read_only=True
    )
    customer_lines = serializers.ListField(
        child=serializers.CharField(),
        read_only=True
    )
    