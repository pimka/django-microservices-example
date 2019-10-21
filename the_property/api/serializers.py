from rest_framework import serializers
from api.models import PropertyModel

class PropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyModel
        fields = ['prop_uuid', 'addres', 'area', 'is_living', 'owner_uuid']