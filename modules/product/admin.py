from django.contrib import admin
from django.utils.html import mark_safe, format_html

from modules.base.forms import get_field_from_info
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

    def name_from_info(self, obj):
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

    def name_from_info(self, obj):
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

    def name_from_info(self, obj):
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

    def image_preview_tag(self, obj):
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

    def preview_media(self, obj):
        url = obj.get_preview_media()
        if url:
            return format_html(
                f'<img src="{url}" class="image-preview" style="max-height: 100px; max-width: 100px; border: 1px solid #ddd; margin-top: 5px;">'
            )
        return "No Image"

    preview_media.short_description = 'Preview'
