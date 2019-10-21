import django.contrib.auth.password_validation as validators
from django.core import exceptions
from rest_framework import serializers

from api.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'owner_uuid', 'username']
        extra_kwargs = {'password':{'write_only':True}}

    '''def validate(self, data):
        user = User(**data)
        password = data.get('password')
        try:
            validators.validate_password(password, user)
        except exceptions.ValidationError as err:
            raise serializers.ValidationError(err.message)
        return super(UserSerializer, self).validate(data)'''
