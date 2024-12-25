from django.db import models

from modules.base.models import TimeStampeMixin


class Channel(models.Model, TimeStampeMixin):
    code = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    address = models.TextField(null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    phone = models.CharField(max_length=15)
    active = models.BooleanField(default=True)
    base_language = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "channel"
