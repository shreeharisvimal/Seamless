from django.db import models
from django.utils.text import slugify
from category_manage.models import Category
from django.db.models import UniqueConstraint, Q
from PIL import Image

class Brand(models.Model):
    brand_name = models.CharField(max_length=30)
    brand_img = models.ImageField(upload_to='brand_logo/', default="")
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.brand_name
    

class Atrribute(models.Model):
    attribute_name = models.CharField(max_length=100, unique=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.attribute_name
    


class AttributeValue(models.Model):
    Attribute = models.ForeignKey(Atrribute, on_delete=models.CASCADE)
    Attribute_value = models.CharField(max_length=50, unique=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self)->str:
        return f"{self.Attribute} : {self.Attribute_value}"



class Product(models.Model):
    product_name = models.CharField(max_length=49,unique=True, null=False)
    product_catg = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    product_slug = models.SlugField(unique=True, blank=True, max_length=200)
    product_img = models.ImageField(upload_to='mproducts/',null=True,blank=True)
    product_description = models.TextField(max_length=500)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    product_brand = models.ForeignKey(Brand,on_delete=models.CASCADE)


    def save(self, *args, **kwargs):
        product_slug_name = '-'.join([
            self.product_name,
            self.product_catg.category_name,
            self.product_brand.brand_name
        ])
        base_slug = slugify(product_slug_name)
        self.product_slug = base_slug
        super(Product, self).save(*args, **kwargs)

    def __str__(self):

        return f"{self.product_name}"
    


class ProductVariant(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE ,related_name='product_variants')
    model_id = models.CharField(max_length=30, unique=True,null=False)
    color = models.TextField(max_length=50,blank = True)
    ram = models.TextField(max_length=50,blank = True)
    storage = models.TextField(max_length=50,blank = True)
    os = models.TextField(max_length=50,blank = True)
    screen_size = models.TextField(max_length=50,blank = True)
    max_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    sale_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    stock = models.IntegerField()
    product_varient_slug = models.SlugField(unique=True, blank=True,max_length=350)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    description = models.TextField(max_length=500, blank=True)




    def save(self, *args,**kwargs):
        base_slug = '-'.join([
            self.product.product_name,
            self.product.product_brand.brand_name,
            self.product.product_catg.category_name,
            self.model_id,
        ])
        self.product_varient_slug = slugify(base_slug)
        super(ProductVariant, self).save(*args, **kwargs)




    class Meta:
        constraints = [
            UniqueConstraint(
                name="unique_skuid_must_be_provided",
                fields=['product', 'model_id'],
                condition=Q(model_id__isnull=False)
            )
        ]


    
    def name(self):
        return f'{self.product.product_name} {self.color} {self.ram} {self.storage}'

    
    def get_variant_name(self):

        return f"{self.product.product_name} (RAM : {self.ram}, ROM :{self.storage}, COLOR : {self.color}, PRICE: {self.sale_price})"
    
    
class VariantImage(models.Model):
    variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE)
    images = models.ImageField(upload_to='varient_img/')

    def __str__(self):
        return f"Images for {self.variant.product_varient_slug}"






