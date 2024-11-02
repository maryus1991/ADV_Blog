from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.permissions import AllowAny
from django.urls import reverse_lazy

from SiteSetting.models import SiteSetting

from .serializers import ContactModelSerializer, SiteSettingModelSerializer


class CreateContactView(CreateAPIView):
    '''
    create post view for contact
    '''
    
    permission_classes  = [AllowAny]
    serializer_class = ContactModelSerializer
    success_url = reverse_lazy('ContactUS')


class SiteSettingView(ListAPIView):
    '''
    create post view for contact
    ''' 

    queryset = SiteSetting.objects.filter(is_active=True).all()
    serializer_class = SiteSettingModelSerializer


