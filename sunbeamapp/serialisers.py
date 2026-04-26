# app/serializers.py
from rest_framework import serializers

class EmailSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100, required=False)
    mobile = serializers.CharField(max_length=255)
    message = serializers.CharField()
    email = serializers.EmailField(required=False)
    to = serializers.ListField(
        child=serializers.EmailField(),
         default=["rajkumarmech95@gmail.com"]
    )


class EmailSerializerQuotation(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    email = serializers.EmailField()
    mobile = serializers.CharField(max_length=20)
    address = serializers.CharField(required=False, allow_blank=True)
    requirements = serializers.CharField(required=False, allow_blank=True)
    deliveryDate = serializers.DateField(required=False)