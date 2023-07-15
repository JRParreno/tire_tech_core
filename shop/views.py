from rest_framework import generics, permissions, response, status
from .serializers import ServiceOfferSerializer, ShopServiceSerializer
from .models import ServiceOffer, Shop
from .paginate import ExtraSmallResultsSetPagination


class ServicesOfferListView(generics.ListAPIView):
    serializer_class = ServiceOfferSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = ServiceOffer.objects.all().order_by('service_name')


class FindShopServiceListView(generics.ListAPIView):
    serializer_class = ShopServiceSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Shop.objects.all().order_by('shop_name')
