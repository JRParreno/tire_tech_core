from django.urls import path

from user_profile.views import (ProfileView,
                                RegisterView, ChangePasswordView,)

from shop.views import ServicesOfferListView, FindShopServiceListView

app_name = 'api'

urlpatterns = [
    path('register', RegisterView.as_view(), name='register'),
    path('profile', ProfileView.as_view(), name='profile'),
    path('change-password', ChangePasswordView.as_view(), name='change-password'),

    path('services-offer', ServicesOfferListView.as_view(), name='services-offer'),
    path('find-shop', FindShopServiceListView.as_view(),
         name='find-shop'),
]
