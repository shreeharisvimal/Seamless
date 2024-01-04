from django import forms
from .models import UserProfile
 
class ImageForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('profile_pic',)

