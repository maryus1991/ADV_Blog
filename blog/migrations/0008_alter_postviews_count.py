# Generated by Django 5.1.1 on 2024-10-11 14:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0007_postviews_count"),
    ]

    operations = [
        migrations.AlterField(
            model_name="postviews",
            name="count",
            field=models.IntegerField(default=0),
        ),
    ]
