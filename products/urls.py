from django.urls import path
from products.views import detail, catalog, addproduct, add_to_basket, basket


app_name = "products"

urlpatterns = [
    path("<int:my_id>/", detail, name="product-detail"),
    path("catalog/", catalog, name="catalog"),
    path("addproduct/", addproduct, name="add_product"),
    path("basket/", basket, name="basket"),
    path("add-to-basket/<int:product_id>/", add_to_basket, name="add-to-basket"),
]