from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from django.core import exceptions

User = get_user_model()


class LoginForm(forms.Form):
    """ 
    login form 
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
                'placeholder': 'لطفا رمز عبور خود را وارد کنید '

        }), required=True)

class RegistrationForm(forms.Form):
    """
    register  form 
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
                'placeholder': 'لطفا رمز عبور خود را وارد کنید '

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
        # validate the password 

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
    
class ChangePasswordForm(forms.Form):
    """
    ChangePasswordForm
    """

    # password field
    password= forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'id': 'password',
                'placeholder': 'لطفا رمز عبور جدید خود را وارد کنید '

        }), required=True)

    # create conform pass field
    conform_password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'لطفا رمز عبور جدید را دوباره وارد کنید',
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
        # validate the password 

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

class SendMail_EmailField(forms.Form):
    # email field
    email= forms.EmailField( 
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control',
                'id':"username",
                'placeholder':'ایمیل خود را وارد کنید'
            }
    ), required=True)

class UpdateProfileForm(forms.ModelForm):

    '''
    form for user info update 
    '''
    # setting thr avatar part for more customizing
    avatar = forms.ImageField(
        widget=forms.FileInput(attrs={
        'class': 'form-control',
        'id':"username",}
        )
    )

    # setting and cufigoring the model form
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'avatar')
        widgets={
            'first_name': forms.TextInput(
                attrs={
                    'placeholder': 'لطفا نام خود را وارد کنید',
                    'class': 'form-control',
                    'id':"username",
                }
            )
            ,'last_name': forms.TextInput(
                attrs={
                    'placeholder': 'لطفا نام خانوادگی خود را وارد کنید',
                    'class': 'form-control',
                    'id':"username",
                }
            )
            
        }

class UpdateEmailForm(forms.Form):
    """
    updating the user email
    """
    email= forms.EmailField( 
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control',
                'id':"username",
                'placeholder':'ایمیل جدید خود را وارد کنید'
            }
    ), required=True)

class UserSetPasswordForm(forms.Form):
    '''
    for changing user password with out sending email 
    '''
    current_password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'id': 'password',
                'placeholder': 'لطفا رمز عبور فعلی خود را وارد کنید '

        }), required=True)
