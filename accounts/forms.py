from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

User = get_user_model()


class LoginForm(forms.Form):
    pass


class RegistrationForm(forms.ModelForm):
    """
    register model form 
    """

    # create conform pass field
    conform_password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'لطفا رمز عبور را دوباره وارد کنید',
                'class': 'form-control',
                'id': 'password'
            }
        ))

    class Meta:
        model = User
        fields = ('email', 'password' )
        widgets={
            'email': forms.EmailInput(
                attrs={
                    'class': 'form-control',
                    'id':"username",
                    'placeholder':'ایمیل خود را وارد کنید'
                }
            ),
            'password':forms.PasswordInput(
                attrs={

                    'class': 'form-control',
                    'id': 'password',
                    'placeholder': 'لطفا رمز عبور خود را وارد کنید ...'

                }
            )
        }
        
    def clean_conform_password(self):
        # for checking that the password  and conform_password must be equal else gonna return err
        password = self.cleaned_data["password"]
        conform_password = self.cleaned_data["conform_password"]
        
        if conform_password == password:
            return conform_password
        else :
            raise ValidationError('کلمه عبور و تکرار ان غیر هم سان هستند')

    
