from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from newaccounts.models import UserProfile
from django.forms import ModelForm

class Email_Change_Form(forms.Form):
	email1 = forms.EmailField(required=True)
	email2 = forms.EmailField(required=True)

class Profile_Search_Form(forms.Form):
	user = forms.CharField(required=True)

class UserCreateForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
    	model = User
        fields = ('username', 'email', 'password1', 'password2')

   	def save(self, commit = True):
   		user = (UserCreateForm, self).save(commit = False)
   		user.email = self.cleaned_data['email']

   		if commit:
   			user.save()

   		return user


    

