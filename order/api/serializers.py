from api.models import OrderModel
from rest_framework import serializers
from order.settings import ACCESS_DATA


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderModel
        fields = ['order_uuid', 'order_type', 'prop_uuid', 'customer_uuid', 'price']
        
class AppSerializer(serializers.Serializer):
    app_id = serializers.CharField(label='ID')
    app_secret = serializers.CharField(label='Secret')

    def validate(self, attrs):
        _id, _secret = attrs.get('app_id'), attrs.get('app_secret')

        if _id and _secret:
            if not (_id == ACCESS_DATA['app_id'] and _secret == ACCESS_DATA['app_secret']):
                raise serializers.ValidationError('Invalid Data', code='authorization')

        else:
            raise serializers.ValidationError('Miss Data', code='authorization')

        return attrs