# Generated by Django 5.1.1 on 2024-10-27 18:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0010_alter_user_verified_code"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="verified_code",
            field=models.CharField(
                default="2QE07kSfJaTo2Ud9gIg7FWZUUHiZynqMXj2V512AxNhhhqbNqXk9Xy3OJYCUz8BPu690cDw4OsXCJguK5As8ZabFNyI7CwdFlrJkck0n8SQz9bJmHlJLzsTJWMXFnVIscm4KH1NdeVLTOe1XemOjwLkOyZC2h6GZJIAnk64Q1KECdRhfUTb69SDDFZhRenojNOVsQR8JT20f65dLXp5wzY3toeQaun0Jr7Vg18rNwukWGIHFDQIT96jA6w7cViF",
                max_length=255,
            ),
        ),
    ]
