from django import forms
from django.contrib.auth.models import User
from .models import Event,UserAccount,Attendee

class EventForm(forms.ModelForm):

    class Meta:
        model = Event
        fields = ['name','description','location','startDate','endDate','capacity']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'w-full border border-gray-300 rounded p-3 focus:ring-2 focus:ring-green-500 focus:outline-none',
                'placeholder': field.label
            })



class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput,label="Password")
   
    class Meta:
        model = User
        fields =['username','email','password','user_role']
    user_role = forms.ChoiceField(choices=UserAccount.USER_ROLE_CHOICES,label="User Role")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'w-full border border-gray-300 rounded p-3 focus:ring-2 focus:ring-green-500 focus:outline-none',
                'placeholder': field.label
            })



class LoginForm(forms.Form):
    username = forms.CharField(label="username")
    password = forms.CharField(widget=forms.PasswordInput,label="Password")
    
    class Meta:
        model=User
        fields=['username','password']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'w-full border border-gray-300 rounded p-3 focus:ring-2 focus:ring-green-500 focus:outline-none',
                'placeholder': field.label
            })
       


class AttendeeForm(forms.ModelForm):

    class Meta:
        model=Attendee
        fields=['name','email','phone_number','event']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'w-full border border-gray-300 rounded p-3 focus:ring-2 focus:ring-green-500 focus:outline-none',
                'placeholder': field.label
            })

        self.fields['event'].queryset = Event.objects.all()