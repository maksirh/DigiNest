from django.db import models


class TypeProduct(models.Model):
    name = models.CharField(max_length=256)


class Product(models.Model):
    name = models.CharField(max_length=128)
    description = models.TextField()
    price = models.IntegerField()
    type = models.ForeignKey(to=TypeProduct, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


