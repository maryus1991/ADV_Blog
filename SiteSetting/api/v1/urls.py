from django.urls import path
from .views import CreateContactView, SiteSettingView

urlpatterns = [
    path("create/", CreateContactView.as_view(), name='CreateContactView'),
    path("get-site-setting/", SiteSettingView.as_view(), name='SiteSettingView'),
]
