from django.contrib.auth.forms import UserCreationForm
from django import forms
from . models import Main_Category,Variation
from django.forms import ModelForm


class VariantsForm(ModelForm):
    class Meta:
        model = Variation
        fields = ["product", "variation_category", "variation_value"]