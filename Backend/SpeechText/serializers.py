from rest_framework import serializers
from .models import call

class CallSerializer(serializers.ModelSerializer):
    class Meta:
        model = call
        fields = '__all__'