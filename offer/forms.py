

from django.forms import ModelForm
from django import forms
from .models import Coupon
from .models import CategoryOffer,SubcategoryOffer,ProductOffer


class CategoryOfferForm(ModelForm):
    class Meta:
        model=CategoryOffer
        fields=['category_name','discount']

    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["category_name"].widget.attrs.update(
            {"class":"form-control","placeholder":"Select Main Category"}
        )
        self.fields["discount"].widget.attrs.update(
            {"class":"form-control","placeholder":"Enter Discount Percentage"}
        )


class SubcategoryOfferForm(ModelForm):
    class Meta:
        model=SubcategoryOffer
        fields=['subcategory_name','discount']

    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["subcategory_name"].widget.attrs.update(
            {"class":"form-control","placeholder":"Select SubCategory"}
        )
        self.fields["discount"].widget.attrs.update(
            {"class":"form-control","placeholder":"Enter Discount Percentage"}
        )


class ProductOfferForm(ModelForm):
    class Meta:
        model=ProductOffer
        fields=['product_name','discount']

    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["product_name"].widget.attrs.update(
            {"class":"form-control","placeholder":"Select Product"}
        )
        self.fields["discount"].widget.attrs.update(
            {"class":"form-control","placeholder":"Enter Discount Percentage"}
        )





class DateInput(forms.DateInput):
    input_type = "date"


class CouponForm(forms.ModelForm):
    class Meta:
        model = Coupon
        fields = [
            "coupon_name",
            "code",
            "coupon_limit",
            "discount",
            "valid_from",
            "valid_to",
        ]
        widgets = {
            "valid_from": DateInput(),
            "valid_to": DateInput(),
        }

    def __init__(self, *args, **kwargs):
        super(CouponForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs["class"] = "form-control"








