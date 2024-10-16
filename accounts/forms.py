from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from django.core import exceptions

User = get_user_model()


class LoginForm(forms.Form):
    pass


class RegistrationForm(forms.Form):
    """
    register model form 
    """

    # email field
    email= forms.EmailField( 
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control',
                'id':"username",
                'placeholder':'ایمیل خود را وارد کنید'
            }
    ), required=True)

    # password field
    password= forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'id': 'password',
                'placeholder': 'لطفا رمز عبور خود را وارد کنید ...'

        }), required=True)

    # create conform pass field
    conform_password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'لطفا رمز عبور را دوباره وارد کنید',
                'class': 'form-control',
                'id': 'password'
            }
        ), required=True)

        
    def clean_conform_password(self):
        # for checking that the password  and conform_password must be equal else gonna return err
        password = self.cleaned_data.get('password')
        conform_password = self.cleaned_data.get("conform_password")
        
        if conform_password == password:
            return conform_password
        else :
            raise ValidationError('** کلمه عبور و تکرار ان غیر هم سان هستند'+" **")


    def clean_password(self):
        password = self.cleaned_data.get("password")

        try:
            validate_password(password)
            return password
        except exceptions.ViewDoesNotExist:
            raise ValidationError(
                '''

                ** رمز عبور شما باید حداقل 8 کاراکتر باشد **
                **  رمز عبور قابل پیش بینی هست **
                **  رمز عبور باید یک حرف کوچیک و بزرگ باشد و دارای اعداد و کارکتر های خاص باشد**

                '''
            )
    

    
