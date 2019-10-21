from api.models import OrderModel
from rest_framework import serializers

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderModel
        fields = ['order_uuid', 'order_type', 'prop_uuid', 'customer_uuid', 'price']