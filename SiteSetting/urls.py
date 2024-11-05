from django.urls import path, include
from .views import AboutUS, ContactUS

urlpatterns = [
    path("about-us", AboutUS.as_view(), name="AboutUs"),
    path("ContactUS", ContactUS.as_view(), name="ContactUS"),
    path("api/v1/", include("SiteSetting.api.v1.urls")),
]
