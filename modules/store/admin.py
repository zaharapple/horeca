from django.contrib import admin

from modules.store.models import Store


@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'code', 'is_default')
    search_fields = ('name', 'code')
    list_filter = ('created_at',)
