from rest_framework import generics, permissions, response, status
from .serializers import ServiceOfferSerializer, ShopServiceSerializer, ShopReviewSerializer, ShopReviewRateSerializer
from .models import ServiceOffer, Shop, ShopReview
from .paginate import ExtraSmallResultsSetPagination
from django.db.models import Q
from .distance_formula import get_distance
from rest_framework.decorators import api_view, permission_classes


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


class ShopReviewListView(generics.ListCreateAPIView):
    serializer_class = ShopReviewSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = ShopReview.objects.all().order_by('date_updated')
    pagination_class = ExtraSmallResultsSetPagination

    def get_queryset(self):
        shop_pk = self.kwargs['pk']
        queryset = ShopReview.objects.filter(
            shop__pk=shop_pk).order_by('date_updated')

        return queryset


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def shop_review_total_rate(request, pk):
    try:
        shop = Shop.objects.get(pk=pk)
    except Shop.DoesNotExist:
        return response.Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        temp_reviews = ShopReview.objects.filter(shop=shop)
        total_rate = 0

        check_user_review = temp_reviews.filter(
            user_profile__user__pk=request.user.pk)

        for review in temp_reviews:
            total_rate += review.rate
        data = {
            "rate":  total_rate / temp_reviews.count() if total_rate > 0 else 0,
            "comment_id": check_user_review.first().pk if check_user_review.exists() else None
        }

        serializer = ShopReviewRateSerializer(data)
        return response.Response(serializer.data)
