from django import forms
from .models import Vendor

class VendorForm(forms.ModelForm):
    
    class Meta:
        model = Vendor
        fields = ['name','services_offered','phone_number','event']
        widgets = {
            'services_offered': forms.Textarea(attrs={'rows': 5, 'placeholder': 'Enter services offered...'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'w-full border border-gray-300 rounded p-3 focus:ring-2 focus:ring-green-500 focus:outline-none',
                'placeholder': field.label
            })