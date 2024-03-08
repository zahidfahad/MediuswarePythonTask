from django.contrib import admin
from .models import Product,ProductVariant,ProductVariantPrice,ProductImage

# Register your models here.


admin.site.register(Product)
admin.site.register(ProductVariant)
admin.site.register(ProductVariantPrice)
admin.site.register(ProductImage)