from django import forms
from django.forms import ModelForm
from order_management.models import OrderItem

class order_status_form(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    class Meta:
        model = OrderItem
        fields = ['order_status']
        widgets = {
            'order_status': forms.Select(attrs={'class': 'form-control'})
        }

