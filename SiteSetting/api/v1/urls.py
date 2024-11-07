from django.urls import path
from .views import CreateContactView, SiteSettingView

urlpatterns = [
    path("create/", CreateContactView.as_view()),
    path("get-site-setting/", SiteSettingView.as_view()),
]
