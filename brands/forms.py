from django import forms
from products.models import Brand


class BrandForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name,field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
        self.fields['is_active'].widget.attrs['class'] = ' '


    class Meta:
        model = Brand
        fields = '__all__'
        widgets ={
            'brand_name': forms.TextInput(attrs={'required': True}), 
            'brand_img': forms.ClearableFileInput(attrs={'required': True}), 
        }
        