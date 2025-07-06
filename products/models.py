from django.db import models


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

    def __str__(self):
        return self.name


