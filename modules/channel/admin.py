from django.contrib import admin
from .models import Channel


@admin.register(Channel)
class ChannelAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'code', 'status', 'created_at')
    search_fields = ('name', 'status', 'created_at')
    list_filter = ('created_at',)

