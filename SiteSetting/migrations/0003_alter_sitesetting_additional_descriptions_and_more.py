# Generated by Django 5.1.1 on 2024-10-20 16:44

import ckeditor_uploader.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("SiteSetting", "0002_contact_sitesetting_additional_descriptions_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="sitesetting",
            name="additional_descriptions",
            field=ckeditor_uploader.fields.RichTextUploadingField(),
        ),
        migrations.AlterField(
            model_name="sitesetting",
            name="descriptions",
            field=ckeditor_uploader.fields.RichTextUploadingField(),
        ),
    ]
