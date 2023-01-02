from django import forms
from .models import User, UserProfile
from .validators import allow_only_images


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


class UserProfileForm(forms.ModelForm):
    # make field only read only
    # latitude = forms.CharField(widget=forms.TextInput(attrs={'readonly' : 'readonly'}))
    class Meta:
        model = UserProfile
        fields = ['profile_picture', 'cover_photo', 'address', 'country', 'state', 'city', 'pin_code', 'longitude', 'latitude']

    # make field only readable
    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            if field == 'latitude' or field == 'longitude':
                self.fields[field].widget.attrs['readonly'] = 'readonly'
