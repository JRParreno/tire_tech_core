import json
from django.shortcuts import render
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.debug import sensitive_post_parameters
from oauth2_provider.models import get_access_token_model
from oauth2_provider.signals import app_authorized
from oauth2_provider.views.base import TokenView
from user_profile.models import UserProfile
from rest_framework import generics, permissions, response, status
from django.contrib.auth.models import User
from django.conf import settings
from rest_framework.response import Response
from django.template.loader import get_template
import re
from oauth2_provider.models import (
    Application,
    RefreshToken,
    AccessToken
)
from datetime import (
    datetime,
    timedelta
)
from django.utils.crypto import get_random_string
import random
from django.conf import settings

from user_profile.models import UserProfile
from user_profile.utils import Util
from tire_tech_core import settings
from .serializers import ChangePasswordSerializer, ProfileSerializer, RegisterSerializer

class RegisterView(generics.CreateAPIView):
    permission_classes = []
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

    def create_access_token(self, user):
        application = Application.objects.all()

        if application.exists():
            self.expire_seconds = settings.OAUTH2_PROVIDER['ACCESS_TOKEN_EXPIRE_SECONDS']
            scopes = settings.OAUTH2_PROVIDER['SCOPES']
            expires = datetime.now() + timedelta(seconds=self.expire_seconds)
            token = get_random_string(32)
            refresh_token = get_random_string(32)

            access_token = AccessToken.objects.create(
                user=user,
                expires=expires,
                scope=scopes,
                token=token,
                application=application.first(),
            )

            refresh_token = RefreshToken.objects.create(
                user=user,
                access_token=access_token,
                token=refresh_token,
                application=application.first(),
            )

            return access_token, refresh_token

        return None

    def post(self, request, *args, **kwargs):
        password = request.data.get('password')
        address = request.data.get('address')
        confirm_password = request.data.get('confirm_password')
        first_name = request.data.get('first_name')
        last_name = request.data.get('last_name')
        mobile_number = request.data.get('contact_number')
        gender = request.data.get('gender')

        email = request.data.get('email')
        if User.objects.filter(email=email).exists():
            data = {
                "error_message": "Email already exists"
            }
            return response.Response(
                data=data,
                status=status.HTTP_400_BAD_REQUEST
            )

        if User.objects.filter(username=email).exists():
            data = {
                "error_message": "Mobile number already exists"
            }
            return response.Response(
                data=data,
                status=status.HTTP_400_BAD_REQUEST
            )

        if password != confirm_password:
            data = {
                "error_message": "Password does not match"
            }
            return response.Response(
                data=data,
                status=status.HTTP_400_BAD_REQUEST
            )

        user = User.objects.create(
            username=email, email=email, first_name=first_name, last_name=last_name)
        user.set_password(password)
        user.save()

        UserProfile.objects.create(user=user,
                                   address=address,
                                   contact_number=mobile_number, gender=gender,
                                   )


        data = {
            "email": user.email,
        }

        return response.Response(
            data=data,
            status=status.HTTP_200_OK
        )
    
class ProfileView(generics.RetrieveUpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ProfileSerializer

    def get(self, request, *args, **kwargs):
        user = self.request.user
        user_profiles = UserProfile.objects.filter(user=user)

        if user_profiles.exists():
            user_profile = user_profiles.first()

            data = {
                "pk": str(user.pk),
                "profilePk": str(user_profile.pk),
                "username": user.username,
                "firstName": user.first_name,
                "lastName": user.last_name,
                "email": user.email,
                "address": user_profile.address,
                "profilePhoto": request.build_absolute_uri(user_profile.profile_photo.url) if user_profile.profile_photo else None,
                "contactNumber": user_profile.contact_number,
                "isVerified": user_profile.is_verified,
                "otpVerified": user_profile.otp_verified,
                "frontIdPhoto": request.build_absolute_uri(user_profile.front_photo.url) if user_profile.front_photo else None,
                "backIdPhoto": request.build_absolute_uri(user_profile.back_photo.url) if user_profile.back_photo else None,
            }

            return response.Response(data, status=status.HTTP_200_OK)

        else:
            error = {
                "error_message": "Please setup your profile"
            }
            return response.Response(error, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, *args, **kwargs):
        user = self.request.user
        user_details = self.request.data.get('user')
        contact_number = self.request.data.get('contact_number')
        address = self.request.data.get('address')
        user_email = UserProfile.objects.filter(
            user__email=user_details['email']).exclude(user=user).exists()
        check_contact_number = UserProfile.objects.filter(
            contact_number=contact_number).exclude(user=user).exists()

        if user_email:
            error = {
                "error_message": "Email already exists"
            }
            return response.Response(error, status=status.HTTP_400_BAD_REQUEST)

        if check_contact_number:
            error = {
                "error_message": "Mobile number already exists"
            }
            return response.Response(error, status=status.HTTP_400_BAD_REQUEST)

        user_profile = UserProfile.objects.get(user=user)

        user.email = user_details['email']
        user.first_name = user_details['first_name']
        user.last_name = user_details['last_name']
        user.username = user_details['email']
        user.save()

        user_profile.address = address
        user_profile.contact_number = contact_number
        user_profile.save()

        data = {
            "pk": str(user.pk),
            "profilePk": str(user_profile.pk),
            "username": user.username,
            "firstName": user.first_name,
            "lastName": user.last_name,
            "email": user.email,
            "address": user_profile.address,
            "profilePhoto": request.build_absolute_uri(user_profile.profile_photo.url) if user_profile.profile_photo else None,
            "contactNumber": user_profile.contact_number,
            "isVerified": user_profile.is_verified,
            "otpVerified": user_profile.otp_verified,
            "frontIdPhoto": request.build_absolute_uri(user_profile.front_photo.url) if user_profile.front_photo else None,
            "backIdPhoto": request.build_absolute_uri(user_profile.back_photo.url) if user_profile.back_photo else None,
        }

        return response.Response(data, status=status.HTTP_200_OK)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({
            'request': self.request
        })
        return context


class ChangePasswordView(generics.UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"error_message": "Wrong old password."}, status=status.HTTP_400_BAD_REQUEST)
            new_password_entry = serializer.data.get("new_password")
            reg = "[^\w\d]*(([0-9]+.*[A-Za-z]+.*)|[A-Za-z]+.*([0-9]+.*))"
            pat = re.compile(reg)

            if 8 <= len(new_password_entry) <= 16:
                password_validation = re.search(pat, new_password_entry)
                if password_validation:
                    self.object.set_password(
                        serializer.data.get("new_password"))
                else:
                    return Response({"error_message":
                                     "Password must contain a combination of letters and numbers"},
                                    status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"error_message":
                                 "Password must contain at least 8 to 16 characters"},
                                status=status.HTTP_400_BAD_REQUEST)

            self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': []
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
