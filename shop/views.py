from rest_framework import generics, permissions, response, status
from .serializers import ServiceOfferSerializer
from .models import ServiceOffer
from .paginate import ExtraSmallResultsSetPagination

class ServicesOfferListView(generics.ListAPIView):
    serializer_class = ServiceOfferSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = ServiceOffer.objects.all().order_by('service_name')
