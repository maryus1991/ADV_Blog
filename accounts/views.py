from django.views.generic.base import TemplateView
from django.views.generic import View 
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from django.shortcuts import redirect
from django.contrib.auth.password_validation import validate_password
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.conf import settings

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

    # rewrite the dispatch method for redirect login user to dashboard page 
    def dispatch(self, request, *args, **kwargs):

        if request.user.is_authenticated:
            return redirect(reverse('Dashboard'))
        
        return super().dispatch(request, *args, **kwargs)
    

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
                
                # getting the elemnts
                password = form.cleaned_data.get('password')
                email = form.cleaned_data.get('email')

                # check if user is not exist
                user = User.objects.filter(email=email).exists()
                
                # create  user if is not exist            
                if not user :

                    # create user if new email
                    User.objects.create_user(
                        email=email,
                        password=password
                )   

                    # sending message 
                    messages.add_message(request, messages.SUCCESS,
                    '  حساب کاربری شما با موفقیت ساخنه شد و یک ایمیل جهت فعال سازی حساب کاربری خود ارسال شد'                        
                    )
                    # todo : send email to conform
                    return redirect(reverse('Authorizations'))
    
                else:
                    # sending message if user is exist
                    messages.warning(
                        request, 
                    'کاربری با این مشخصات قبلا ثبت نام کرد است'
                    )
                    return redirect(reverse('Authorizations'))

            else :
                # sending message if form is invalid  
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

class Login(View):
    """ 
    for login system
    """

    def get(self, request, *args, **kwargs):
        # redirect the get request to main Authorizations page
        return redirect(reverse('Authorizations'))


    def post(self, request, *args, **kwargs):
        # for creating login system
        
        # checking the uer if login or not
        if not request.user.is_authenticated:
            form = LoginForm( request.POST )

            # validate the form
            if form.is_valid():

                # getting form info
                email = form.cleaned_data.get('email')
                password = form.cleaned_data.get('password')

                # getting the user 
                user = User.objects.filter(email=email).first()
                
                # checking user if exist
                if user is not None :
                    
                    # checking user is active 
                    if user.is_active:
                        
                        # user verifications
                        if user.is_verified:
                            
                            # checking user password
                            if user.check_password(password):
                                
                                # login the user finally and redirect to dashboard
                                
                                if user == authenticate(email=email, password=password):    
                                    login(request, user)
                                    return redirect(reverse('Dashboard'))
                                else:
                                    messages.error(
                                        request,
                                        'کاربر یافت نشد'
                                    )
                                    return redirect(reverse('Authorizations'))
                                
                            else:
                                # redirect and set message for user password   
                                messages.error(
                                    request,
                                    'کاربر یافت نشد'
                                 )
                            return redirect(reverse('Authorizations'))


                        else:
                            # redirect and set message for user verifications
                            messages.info(
                                request,
                                'ایمیل شما فعال نیست لطفا انرا فعال کنید و سپس وارد شوید'
                            )
                            return redirect(reverse('Authorizations'))

                    else:
                        # redirect and set message for user activations
                        messages.info(
                            request,
                            'حساب شما فعال نیست لطفا با پشتیبانی تماس حاصل فرمایید'
                        )
                        return redirect(reverse('Authorizations'))

                else:
                    # redirect and set not found user message
                    messages.error(
                        request,
                        'کاربر یافت نشد'
                    )
                    return redirect(reverse('Authorizations'))

            else:
                # redirect and set message for invalid form
                messages.error(
                    request,
                    'لطفا اطلاعات را به صورت دقیق وارد نمایید'
                )
                return redirect(reverse('Authorizations'))

        else:
            # redirect the authenticated user to dashboard 
            messages.warning(
                request,
                'شما وارد سایت هستید'
            )
            return redirect(reverse('Dashboard'))

class Logout(View):
    # logout system

    def dispatch(self, request, *args, **kwargs):
        """
        calling and over writhing dispatch for checking the user is login for logout 
        """
        if not request.user.is_authenticated:
            # setting message and redirect to login page
            messages.warning(
                request,
                'شما باید وارد سایت شوید'
            )
            return redirect(reverse('Authorizations'))

        return super().dispatch(request, *args, **kwargs)

    
    def get(self, request, *args, **kwargs):
        # calling get method for logout is just for developer and not for user and production 
        # so if debug is true  the developer can log out via url
        if settings.DEBUG:
            logout(request)
            messages.success(
                    request,
                    'منتظر ورود دوباره شما هستیم '
                )
            return redirect(reverse('Authorizations'))

    def post(self, request, *args, **kwargs):
        # set post method for logout in production  
        logout(request)
        messages.success(
            request,
            'منتظر ورود دوباره شما هستیم '
        )
        return redirect(reverse('Authorizations'))