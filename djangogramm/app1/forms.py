from crispy_forms.helper import FormHelper
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Image, User


class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['image_file']


class LoginForm(AuthenticationForm):
    helper = FormHelper()
    helper.form_method = 'POST'
    helper.form_class = 'form-horizontal'
    helper.label_class = 'col-lg-5 control-label'
    helper.field_class = 'col-lg-8'

    class Meta:
        model = User
        fields = ('email', 'password')
        widgets = {
            'email': forms.EmailInput(attrs={'placeholder': 'Email Address'}),
            'password': forms.PasswordInput(attrs={'placeholder': 'Password'}),
        }


class RegisterUserForm(UserCreationForm):
    helper = FormHelper()
    helper.form_method = 'POST'
    helper.form_class = 'form-horizontal'
    helper.label_class = 'col-lg-5 control-label'
    helper.field_class = 'col-lg-8'
    # email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-input'}))
    # password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    # password2 = forms.CharField(label='Repeat Password', widget=forms.PasswordInput(attrs={'class': 'form-input'}))

    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')
        widgets = {
            'email': forms.EmailInput(attrs={'placeholder': 'Email Address'}),
            'password1': forms.PasswordInput(attrs={'placeholder': 'Password'}),
            'password2': forms.PasswordInput(attrs={'placeholder': 'Repeat Password'}),
        }


    # class Meta:
    #     model = User
    #     fields = ('email', 'password1', 'password2')
    #     widgets = {
    #         'email': forms.EmailInput(attrs={'placeholder': 'Email Address'}),
    #         'password1': forms.PasswordInput(attrs={'placeholder': 'Password1'}),
    #         'password2': forms.PasswordInput(attrs={'placeholder': 'Password2'}),
    #     }