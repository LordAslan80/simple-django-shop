from django import forms


class AddToCardForm(forms.Form):
    quantity = forms.IntegerField(label=False, min_value=1, widget=forms.NumberInput(attrs={
        'class':'input-counter d-flex justify-content-between', 'style':'text-align:center'
    }))


class CouponApplyForm(forms.Form):
    code = forms.CharField(label=False, widget=forms.TextInput(attrs={
        'class':'form-control', 'placeholder':'کد تخفیف'
    }))