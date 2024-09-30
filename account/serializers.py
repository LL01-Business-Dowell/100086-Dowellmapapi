from rest_framework import serializers

class UserSerializer(serializers.Serializer):
    workspace_id = serializers.CharField()
    portfolio = serializers.CharField()
    password = serializers.CharField()

class UserAuthSerializer(serializers.Serializer):
    workspace_name = serializers.CharField()
    portfolio = serializers.CharField()
    password = serializers.CharField()

class UserUpdateSerializer(serializers.Serializer):
    email = serializers.CharField(required=False, allow_blank=True)
    profile_image = serializers.CharField(required=False, allow_blank=True)
