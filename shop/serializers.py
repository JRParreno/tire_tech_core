from rest_framework import serializers

from user_profile.serializers import ProfileSerializer
from .models import (ServiceOffer, Shop, ShopPhotos, ShopCategory, Vehicle,
                     ProductOffer, ShopReview
                     )


class ProductOfferSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductOffer
        fields = ['pk', 'product_name',]


class ServiceOfferSerializer(serializers.ModelSerializer):

    class Meta:
        model = ServiceOffer
        fields = ['pk', 'service_name',]


class VehicleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Vehicle
        fields = ['pk', 'vehicle_name',]


class ShopCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = ShopCategory
        fields = ['pk', 'category_name',]


class ShopServiceSerializer(serializers.ModelSerializer):
    shop_category = ShopCategorySerializer(read_only=True, many=True)
    vehicle_types = VehicleSerializer(read_only=True, many=True)
    products = ProductOfferSerializer(read_only=True, many=True)
    services = ServiceOfferSerializer(read_only=True, many=True)

    class Meta:
        model = Shop
        fields = ['pk', 'shop_name', 'contact_number',
                  'open_time', 'close_time', 'special_offers',
                  'address_name', 'longitude', 'latitude',
                  'vehicle_types', 'shop_category',
                  'service_description', 'walk_in_service_description',
                  'services', 'product_description', 'walk_in_product_description',
                  'products'
                  ]

    def __init__(self, *args, **kwargs):
        # init context and request
        context = kwargs.get('context', {})
        self.request = context.get('request', None)
        self.kwargs = context.get("kwargs", None)

        super(ShopServiceSerializer, self).__init__(*args, **kwargs)

    def to_representation(self, instance):
        data = super(ShopServiceSerializer,
                     self).to_representation(instance)

        if 'request' in self.context and self.request:
            shop = data['pk']
            shop_photos = ShopPhotos.objects.filter(shop__pk=shop)
            shop_object_photos = []
            for shop_photo in shop_photos:
                if shop_photo.image.url:
                    shop_object_photos.append(
                        self.request.build_absolute_uri(shop_photo.image.url))
            data['shop_photos'] = shop_object_photos
        return data


class ShopReviewSerializer(serializers.ModelSerializer):
    user_profile = ProfileSerializer(read_only=True)
    shop_pk = serializers.CharField(write_only=True)

    class Meta:
        model = ShopReview
        fields = ['pk', 'shop', 'user_profile',
                  'description', 'rate', 'shop_pk']

    def __init__(self, *args, **kwargs):
        # init context and request
        context = kwargs.get('context', {})
        self.request = context.get('request', None)
        self.kwargs = context.get("kwargs", None)

        super(ShopReviewSerializer, self).__init__(*args, **kwargs)


class ShopReviewRateSerializer(serializers.Serializer):
    rate = serializers.FloatField(read_only=True)
    user_review = ShopReviewSerializer(read_only=True)
    is_owner = serializers.BooleanField(read_only=True)
    shop_name = serializers.CharField(read_only=True)
