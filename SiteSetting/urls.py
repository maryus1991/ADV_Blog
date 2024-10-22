from django.urls import path
from .views import AboutUS, ContactUS

urlpatterns = [
    path('about-us', AboutUS.as_view(), name='AboutUs'),    
    path('ContactUS', ContactUS.as_view(), name='ContactUS')    
]
