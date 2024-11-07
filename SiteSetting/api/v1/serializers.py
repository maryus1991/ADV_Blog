from SiteSetting.models import Contact, SiteSetting
from rest_framework import serializers


class ContactModelSerializer(serializers.ModelSerializer):
    """
    serializer the contact model
    """

    class Meta:
        model = Contact
        fields = "__all__"
        read_only_fields = ["id", "is_read_by_admin"]


class SiteSettingModelSerializer(serializers.ModelSerializer):
    """
    serialize the site setting model
    """

    class Meta:
        model = SiteSetting
        fields = "__all__"
        read_only_fields = ["id"]
