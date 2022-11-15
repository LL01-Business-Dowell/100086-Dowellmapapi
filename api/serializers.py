from rest_framework import serializers
from .models import PlacesRequest, PlacesResponse


class CreatePlacesRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlacesRequest
        fields = '__all__'

    def create(self, validated_data):
        place_request = PlacesRequest.objects.create(**validated_data)

        place_request.save()
        return place_request



class CreatePlacesResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlacesResponse
        fields = '__all__'

    def create(self, validated_data):
        place_response = PlacesResponse.objects.create(**validated_data)

        place_response.save()
        return place_response

