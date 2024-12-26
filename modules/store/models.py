from django.db import models


class Store(models.Model):
    code = models.CharField(max_length=255, db_index=True)
    name = models.CharField(max_length=255)
    is_default = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "store"
