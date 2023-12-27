from django import forms
from django.forms import ModelForm
from .models import CategoryOffer


class CategoryOfferForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name,field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = 'Enter here'
        self.fields['is_active'].widget.attrs['class'] = ''

    class Meta:
        model = CategoryOffer
        fields = '__all__'
    valid_to = forms.DateTimeField(
        widget=forms.TextInput(attrs={'type': 'datetime-local'}),
    )