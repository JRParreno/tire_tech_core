from rest_framework import generics, permissions, response, status
from .serializers import ServiceOfferSerializer, ShopServiceSerializer
from .models import ServiceOffer, Shop
from .paginate import ExtraSmallResultsSetPagination
from django.db.models import Q
from .distance_formula import get_distance


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
        user_longitude = self.request.query_params.get('user_longitude', None)
        user_latitude = self.request.query_params.get('user_latitude', None)

        query_set = []
        temp_query_set = []

        if user_longitude and user_latitude:
            if search_query:
                temp_query_set = Shop.objects.filter(
                    Q(shop_category__category_name__contains=search_query) |
                    Q(services__service_name__contains=search_query)
                ).order_by('shop_name')

            if service_pk:
                temp_query_set = Shop.objects.filter(
                    services__pk__exact=service_pk
                ).order_by('shop_name')

            if len(temp_query_set) > 0:
                for temp_value in temp_query_set:
                    distance = get_distance(
                        float(user_longitude), float(user_latitude), temp_value.longitude, temp_value.latitude)
                    if distance <= 35:
                        query_set.append(temp_value)

        return query_set
