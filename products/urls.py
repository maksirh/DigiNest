from django.urls import path
from products.views import catalog, addproduct, add_to_basket, basket, ProductDetail, ProductDeleteView, ProductUpdateView, create_checkout_session, stripe_webhook, basket_success, basket_cancel


app_name = "products"

urlpatterns = [
    path("<int:pk>/", ProductDetail.as_view(), name="product-detail"),
    path("catalog/", catalog, name="catalog"),
    path("addproduct/", addproduct, name="add_product"),
    path("basket/", basket, name="basket"),
    path("add-to-basket/<int:product_id>/", add_to_basket, name="add-to-basket"),
    path("deleteproduct/<int:pk>", ProductDeleteView.as_view(), name="delete-product"),
    path("editproduct/<int:pk>", ProductUpdateView.as_view(), name="edit-product" ),
    path("basket/checkout/", create_checkout_session, name="checkout"),
    path("webhook/stripe/", stripe_webhook, name="stripe-webhook"),
    path("basket/success/", basket_success, name="basket-success"),
    path("basket/cancel/", basket_cancel, name="basket-cancel"),

]