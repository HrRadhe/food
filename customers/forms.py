from django import forms
from accounts.models import User

class UserInfoForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name','last_name', 'phone_number', 'email']
