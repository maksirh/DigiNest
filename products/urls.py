from django.urls import path
from products.views import catalog, addproduct, add_to_basket, basket, ProductDetail


app_name = "products"

urlpatterns = [
    path("<int:pk>/", ProductDetail.as_view(), name="product-detail"),
    path("catalog/", catalog, name="catalog"),
    path("addproduct/", addproduct, name="add_product"),
    path("basket/", basket, name="basket"),
    path("add-to-basket/<int:product_id>/", add_to_basket, name="add-to-basket"),
]