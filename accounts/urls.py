from django.urls import path
from .views import Dashboard, Authorizations, Registrations

urlpatterns = [
    path('', Dashboard.as_view(), name='Dashboard'),
    path('authorize/', Authorizations.as_view(), name='Authorizations'),
    path('register/', Registrations.as_view(), name='Registrations'),
]
