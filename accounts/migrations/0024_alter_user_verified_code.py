# Generated by Django 5.1.1 on 2024-11-23 15:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0023_alter_user_verified_code"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="verified_code",
            field=models.CharField(
                default="AleMlNJFZlF2U4JZ1FoiBVduDygIm8uIQF8dKhHN9TApePoxTL2zhh3IH7RPwC5kEvuhUCdYoAwvOiEryCRQ0hNYwkAv1vvJhW97h4ND0l1txODGKtUf3ZJ2EhvPAgUXOZaQW5BM4c1jipA2Pb4Sj171mkvckzieFh3L3W5oQAbNEismbR5vpzNEG6RVFAJ9R108HmGuGEnAwT6fD254U4gYVFlaiqYE55dOglghSTuT81WtXcJD1jipL1qUc8N",
                max_length=255,
            ),
        ),
    ]