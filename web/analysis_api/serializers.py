from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Analysis

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'first_name', 'last_name')

    def create(self, validated_data):
        user = super().create({
            'username': validated_data['username'],
            'email': validated_data['email'],
        })

        user.set_password(validated_data['password'])
        user.save()
        return user


class UserSerializerSimple(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username')

class AnalysisSerializer(serializers.ModelSerializer):
    class Meta:
        model = Analysis
        fields = ('id', 'analysis', 'date_uploaded', 'date_modified')
    
    def create(self, validated_data):
        return Analysis(**validated_data)

    # def update(self, instance, validated_data):
    #     print(instance)
    #     # instance.user_id = validated_data.get('user_id', instance.user_id)
    #     instance.analysis = validated_data.get('analysis', instance.analysis)
    #     instance.save()
    #     return instance
