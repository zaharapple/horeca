import os

from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.signals import post_delete
from django.core.validators import MinValueValidator
from django.dispatch import receiver

from .choices import ProductStatus
from ..base.forms import get_field_from_info
from ..channel.models import Channel
from ..store.models import Store


class Category(models.Model):
    code = models.CharField(max_length=255, db_index=True)

    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return get_field_from_info(self, 'info', 'name')

    def delete(self, *args, **kwargs):
        if self.products.exists():
            raise ValidationError("Cannot delete category because it has associated products.")
        super().delete(*args, **kwargs)

    class Meta:
        db_table = "category"
        verbose_name = "Category"
        verbose_name_plural = "Categories"


class CategoryInfo(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='info')
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='category_info')
    name = models.CharField(max_length=255)

    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "category_info"
        unique_together = ('category', 'store')


class CategoryChannel(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='channels')
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE, related_name='categories')

    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "category_channel"


class Product(models.Model):
    sku = models.CharField(max_length=255, db_index=True)
    status = models.CharField(
        max_length=50,
        choices=ProductStatus.choices,
        default=ProductStatus.offline,
        db_index=True,
    )
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.sku

    class Meta:
        db_table = "product"

    def get_preview_media(self):
        media = self.media.order_by('priority').first()
        return media.image.url if media else None


class ProductInfo(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='info')
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='product_info')
    name = models.CharField(max_length=255)
    description = models.TextField()
    info = models.TextField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "product_info"
        unique_together = ('product', 'store')


class ProductMediaGallery(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='media')
    image = models.ImageField(upload_to='product_images/')
    priority = models.PositiveSmallIntegerField(default=0)
    alt_text = models.CharField(max_length=255, null=True, blank=True)  # Text for SEO
    
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Media for {self.product.sku}"

    class Meta:
        db_table = "product_media_gallery"

    # Override the delete method to delete the file
    def delete(self, *args, **kwargs):
        if self.image:
            if os.path.isfile(self.image.path):
                os.remove(self.image.path)
        super().delete(*args, **kwargs)


class ProductExcludeChannel(models.Model):
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        db_table = "product_exclude_channel"


class Additive(models.Model):
    price = models.DecimalField(max_digits=10, decimal_places=2, db_index=True, validators=[MinValueValidator(0.01)])
    
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return get_field_from_info(self, 'info', 'name')

    class Meta:
        db_table = "additive"


class AdditiveInfo(models.Model):
    additive = models.ForeignKey(Additive, on_delete=models.CASCADE, related_name='info')
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='additive_info')
    name = models.CharField(max_length=255)
    
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "additive_info"
        unique_together = ('additive', 'store')


class ProductAdditive(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='additives')
    additive = models.ForeignKey(Additive, on_delete=models.CASCADE, related_name='products')

    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "product_additive"


class Package(models.Model):
    code = models.CharField(max_length=255, db_index=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, db_index=True, validators=[MinValueValidator(0.01)])

    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return get_field_from_info(self, 'info', 'name')

    class Meta:
        db_table = "package"


class PackageInfo(models.Model):
    package = models.ForeignKey(Package, on_delete=models.CASCADE, related_name='info')
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='package_info')
    name = models.CharField(max_length=255)

    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "package_info"
        unique_together = ('package', 'store')


class ProductVariant(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variants')
    code = models.CharField(max_length=255, db_index=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, db_index=True, validators=[MinValueValidator(0.01)])
    package = models.ForeignKey(Package, on_delete=models.CASCADE, related_name='variants')

    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.code

    class Meta:
        db_table = "product_variant"


class ProductVariantInfo(models.Model):
    product_variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE, related_name='info')
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='variant_info')
    name = models.CharField(max_length=255)

    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "product_variant_info"
        unique_together = ('product_variant', 'store')
