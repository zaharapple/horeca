from django.db import models

from .choices import ProductStatus
from ..channel.models import Channel
from ..store.models import Store


class Category(models.Model):
    code = models.CharField(max_length=255, db_index=True)
    name = models.CharField(max_length=255)
    
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "category"


class Package(models.Model):
    code = models.CharField(max_length=255, db_index=True)
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2, db_index=True)
    
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "package"


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


class ProductInfo(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='info')
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='product_info')
    name = models.CharField(max_length=255)
    description = models.TextField()
    info = models.TextField()
    
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "product_info"


class ProductMediaGallery(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='media')
    image = models.ImageField(upload_to='product_images/')
    alt_text = models.CharField(max_length=255, null=True, blank=True)  # Text for SEO
    
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Media for {self.product.sku}"

    class Meta:
        db_table = "product_media_gallery"


class ProductExcludeChannel(models.Model):
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        db_table = "product_exclude_channel"


class ProductVariant(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variants')
    code = models.CharField(max_length=255, db_index=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, db_index=True)
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


class Additive(models.Model):
    price = models.DecimalField(max_digits=10, decimal_places=2, db_index=True)
    
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "additive"


class AdditiveInfo(models.Model):
    additive = models.ForeignKey(Additive, on_delete=models.CASCADE, related_name='info')
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='additive_info')
    name = models.CharField(max_length=255)
    
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "additive_info"


class ProductAdditive(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='additives')
    additive = models.ForeignKey(Additive, on_delete=models.CASCADE, related_name='products')
    
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "product_additive"


class PackageInfo(models.Model):
    package = models.ForeignKey(Package, on_delete=models.CASCADE, related_name='info')
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='package_info')
    name = models.CharField(max_length=255)

    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "package_info"
