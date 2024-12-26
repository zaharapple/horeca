from django.db import models


class ChannelStatus(models.TextChoices):
    online = 'online', 'Online'
    offline = 'offline', 'Offline'
