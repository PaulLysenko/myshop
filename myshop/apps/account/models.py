import uuid
from django.db import models
from django.contrib.auth.models import User


class RegTry(models.Model):

    email = models.EmailField(unique=True, db_index=True)
    otc = models.UUIDField(default=uuid.uuid4, editable=False, db_index=True)
    c_time = models.DateTimeField(auto_now=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.email} at {self.c_time.strftime('%d-%m-%Y %H:%M:%S')}"
