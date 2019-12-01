from django.db import models
import uuid

ORDER_TYPES = [
    ('R', 'Rent'),
    ('P', 'Purchase'),
    ('S', 'Sale')
]

class OrderModel(models.Model):
    order_type = models.CharField(choices=ORDER_TYPES, default='R', max_length=20)
    customer_uuid = models.UUIDField()
    price = models.PositiveIntegerField()
    prop_uuid = models.UUIDField(null=False, unique=False)
    order_uuid = models.UUIDField(default = uuid.uuid4, editable = False)