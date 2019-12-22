from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid

class User(AbstractUser):
    owner_uuid = models.UUIDField(default = uuid.uuid4, editable = False)


class CustomToken(models.Model):
    token = models.UUIDField(verbose_name='Token', default=uuid.uuid4)
    created_time = models.DateTimeField(verbose_name='Created', auto_now_add=True)

    def __str__(self):
        return self.token