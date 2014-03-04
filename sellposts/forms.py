from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from newaccounts.models import UserProfile
from django.forms import ModelForm
from .models import SellPost 

class SellPostForm(ModelForm):
    
    image_path = forms.CharField(max_length = 255, widget = forms.HiddenInput(), required = False)

    class Meta:
        model = SellPost 
        fields = ('title', 'description', 'tags')




