from django.db import models

from .choices import ProductStatus
from ..base.models import TimeStampeMixin
from ..channel.models import Channel
from ..store.models import Store


class Category(models.Model, TimeStampeMixin):
    code = models.CharField(max_length=255)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "category"


class Package(models.Model, TimeStampeMixin):
    code = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "package"


class CategoryChannel(models.Model, TimeStampeMixin):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='channels')
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE, related_name='categories')

    class Meta:
        db_table = "category_channel"


class Product(models.Model, TimeStampeMixin):
    sku = models.CharField(max_length=255)
    status = models.CharField(
        max_length=50,
        choices=ProductStatus.choices,
        default=ProductStatus.offline,
    )
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')

    def __str__(self):
        return self.sku

    class Meta:
        db_table = "product"


class ProductInfo(models.Model, TimeStampeMixin):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='info')
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='product_info')
    name = models.CharField(max_length=255)
    description = models.TextField()
    info = models.TextField()

    class Meta:
        db_table = "product_info"


class ProductMediaGallery(models.Model, TimeStampeMixin):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='media')
    image = models.ImageField(upload_to='product_images/')
    alt_text = models.CharField(max_length=255, null=True, blank=True)  # Text for SEO

    def __str__(self):
        return f"Media for {self.product.sku}"

    class Meta:
        db_table = "product_media_gallery"


class ProductExcludeChannel(models.Model, TimeStampeMixin):
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    class Meta:
        db_table = "product_exclude_channel"


class ProductVariant(models.Model, TimeStampeMixin):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variants')
    code = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    package = models.ForeignKey(Package, on_delete=models.CASCADE, related_name='variants')

    def __str__(self):
        return self.code

    class Meta:
        db_table = "product_variant"


class ProductVariantInfo(models.Model, TimeStampeMixin):
    product_variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE, related_name='info')
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='variant_info')
    name = models.CharField(max_length=255)

    class Meta:
        db_table = "product_variant_info"


class Additive(models.Model, TimeStampeMixin):
    price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = "additive"


class AdditiveInfo(models.Model, TimeStampeMixin):
    additive = models.ForeignKey(Additive, on_delete=models.CASCADE, related_name='info')
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='additive_info')
    name = models.CharField(max_length=255)

    class Meta:
        db_table = "additive_info"


class ProductAdditive(models.Model, TimeStampeMixin):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='additives')
    add_on = models.ForeignKey(Additive, on_delete=models.CASCADE, related_name='products')

    class Meta:
        db_table = "product_additive"


class PackageInfo(models.Model, TimeStampeMixin):
    package = models.ForeignKey(Package, on_delete=models.CASCADE, related_name='info')
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='package_info')
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = "package_info"
