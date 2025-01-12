from typing import Any, Optional

from django.contrib import admin, messages
from django.db.models import Model
from django.utils.html import mark_safe, format_html
from django.http.request import HttpRequest
from django.utils.safestring import SafeString

from modules.base.forms import get_field_from_info
from modules.product.choices import ProductStatus
from modules.product.forms import (
    CategoryChannelFormSet,
    ProductVariantInfoInlineFormSet,
    PackageInfoInlineFormSet,
    AdditiveInfoInlineFormSet,
    UniqueChannelAdditiveFormSet,
    ProductVariantFormSet,
)
from modules.product.models import (
    Category,
    CategoryChannel,
    ProductVariantInfo,
    ProductVariant,
    PackageInfo,
    Package,
    AdditiveInfo,
    Additive,
    ProductInfo,
    ProductMediaGallery,
    ProductExcludeChannel,
    ProductAdditive,
    Product,
    CategoryInfo,
    Store,
)


class CategoryChannelInline(admin.TabularInline):
    model = CategoryChannel
    extra = 1
    formset = CategoryChannelFormSet


class CategoryInfoInline(admin.TabularInline):
    model = CategoryInfo
    extra = 1
    min_num = 1


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'code', 'name_from_info')
    search_fields = ('code', 'name_from_info')
    list_filter = ('created_at',)
    inlines = [
        CategoryChannelInline,
        CategoryInfoInline,
    ]

    def name_from_info(self, obj: Model) -> Optional[str]:
        return get_field_from_info(obj, related_name='info', field_name='name')

    name_from_info.short_description = 'Name'


class ProductVariantInfoInline(admin.TabularInline):
    model = ProductVariantInfo
    formset = ProductVariantInfoInlineFormSet
    extra = 1


@admin.register(ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):
    list_display = ('id', 'code', 'price', 'product', 'package')
    search_fields = ('code', 'product__name')
    list_filter = ('product', 'created_at')
    inlines = [ProductVariantInfoInline]


class PackageInfoInline(admin.TabularInline):
    model = PackageInfo
    formset = PackageInfoInlineFormSet
    extra = 1


@admin.register(Package)
class ProductVariantAdmin(admin.ModelAdmin):
    list_display = ('id', 'code', 'name_from_info', 'price')
    search_fields = ('code', 'package__name')
    list_filter = ('code', 'created_at')
    inlines = [PackageInfoInline]

    def name_from_info(self, obj: Model) -> Optional[str]:
        return get_field_from_info(obj, related_name='info', field_name='name')

    name_from_info.short_description = 'Name'


class AdditiveInfoInline(admin.TabularInline):
    model = AdditiveInfo
    formset = AdditiveInfoInlineFormSet
    extra = 1


@admin.register(Additive)
class AdditiveAdmin(admin.ModelAdmin):
    list_display = ('id', 'name_from_info', 'price', 'created_at')
    search_fields = ('info__name',)
    list_filter = ('created_at', 'updated_at')
    inlines = [AdditiveInfoInline]

    def name_from_info(self, obj: Model) -> Optional[str]:
        return get_field_from_info(obj, related_name='info', field_name='name')

    name_from_info.short_description = 'Name'


class ProductInfoInline(admin.TabularInline):
    model = ProductInfo
    extra = 1
    min_num = 1


class ProductMediaGalleryInline(admin.TabularInline):
    model = ProductMediaGallery
    extra = 1
    fields = ('image', 'priority', 'image_preview_tag', 'alt_text')
    readonly_fields = ('image_preview_tag',)

    def image_preview_tag(self, obj: Model) -> Optional[SafeString]:
        if obj.image and obj.pk:
            return mark_safe(
                f'<img src="{obj.image.url}" id="preview-{obj.pk}" class="image-preview" style="max-height: 100px; max-width: 100px;" />'
            )
        return mark_safe(
            f'<img id="preview-new" class="image-preview" style="max-height: 100px; max-width: 100px; display: none;" />'
        )

    image_preview_tag.short_description = "Preview"


class ProductExcludeChannelInline(admin.TabularInline):
    model = ProductExcludeChannel
    formset = UniqueChannelAdditiveFormSet
    extra = 1


class ProductAdditiveInline(admin.TabularInline):
    model = ProductAdditive
    formset = UniqueChannelAdditiveFormSet
    extra = 1


class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    formset = ProductVariantFormSet
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):

    def __init__(self, model, admin_site):
        super().__init__(model, admin_site)
        self.has_error = False  # TODO: Temporary flag

    validation_messages = {
        'create_missing_info': 'Product was created but set to "offline" because ProductInfo is missing for the following stores: {}',
        'update_missing_info': 'Cannot update to "online": missing ProductInfo for: {}',
    }

    class Media:
        css = {
            'all': ('admin/css/admin_custom.css',)
        }
        js = ('admin/js/admin_custom.js',)

    change_list_template = "admin/product/change_list.html"
    list_display = ('sku', 'name_from_info', 'status', 'category', 'created_at', 'preview_media')
    search_fields = ('sku', 'category__name')
    list_filter = ('status', 'category')
    inlines = [
        ProductInfoInline,
        ProductMediaGalleryInline,
        ProductExcludeChannelInline,
        ProductAdditiveInline,
        ProductVariantInline
    ]

    def name_from_info(self, obj):
        return get_field_from_info(obj, related_name='info', field_name='name')
    name_from_info.short_description = 'Name'

    def preview_media(self, obj: Product) -> str:
        url = obj.get_preview_media()
        if url:
            return format_html(
                f'<img src="{url}" class="image-preview" style="max-height: 100px; max-width: 100px; border: 1px solid #ddd; margin-top: 5px;">'
            )
        return "No Image"

    preview_media.short_description = 'Preview'

    def save_related(self, request: HttpRequest, form: Any, formsets: list, change: bool) -> None:
        super().save_related(request, form, formsets, change)

        product = form.instance

        if product.status == ProductStatus.online:
            existing_store_ids = set(product.info.values_list('store_id', flat=True))

            formset_store_ids = set()
            for formset in formsets:
                if formset.model == ProductInfo:
                    for inline_form in formset.forms:
                        if inline_form.cleaned_data and not inline_form.cleaned_data.get('DELETE', False):
                            formset_store_ids.add(inline_form.cleaned_data['store'].id)

            all_store_ids = existing_store_ids.union(formset_store_ids)

            missing_stores = Store.objects.exclude(id__in=all_store_ids)
            if missing_stores.exists():
                missing_store_names = ", ".join(missing_stores.values_list('name', flat=True))
                if not change:
                    product.status = ProductStatus.offline
                    product.save()

                    messages.warning(
                        request,
                        self.validation_messages['create_missing_info'].format(missing_store_names)
                    )
                else:
                    # Rollback status to the old value
                    self.has_error = True
                    old_status = form.initial.get('status', ProductStatus.offline)
                    product.status = old_status
                    product.save()

                    messages.error(
                        request,
                        self.validation_messages['update_missing_info'].format(missing_store_names)
                    )

    def message_user(self, request, message, level=messages.INFO, extra_tags='', fail_silently=False):
        # TODO: Temporary method
        if level == messages.SUCCESS and self.has_error:
            return
        super().message_user(request, message, level, extra_tags, fail_silently)
