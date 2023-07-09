from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'pk',
            'email',
            'first_name',
            'last_name',
            'username',
            'get_full_name'
        )

        extra_kwargs = {
            'username': {
                'read_only': True
            },
        }


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)


class RegisterSerializer(serializers.ModelSerializer):
    # set all fields required and model
    address = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)
    contact_number = serializers.CharField(write_only=True)
    gender = serializers.ChoiceField(choices=UserProfile.GENDER_CHOICES)

    class Meta:
        model = User
        fields = [
            'email', 'first_name', 'last_name',
            'password', 'confirm_password', 'contact_number', 'address',
            'gender',
        ]

        extra_kwargs = {
            'password': {'write_only': True},
            'confirm_password': {'write_only': True},
        }

    def validate(self, data):
        password = data['password']
        confirm_password = data['confirm_password']
        email_address = data['email']

        if password != confirm_password:
            raise serializers.ValidationError(
                {"error_message": "Passwords do not match"})

        return data


class ProfileSerializer(serializers.Serializer):
    user = UserSerializer()
    address = serializers.CharField()
    contact_number = serializers.CharField()

    class Meta:
        model = UserProfile
        fields = ('user', 'is_verified',
                  'otp_verified', 'address',
                  'contact_number',
                  'profile_photo', 'profile_photo_image_64')

        extra_kwargs = {
            'profile_photo': {
                'read_only': True
            },
        }

    def __init__(self, *args, **kwargs):
        # init context and request
        context = kwargs.get('context', {})
        self.request = context.get('request', None)
        super(ProfileSerializer, self).__init__(*args, **kwargs)

    def get_profile_photo(self, data):
        request = self.context.get('request')
        photo_url = data.profile_photo.url
        return request.build_absolute_uri(photo_url)

    def validate(self, attrs):
        user = attrs.get('user', None)
        contact_number = attrs.get('contact_number', None)
        # get request context
        request = self.context['request']

        errors = {}
        if user:
            email = user.get('email', None)
            if email:
                if User.objects.filter(email=email).exclude(pk=request.user.pk).exists():
                    errors['email'] = "Email address is already taken"

        if contact_number:
            if User.objects.filter(username=contact_number).exclude(pk=request.user.pk).exists():
                errors['email'] = "Mobile number is already taken"

        if errors:
            raise serializers.ValidationError(errors)

        return attrs

    def update(self, instance, validated_data):

        instance.contact_number = validated_data.pop('contact_number')
        instance.address = validated_data.pop('address')

        user = instance.user
        user_data = validated_data.pop('user')
        user.first_name = user_data.get('first_name', user.first_name)
        user.last_name = user_data.get('last_name', user.last_name)
        user.email = user_data.get('email', user.email)
        user.username = user_data.get('email', user.email)

        instance.save()

        return instance


class UploadIDPhotoSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfile
        fields = ['front_photo', 'back_photo',]

    def __init__(self, *args, **kwargs):
        # init context and request
        context = kwargs.get('context', {})
        self.request = context.get('request', None)
        self.kwargs = context.get("kwargs", None)

        super(UploadIDPhotoSerializer, self).__init__(*args, **kwargs)
