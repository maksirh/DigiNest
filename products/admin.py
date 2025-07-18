from django.contrib import admin
from .models import Product, TypeProduct

admin.site.register(TypeProduct)


admin.site.site_header = "DigiNest"


class ProductAdmin(admin.ModelAdmin):
    list_display = ["name", "price", "shortDescription"]
    search_fields = ["shortDescription", "description"]
    list_editable = ["price"]
    actions = ('make_zero',)

    def make_zero(self, request, queryset):
        queryset.update(price=0)



admin.site.register(Product, ProductAdmin)