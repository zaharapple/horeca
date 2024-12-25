from django.db import models

from modules.base.models import TimeStampeMixin


class Store(models.Model, TimeStampeMixin):
    code = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    is_default = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "store"
