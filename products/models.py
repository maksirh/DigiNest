from django.db import models
from django.contrib.auth.models import User


class TypeProduct(models.Model):
    name = models.CharField(max_length=256)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=128)
    shortDescription = models.CharField(max_length=256)
    description = models.TextField()
    price = models.IntegerField()
    type = models.ForeignKey(to=TypeProduct, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="products_images", blank=True)
    seller = models.ForeignKey(User, on_delete=models.CASCADE, default='1')
    views = models.BigIntegerField(default=0)

    def __str__(self):
        return self.name
    
    def update_views(self):
        self.views += 1


class Basket(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, blank=True, related_name="baskets")
    paid = models.BooleanField(default=False)

    def total_price(self):
        return sum(p.price for p in self.products.all())

    def __str__(self):
        return f"Basket {self.pk} for {self.user.username}"
