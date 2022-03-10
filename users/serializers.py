from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from .models import Customer


class CreateCustomerSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=65, min_length=8, write_only=True)

    class Meta:
        model = Customer
        fields = ('email', 'password',)

    def validate(self, attrs):
        email = attrs.get('email', '')
        if Customer.objects.filter(email=email).exists():
            raise serializers.ValidationError({'email', _(f'The email {email} already exists')})
        return super().validate(attrs)

    def create(self, validated_data):
        return Customer.objects.create_user(**validated_data)


# class LoginSerializer(serializers.ModelSerializer):
#     password = serializers.CharField(max_length=65, min_length=8, write_only=True)
#
#     class Meta:
#         model = Customer
#         fields = ('email', 'password', 'token')
#
#         read_only_fields = ('token', )
