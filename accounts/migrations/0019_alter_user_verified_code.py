# Generated by Django 5.1.1 on 2024-11-23 15:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0018_alter_user_verified_code"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="verified_code",
            field=models.CharField(
                default="4givGOMnJUu3r9LN1lacUtEOEnz4RR6xXJIa0GfPYRrzZgjxIpvw1THBFOh9sBsay7ATaZIjJetkNiQl5bIHQ2u0eNXEK8wQUzv9ifLpDKTfUUM1ihG6IFszVkUfVL7wpkQV5c3OWMrLGORmFsszK6SpqpbTdta8wl2nhjLiM8APp5mEgEGtSywlluPfUwBKhgQTD2HbZ8t3nNAO5GXUHp6HQmGkserMjPe7tyfBnaWHpXOlHJurjH2HGaYoRKx",
                max_length=255,
            ),
        ),
    ]
