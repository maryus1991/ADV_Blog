# Generated by Django 5.1.1 on 2024-10-20 16:45

import ckeditor_uploader.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("SiteSetting", "0003_alter_sitesetting_additional_descriptions_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="contact",
            name="message",
            field=ckeditor_uploader.fields.RichTextUploadingField(),
        ),
    ]
