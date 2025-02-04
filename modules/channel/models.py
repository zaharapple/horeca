from django.core.exceptions import ValidationError
from django.db import models

from modules.channel.choices import ChannelStatus


class Channel(models.Model):
    code = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    status = models.CharField(
        max_length=50,
        choices=ChannelStatus.choices,
        db_index=True,
    )
    city = models.CharField(max_length=255)
    address = models.TextField(null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    phone = models.CharField(max_length=15)
    active = models.BooleanField(default=True)
    base_language = models.CharField(max_length=255)
    currency = models.CharField(max_length=255)
    
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def delete(self, *args, **kwargs):
        if self.categories.exists():
            raise ValidationError("Cannot delete channel because it has associated categories.")
        super().delete(*args, **kwargs)

    class Meta:
        db_table = "channel"
