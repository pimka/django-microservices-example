from django.db import models
import uuid

class PropertyModel(models.Model):
    addres = models.CharField(max_length=250, unique=True)
    area = models.IntegerField()
    is_living = models.BooleanField()
    owner_uuid = models.UUIDField()
    prop_uuid = models.UUIDField(default = uuid.uuid4, editable = False)