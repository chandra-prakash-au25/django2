from rest_framework import serializers
from .models import Airport

class AirportSerializer(serializers.Serializer):
    name=serializers.CharField(max_length=100,default='')
    code=serializers.CharField(max_length=100,default='')
    #id=serializers.IntegerField()
    user_id=serializers.IntegerField(default=0000)
    def create(self, validated_data):
        return Airport.objects.create(**validated_data)
