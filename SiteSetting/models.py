from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField


# Create your models here

class SiteSetting(models.Model):
    """
    information about our site
    """
    logo = models.ImageField(upload_to='logo/')
    short_addr = models.CharField(max_length=255)
    email = models.EmailField()
    email2 = models.EmailField()
    phone_number = models.CharField(max_length=255)
    second_number = models.CharField(max_length=255)
    short_about = models.CharField(max_length=500)
    copy_right_text = models.CharField(max_length=255) 
    website_title = models.CharField(max_length=255)
    image1 = models.ImageField(upload_to='SiteSetting/')
    image2 = models.ImageField(upload_to='SiteSetting/')
    descriptions = RichTextUploadingField()
    additional_descriptions = RichTextUploadingField()
    location_link = models.URLField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.website_title
    

class Contact(models.Model):
    '''
    for contact us
    '''
    full_name = models.CharField(max_length=255)
    email = models.EmailField()
    phone_number = models.CharField(max_length=255)
    subject = models.CharField(max_length=255)
    message = RichTextUploadingField()
    is_read_by_admin = models.BooleanField(default=False)

    def __str__(self):
        return self.full_name
    