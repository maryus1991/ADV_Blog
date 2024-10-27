from SiteSetting.models import Contact, SiteSetting
from rest_framework import serializers


class ContactModelSerializer(serializers.ModelSerializer):
    """
    serializer the contact model
    """
    class Meta:
        model = Contact
        read_only_fields = ['id']


class SiteSettingModelSerializer(serializers.ModelSerializer):
    """
    serialize the site setting model
    """
    class Meta:
        model = SiteSetting
        read_only_fields = ['id']