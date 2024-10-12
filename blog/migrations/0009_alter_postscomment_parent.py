# Generated by Django 5.1.1 on 2024-10-11 15:11

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0008_alter_postviews_count'),
    ]

    operations = [
        migrations.AlterField(
            model_name='postscomment',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='child', to='blog.postscomment'),
        ),
    ]
