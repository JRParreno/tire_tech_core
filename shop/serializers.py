from rest_framework import serializers
from .models import ServiceOffer


class ServiceOfferSerializer(serializers.ModelSerializer):

    class Meta:
        model = ServiceOffer
        fields = ['pk', 'service_name',]