from django.contrib import admin
from .models import Contact, SiteSetting

# Register your models here.

admin.site.register(Contact)
admin.site.register(SiteSetting)