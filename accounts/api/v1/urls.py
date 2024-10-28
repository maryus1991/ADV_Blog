from django.urls import path

from .views import Registrations

urlpatterns = [
    path('registrations', Registrations.as_view())
]
