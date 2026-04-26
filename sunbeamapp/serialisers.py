# app/serializers.py
from rest_framework import serializers

class EmailSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100, required=False, allow_blank=True)
    mobile = serializers.CharField(max_length=20)
    message = serializers.CharField()
    email = serializers.EmailField(required=False, allow_blank=True)
    subject = serializers.CharField(required=False, allow_blank=True)

    to = serializers.ListField(
        child=serializers.EmailField(),
        required=False,
        default=["deadryefield@gmail.com"]
    )
class EmailSerializerQuotation(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    email = serializers.EmailField()
    phone = serializers.CharField(max_length=20)

    project = serializers.CharField(required=False, allow_blank=True)
    quantity = serializers.CharField(required=False, allow_blank=True)
    size = serializers.CharField(required=False, allow_blank=True)

    details = serializers.CharField(required=False, allow_blank=True)
    deadline = serializers.DateField(required=False,
                                     allow_null=True,
    default=None)

    def validate_deadline(self, value):
        if value == "":
            return None
        return value