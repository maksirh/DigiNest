from django import forms
from .models import Product, TypeProduct

class ProductForm(forms.ModelForm):
    type = forms.ModelChoiceField(
        queryset=TypeProduct.objects.all(),
        empty_label="— Оберіть тип —"
    )

    class Meta:
        model  = Product
        fields = ["name", "description", "price", "type", "image"]
