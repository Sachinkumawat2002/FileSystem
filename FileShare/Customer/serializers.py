from rest_framework import serializers
from .models import *
from django.contrib.auth.hashers import make_password


class SignupSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        password = make_password(validated_data["password"])
        del validated_data["password"]
        return User.objects.create(password = password,**validated_data)
    uploaded_by = serializers.ReadOnlyField()
    class Meta:
        model = User
        fields = "__all__"

class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields =  ["email","password"]   

class FileUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadFile
        fields = ['file', 'uploaded_at']         

