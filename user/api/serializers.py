import django.contrib.auth.password_validation as validators
from django.core import exceptions
from rest_framework import serializers

from api.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'owner_uuid', 'password', 'username']
        extra_kwargs = {'password':{'write_only':True}}

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)

        if validated_data.get('password'):
            new_password = validated_data.get('password')
            instance.set_password(new_password)

        instance.save()
        return instance

    '''def validate(self, data):
        user = User(**data)
        password = data.get('password')
        try:
            validators.validate_password(password, user)
        except exceptions.ValidationError as err:
            raise serializers.ValidationError(err.message)
        return super(UserSerializer, self).validate(data)'''
