# Generated by Django 5.1.1 on 2024-11-23 15:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0024_alter_user_verified_code"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="verified_code",
            field=models.CharField(
                default="drUKq1fG9MghN9G4ltDL3Jn5LSNmVf4MRuKBSRKoZFLWBhchoOLjAjW6dkQSU4h5RrcCglho1onu1GrGGXUtGoBNpqzbRkQw2sBfLekEtaGSjcvkgZlUWZhynDuA8La28dnKZs8tx8umaj2qNSkBddIxECnLUCUpP1W8IACh80U9FC0zkH0Jg5JzlfD992tVuEWbESQ1WY1sjNFdWYUKO480qIGnjJu6ehu9xhksZO3epLig9iiKlvuY205ZVBN",
                max_length=255,
            ),
        ),
    ]
