from django.urls import path
from django.contrib.auth import views as auth_views

from user_profile.views import (ProfileView,
                                RegisterView, ChangePasswordView, UploadPhotoView, RequestPasswordResetEmail)

from shop.views import ServicesOfferListView, FindShopServiceListView, ShopReviewListView, shop_review_total_rate

app_name = 'api'

urlpatterns = [
    path('register', RegisterView.as_view(), name='register'),
    path('profile', ProfileView.as_view(), name='profile'),
    path('upload-photo/<pk>', UploadPhotoView.as_view(), name='upload-photo'),
    path('change-password', ChangePasswordView.as_view(), name='change-password'),

    path('forgot-password', RequestPasswordResetEmail.as_view(),
         name='forgot-password '),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(),
         name='password-reset-confirm'),

    path('services-offer', ServicesOfferListView.as_view(), name='services-offer'),
    path('find-shop', FindShopServiceListView.as_view(),
         name='find-shop'),
    path('shop-review-list/<pk>', ShopReviewListView.as_view(),
         name='shop-review-list'),
    path('shop-review-total-rate/<pk>', shop_review_total_rate,
         name='shop-total-rate'),

]
