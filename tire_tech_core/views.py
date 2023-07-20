import json
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views.decorators.debug import sensitive_post_parameters
from oauth2_provider.models import get_access_token_model
from oauth2_provider.signals import app_authorized
from oauth2_provider.views.base import TokenView

from user_profile.models import UserProfile, User
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from shop.models import Shop,   ShopPhotos


class TokenViewWithUserId(TokenView):
    @method_decorator(sensitive_post_parameters("password"))
    def post(self, request, *args, **kwargs):
        url, headers, body, status = self.create_token_response(request)
        print(body)

        if status == 200:
            body = json.loads(body)
            access_token = body.get("access_token")
            if access_token is not None:
                token = get_access_token_model().objects.get(
                    token=access_token)
                app_authorized.send(
                    sender=self, request=request,
                    token=token)
                body['id'] = str(token.user.id)
                body = json.dumps(body)
        response = HttpResponse(content=body, status=status)
        for k, v in headers.items():
            response[k] = v
        return response


def registerShop(request):
    data = None
    if request.method == 'POST':
        first_name = request.POST['firstName']
        last_name = request.POST['lastName']
        address = request.POST['address']
        contact_number = request.POST['contactNumber']
        email = request.POST['emailAddress']
        password = request.POST['password']

        if User.objects.filter(email=email).exists():
            data = {
                "error_message": "Email already exists"
            }

        if User.objects.filter(username=email).exists():
            data = {
                "error_message": "Mobile number already exists"
            }

        if data is not None:

            user = User.objects.create(
                username=email, email=email, first_name=first_name, last_name=last_name)
            user.set_password(password)
            user.is_staff = True
            user.save()

            UserProfile.objects.create(user=user,
                                       address=address,
                                       contact_number=contact_number,
                                       )

            content_type_shop = ContentType.objects.get_for_model(Shop)
            content_type_shop_photos = ContentType.objects.get_for_model(
                ShopPhotos)

            shop_permissions = Permission.objects.filter(
                content_type=content_type_shop)
            shop_photos_permissions = Permission.objects.filter(
                content_type=content_type_shop_photos)

            # To add permissions
            for perm in shop_permissions:
                user.user_permissions.add(perm)

            for perm in shop_photos_permissions:
                user.user_permissions.add(perm)

            return redirect('admin:index')

    return render(request, 'register.html', data)
