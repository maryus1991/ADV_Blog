from django.views.generic.base import TemplateView
from django.views.generic import View 
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from django.shortcuts import redirect
from django.contrib.auth.password_validation import validate_password

from .models import User
from .forms import RegistrationForm, LoginForm



class Dashboard(LoginRequiredMixin, TemplateView):
    """
    dashboard page
    """
    template_name = 'accounts/account.html'


class Authorizations(TemplateView):
    """
    login and register page 
    """
    template_name = 'accounts/login.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        """
        send registration and login forms to page
        """
        context["RegistrationForm"] = RegistrationForm
        context["LoginForm"] = LoginForm 
        return context


class Registrations(View):
    """
    for register the user
    """

    success_url = reverse_lazy('Authorizations')
    form_class = RegistrationForm       
    success_message = 'حساب شما با موفقیت ساخته شد وبرای شما ایمیل فرستاده شد جهت تایید حساب شما'
    
    # get method for redirect to login page
    def get(self, request, *arg, **kwargs):
        return redirect(reverse('Authorizations'))

    # post method for create user
    def post(self, request, *arg, **kwargs):
        # get if user is not authenticated
        # if not request.user.is_authenticated:
        
        # get user info 
        form  = RegistrationForm( request.POST )

        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
        else :
            pass


        # validate the password 
        # try: 
        #     validate_password(password=password)
        # except : 
        #     # todo : add some massage
        #     return redirect(reverse('Authorizations'))


        # check if user is not exist
        user = User.objects.filter(email=email).exists()
        
        # create  user if is not exist            
        if not user :
            User.objects.create_user(
                email=email,
                password=password
            )
        
        # todo : send email to conform
    
        # return user for login page to login and conform his account 
        return redirect(reverse('Authorizations'))
    

