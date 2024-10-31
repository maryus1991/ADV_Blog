from django.views.generic.base import TemplateView
from django.views.generic import View, RedirectView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from django.shortcuts import redirect
from django.contrib.auth.password_validation import validate_password
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.conf import settings
from django.utils.crypto import get_random_string
from django.shortcuts import get_object_or_404, render

from mail_templated import EmailMessage, send_mail

from datetime import datetime

from blog.models import PostsComment
from utils.SendEmailThread import SendEmailThread

from .models import User
from .forms import (
                    RegistrationForm, LoginForm, ChangePasswordForm, 
                    SendMail_EmailField, UpdateProfileForm, UpdateEmailForm,
                    UserSetPasswordForm, ChangePasswordForm
                    )



class Dashboard(LoginRequiredMixin, TemplateView):
    """
    dashboard page
    """
    template_name = 'accounts/account.html'

    def get_context_data(self, **kwargs) :
        # setting the form in context data
        context = super().get_context_data(**kwargs)

        # getting the user
        context["User"] = self.request.user 

        # updating user info  
        context['UpdateProfileForm'] = UpdateProfileForm(instance=self.request.user)

        # updating user email
        context['UpdateEmailForm'] = UpdateEmailForm(initial={
                                    'email': self.request.user.email})

        # change password from dashboard
        context['UserSetPasswordForm'] = UserSetPasswordForm ()
        context['ChangePasswordForm'] = ChangePasswordForm ()
        return context
    

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
                    user = User.objects.create_user(
                        email=email,
                        password=password
                )   

                    # set the random string for user to sent it with email
                    user.verified_code = get_random_string(255)
                    user.save()

                    # sending message 
                    messages.add_message(request, messages.SUCCESS,
                    '  حساب کاربری شما با موفقیت ساخنه شد و یک ایمیل جهت فعال سازی حساب کاربری خود ارسال شد'                        
                    )
                    
                    # set the context for send it to email template
                    context = {
                        'url': str(request.get_host()) + reverse('ConformAccount', kwargs={
                            'token': user.verified_code
                        })
                    }

                    # create email object
                    email_message = EmailMessage('Email/ActivationAccount.tpl', 
                                context, settings.EMAIL_HOST_USER, [email]) 

                    # send email with threading 
                    SendEmailThread(email_message).start()


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
                                    user.verified_code = get_random_string(255)
                                    user.save()
                                    login(request, user)
                                    messages.success(
                                        request,
                                        'خوش امدید'
                                    )
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


class ConformAccount(RedirectView):
    """
    get the verified token and verify the account
    """
    
    
    pattern_name = 'Authorizations'

    def get_redirect_url(self,  *args, **kwargs):
        """
        verify the the user account if the user enter the current token
         
        """
        # get the token from url
        token = kwargs.get('token')
        
        # get the user object
        user = get_object_or_404(User, verified_code=token)

        # edit and verify the user and save
        user.is_verified = True
        user.verified_date = datetime.now()
        user.verified_code = get_random_string(255)
        user.save()

        # adding message
        messages.success(
            self.request,
            'حساب شما با موفقیت فعال شد'
        )
        # send the user to login page
        return reverse('Authorizations')


class ForgotPassword(View):
    """
    template view for forgot pass send email 
    """

    
    def dispatch(self, request, *args, **kwargs):
        """
        calling the dispatch method for checking that the user is not login  
        """
        if request.user.is_authenticated:
            messages.warning(
                request,
                'لطفا اول از حساب کاربری خود خارج شوید'
            )

            # edit the user verify code 
            user = get_object_or_404(User, id = request.user.id)
            
            # redirect the user to dashboard 
            return redirect(reverse('Dashboard'))

        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        # for return a render page to email input
        return render(request, 'accounts/ForgotPassword_SendPassword.html', 
            {'SendMail_EmailField': SendMail_EmailField})

    def post(self, request, *args, **kwargs):
        # post method for check and validate email and send email

        # form validate
        form = SendMail_EmailField( request.POST )
        if form.is_valid():

            # getting email
            email = form.cleaned_data.get('email')

            # getting user by email
            user = User.objects.filter(email= email).first()

            # checking if user exist
            if user is not None:
                # todo send mail
                
                
                messages.success(
                    request,
                    f'ایمیل با موفقیت برای ایمیل ( {  email  } ) شما ارسال شد'
                )
                return redirect(reverse('ForgotPassword'))

            else:
                # add the error and message if user is not exist
                messages.error(
                    request,
                    'کاربر یافت نشد'
                )
                return redirect(reverse('ForgotPassword'))
        else:
            # add the error and message if form is not valid
            messages.error(
                request,
                form.errors
            )
            return redirect(reverse('ForgotPassword'))


class ForgotPassword_Token(View):
    """
    change the user password and detach the user user from token
    """


    def dispatch(self, request, *args, **kwargs):
        """
        calling the dispatch method for checking that the user is not login  
        """
        if request.user.is_authenticated:
            messages.warning(
                request,
                'لطفا اول از حساب کاربری خود خارج شوید'
            )

            # edit the user verify code 
            user = get_object_or_404(User, id = request.user.id)
            
            # redirect the user to dashboard 
            return redirect(reverse('Dashboard'))

        return super().dispatch(request, *args, **kwargs)
    

    def get(self, request, *args, **kwargs):
        # get method for showing change pass form
        return render(request, 'accounts/ForgotPassword.html', {'ChangePasswordForm': ChangePasswordForm})

    def post(self, request, *args, **kwargs):
        # post method for set the new pass in db
        
        # get the token
        token = kwargs.get('token')

        # getting the form 
        form = ChangePasswordForm(request.POST)

        # form validation and getting the password 
        if form.is_valid():
            password = form.cleaned_data.get('password')

            # getting the user
            user = get_object_or_404(User, verified_code = token)
            
            # checking if user is exist
            if user is not None:
                user.set_password(password)
                user.verified_code = get_random_string(255)
                user.save()
                messages.success(
                    request,
                    'رمز عبور شما با موفقیت تغییر یافت'
                )
                return redirect(reverse('Authorizations'))
            else:
                messages.error(
                    request,
                    'کابر یافت نشد'
                )
                return redirect(reverse('Authorizations'))

        else:
            # returning the invalid form errors 
            messages.error(
                    request,
                    form.errors
                    )
            return redirect(reverse('ForgotPassword_token', kwargs={'token': token}))
            

class ChangePassword(LoginRequiredMixin, RedirectView):
    """
    redirect view for changing the password and return to dashboard page
    """
    def get_redirect_url(self,  *args, **kwargs):
        # getting request and forms
        request = self.request

        # get the current password from user
        current_password_form = UserSetPasswordForm(request.POST)

        # get the new password from user
        password= ChangePasswordForm(request.POST)

        # getting the user 
        user = get_object_or_404(User, pk= request.user.pk) 

        # current_password validations form
        if current_password_form.is_valid():

            # get the password
            current_password = current_password_form.cleaned_data.get('current_password')

            # checking the password
            if user.check_password(current_password):
                
                # validating the new password form 
                if password.is_valid():
                    
                    # the new password 
                    new_password = password.cleaned_data.get('password')
                    
                    # checking the password is not the same
                    if current_password == new_password:
                        messages.error(request,
                            'رمز های عبور های شما یکسان هستند'
                        )
                        return reverse('Dashboard')

                    # set and save ew password for user and send message and redirect for user
                    user.set_password(new_password)
                    user.save()
                    messages.success(
                        request,
                        'رمز عبور شما با موفقیت تغییر یافت'
                    )
                    return reverse('Dashboard')

                else:
                    # setting form invalid message
                    messages.error(
                        request,
                        password.errors
                    )
                    return reverse('Dashboard')
                
            else:
                # setting message for wrong pass
                messages.error(
                    request,
                    'رمز عبور شما اشتباه است'
                )
                return reverse('Dashboard')


        else:
            # invalid error set
            messages.error(
                request,
                current_password_form.errors
            )
            return reverse('Dashboard')
        
        return reverse('Dashboard')


class ChangeEmail(LoginRequiredMixin, RedirectView):
    """
    getting and conforming and set the new email for user
    """
    def get_redirect_url(self, *args, **kwargs):
        # getting request
        request = self.request

        # get email and form and validate it 
        email_form = UpdateEmailForm(request.POST)
        if email_form.is_valid():
            
            # getting new email
            email = email_form.cleaned_data.get('email')

            # checking if emails are same
            if email == request.user.email:
                messages.error(
                    request,
                    'ایمل جدید با ایمیل قبلیتان یکسان هستن'
                )
                return reverse('Dashboard')
            
            # checking the email is unique  
            exist_user = User.objects.filter(email=email).exists
            if not exist_user :

                # setting message and redirect user to forgot pass page
                messages.error(
                    request,
                    'این ایمیل وجود دارد'
                )
                return reverse('Dashboard')
            
            # get user 
            user = get_object_or_404(User, id=request.user.id)

            # get and set to user db and send to user email the verified_code
            verified_code = get_random_string(255)

            # change the comment with the last email with the new
            comments = PostsComment.objects.filter(email=user.email).all()
            for comment in comments:
                comment.email = email
                comment.save()

            # set email and set un verified the account 
            user.is_verified = False
            user.email = email
            user.updated_at = datetime.now()
            user.verified_code = verified_code
            user.save()

            # set message and send email
            messages.success(
                request,
                'ایمیل شما با موفقیت تغییر یافت و  یک ایمیل برای شما ارسال شد لطفا اول ایمیل را تایید و سپس دوباره وارد سایت شوید'
            )
            
            # todo send email

            # logout the user and sent it to login again
            logout(request)
            return reverse('Dashboard')

        else:
            messages.error(
                request,
                email_form.errors
            )


        return reverse('Dashboard')


class UpdateProfile(LoginRequiredMixin, RedirectView):
    """
    getting user info from form and update them 
    """
    def get_redirect_url(self, *args, **kwargs):
        #getting request 
        request = self.request

        # getting user 
        user = get_object_or_404(User, id=request.user.id)

        # getting form and validate it and save it
        form = UpdateProfileForm(request.POST, request.FILES)
        if form.is_valid():
            
            # getting info and save
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            avatar = form.cleaned_data.get('avatar')

            

            # save the new info for user
            user.first_name = first_name
            user.last_name = last_name
            
            # setting if avatar is not None can be set
            if avatar is not None:
                user.avatar = avatar
                
            user.updated_at = datetime.now()
            user.save()
            
            # add message and redirect user to dashboard page
            messages.success(
                request,
                'اطلاعات شما با موفقیت بروزرسانی شد'
            )
            return reverse('Dashboard')

        else:
            # set invalid messages
            messages.error(
                request,
                form.errors
            )
            return reverse('Dashboard')
        return reverse('Dashboard')


class ResentEmail(View):
    '''
    for resent email if email is exist 
    '''
    def get(self, request, *args, **kwargs):
        """
        for set the email form 
        """
        return render(request, 'accounts/ResentEmail.html', {'UpdateEmailForm':UpdateEmailForm})

    def post(self, request, *args, **kwargs):
        """
        post method and def for resent the email
        """

        # get the form and email
        email_form = UpdateEmailForm(request.POST)
        
        # email form validations
        if email_form.is_valid():

            # getting email from form
            email = email_form.cleaned_data.get('email')

            # get user
            user = User.objects.filter(email=email).first()
            
            # check user is exist 
            if user is None:
                messages.error(
                    request, 
                    'کاربر یافت نشد'
                )
                return  redirect(reverse('ResentEmail'))
            
            # set new code for
            user.verified_code = get_random_string(255)
            user.save()

            # get the verfied code 
            verify_code = user.verified_code


            # set the context for send it to email template
            context = {
                'url': str(request.get_host()) + reverse('ConformAccount', kwargs={
                    'token': user.verified_code
                })
            }
            
            send_mail('Email/ActivationAccount.tpl', 
                        context, settings.EMAIL_HOST_USER, [user.email])

            # create email object
            email_message = EmailMessage('Email/ActivationAccount.tpl', 
                        context, settings.EMAIL_HOST_USER, [user.email]) 

            # send email with threading 
            SendEmailThread(email_message).start()

            # set message and redirect th user
            messages.success(
                    request, 
                    f'لینک فعال سازی برای این ایمیل ( {user.email} ) ارسال شد'
                )
            return  redirect(reverse('ResentEmail'))

        else:
            # set invalid error message
            messages.error(
                request,
                email_form.errors
            ) 
            return  redirect(reverse('ResentEmail'))