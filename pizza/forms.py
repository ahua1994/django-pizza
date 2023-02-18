from django import forms
from .models import Pizza


class PizzaForm(forms.ModelForm):
    class Meta:
        model = Pizza
        fields = ["size", "topping"]
        widgets = {
            "size": forms.RadioSelect,
            "topping": forms.CheckboxSelectMultiple
        }
