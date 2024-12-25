from django.db import models


class ProductStatus(models.TextChoices):
    online = 'online', 'Online'
    offline = 'offline', 'Offline'