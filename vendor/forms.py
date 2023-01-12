from django import forms
from .models import Vendor, OpeningHour
from accounts.validators import allow_only_images


class VendorForm(forms.ModelForm):
    # vendor_license = forms.FileField(widget=forms.FileInput, validators=[allow_only_images]) video no.66
    class Meta:
        model = Vendor
        fields = ['vendor_name','vendor_license']

class OpeningHoursForm(forms.ModelForm):

    class Meta:
        model = OpeningHour
        fields = ['day' , 'from_hour', 'to_hour', 'is_closed']