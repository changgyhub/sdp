from django import forms
from .models import Staff

class LoginForm(forms.Form):
    username = forms.CharField(
        required=True,
        label="Username",
        error_messages={'required': 'Please input username'},
        widget=forms.TextInput(
            attrs={
            }
        ),
    )
    password = forms.CharField(
        required=True,
        label="Password",
        error_messages={'required': 'Please input password'},
        widget=forms.PasswordInput(
            attrs={
            }
        ),
    )
    def clean(self):
        if not self.is_valid():
            raise forms.ValidationError("You must input your username and password")
        else:
            cleaned_data = super(LoginForm, self).clean()
            
class DocumentForm(forms.Form):
    docfile = forms.FileField(
        label='Select a file'
    )