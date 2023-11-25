from django.contrib import admin
from .models import Product,ProductVariant,Atrribute,AttributeValue,Brand


admin.site.register(Product)
admin.site.register(ProductVariant)
admin.site.register(Atrribute)
admin.site.register(AttributeValue)
admin.site.register(Brand)


    