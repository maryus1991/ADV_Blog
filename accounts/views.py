from django.views.generic.base import TemplateView
from django.views.generic import View 
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from django.shortcuts import redirect
# from django.contrib.auth import get_user_model

from .models import User
from .forms import RegistrationForm, LoginForm

# User = get_user_model()

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
    # success_message = 'حساب شما با موفقیت ساخته شد وبرای شما ایمیل فرستاده شد جهت تایید حساب شما'
    
    def post(self, request, *arg, **kwargs):
        # get if user is not authenticated
        if not request.user.is_authenticated:
            # get user info 
            email = request.POST.get('email')
            password = request.POST.get('password')

            # check if user is not exist
            user = User.objects.filter(email=email).exists()

            # create  user if is not exist            
            if not user :
                User.objects.create_user(
                    email=email,
                    password=password
                )
    
        # return user for login page to login and conform his account 
        return redirect(reverse('Authorizations'))
    

