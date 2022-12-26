from django import forms
from .models import User


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ['first_name','last_name','username','email','phone_number','password']

    def clean(self):
        clean_password = super(UserForm,self).clean()
        password = clean_password.get('password')
        confirm_password = clean_password.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError("Password is not match")


        