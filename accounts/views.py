from django.views.generic.base import TemplateView
from django.views.generic import View 
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from django.shortcuts import redirect
from django.contrib.auth.password_validation import validate_password
from django.contrib import messages
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


    # get method for redirect to login page
    def get(self, request, *arg, **kwargs):
        return redirect(reverse('Authorizations'))

    # post method for create user
    def post(self, request, *arg, **kwargs):
        # get if user is not authenticated
        if not request.user.is_authenticated:
            
            # get user info from form
            form  = RegistrationForm(  request.POST  )



            if form.is_valid():

                password = form.cleaned_data.get('password')
                email = form.cleaned_data.get('email')

                # check if user is not exist
                user = User.objects.filter(email=email).exists()
                
                # create  user if is not exist            
                if not user :

                    User.objects.create_user(
                        email=email,
                        password=password
                )
                    messages.add_message(request, messages.SUCCESS,
                    '  حساب کاربری شما با موفقیت ساخنه شد و یک ایمیل جهت فعال سازی حساب کاربری خود ارسال شد'                        
                    )
                    # todo : send email to conform
                    return redirect(reverse('Authorizations'))
    
                else:
                    messages.warning(
                        request, 
                    'کاربری با این مشخصات قبلا ثبت نام کرد است'
                    )
                    return redirect(reverse('Authorizations'))

            else :
                messages.error(
                    request,
                    form.errors
                )

                return redirect(reverse('Authorizations'))




            # return user for login page to login and conform his account 
            return redirect(reverse('Authorizations'))
        
        else :
            # send the user for the dashboard page if login 
            messages.warning(
                request,
                'شما وارد سایت هستید'
            )
            return redirect(reverse('Dashboard'))

