from django.db import models

# Create your models here

class SiteSetting(models.Model):
    logo = models.ImageField(upload_to='logo/')
    short_addr = models.CharField(max_length=255)
    email = models.EmailField()
    email2 = models.EmailField()
    phone_number = models.CharField(max_length=255)
    second_number = models.CharField(max_length=255)
    short_about = models.CharField(max_length=500)
    copy_right_text = models.CharField(max_length=255) 
    website_title = models.CharField(max_length=255)
    image1 =   models.ImageField(upload_to='SiteSetting/')
    image2 =   models.ImageField(upload_to='SiteSetting/')
    descriptions = models.TextField()
    additional_descriptions = models.TextField()
    location_link = models.URLField()


    def __str__(self):
        return self.website_title
    

class Contact(models.Model):
    full_name = models.CharField(max_length=255)
    email = models.EmailField()
    phone_number = models.CharField(max_length=255)
    subject = models.CharField(max_length=255)
    message = models.TextField()

    def __str__(self):
        return self.full_name
    