# Generated by Django 5.1.1 on 2024-11-19 15:01

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0014_alter_post_image_alter_post_image2'),
    ]

    operations = [
        migrations.AlterField(
            model_name='postscomment',
            name='comment',
            field=ckeditor.fields.RichTextField(),
        ),
    ]