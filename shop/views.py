from rest_framework import generics, permissions, response, status
from .serializers import ServiceOfferSerializer, ShopServiceSerializer
from .models import ServiceOffer, Shop
from .paginate import ExtraSmallResultsSetPagination
from django.db.models import Q


class ServicesOfferListView(generics.ListAPIView):
    serializer_class = ServiceOfferSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = ServiceOffer.objects.all().order_by('service_name')


class FindShopServiceListView(generics.ListAPIView):
    serializer_class = ShopServiceSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Shop.objects.all().order_by('shop_name')
    pagination_class = ExtraSmallResultsSetPagination

    def get_queryset(self):
        search_query = self.request.query_params.get('search_query', None)
        service_pk = self.request.query_params.get('service_pk', None)

        if search_query:
            return Shop.objects.filter(
                Q(shop_category__category_name__contains=search_query) |
                Q(services__service_name__contains=search_query)
            ).order_by('shop_name')

        if service_pk:
            return Shop.objects.filter(
                services__pk__exact=service_pk
            ).order_by('shop_name')

        return []
