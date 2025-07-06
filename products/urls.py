from django.urls import path
from products.views import detail, catalog


name_app = "products"

urlpatterns = [
   
    path("<int:my_id>/", detail, name="product-detail"),
    path("catalog/", catalog, name="catalog")
]