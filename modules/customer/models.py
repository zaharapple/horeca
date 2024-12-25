from django.db import models

from ..base.models import TimeStampeMixin


class Customer(models.Model, TimeStampeMixin):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    registered_at = models.DateTimeField()
    birthday = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, null=True, blank=True)
    phone = models.CharField(max_length=15, null=True, blank=True)

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return self.full_name

    class Meta:
        db_table = "customer"

