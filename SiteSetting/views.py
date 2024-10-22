from django.views.generic import TemplateView
from django.contrib import messages
from django.urls import reverse
from django.shortcuts import redirect


from .models import SiteSetting
from .forms import  ContactModelForm



class AboutUS(TemplateView):
    # about us page config

    template_name = 'SiteSetting/about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # send site setting info
        context["SiteSetting"] = SiteSetting.objects.filter(is_active=True).order_by('-id').first()
        return context


class ContactUS(TemplateView):
    # contact page config

    template_name = 'SiteSetting/contact.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # send site setting info
        context["SiteSetting"] = SiteSetting.objects.filter(is_active=True).order_by('-id').first()

        # send the contact model form request
        context['ContactModelForm']  = ContactModelForm
        return context

    
    def post(self, request, *args, **kwargs):
        # for submitting the form and validate it
        form = ContactModelForm(request.POST)

        # validate and saving
        if form.is_valid():
            form.save(commit=True)

        # redirecting and set success message
            messages.success(request, 
                'پیام شما با موفقیت ارسال شد')
        else:
            messages.error(request,
                form.errors
            )
            
        return redirect(reverse('ContactUS'))
        

    