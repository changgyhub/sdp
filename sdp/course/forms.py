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
            
            
class RegisterForm(forms.Form):
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
    password_again = forms.CharField(
        required=True,
        label="PasswordConfirm",
        error_messages={'required': 'Please confirm your password'},
        widget=forms.PasswordInput(
            attrs={
            }
        ),
    )
    
    first_name = forms.CharField(
        required=False,
        label="FirstName",
        # error_messages={'required': 'Please reinput password'},
        widget=forms.TextInput(
            attrs={
            }
        ),
    )
    
    last_name = forms.CharField(
        required=False,
        label="LastName",
        # error_messages={'required': 'Please reinput password'},
        widget=forms.TextInput(
            attrs={
            }
        ),
    )
    def clean(self):
        if not self.is_valid():
            raise forms.ValidationError("Some fileds are detected empty")
        else:
            cleaned_data = super(RegisterForm, self).clean()