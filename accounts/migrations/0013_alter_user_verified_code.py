# Generated by Django 5.1.1 on 2024-11-05 13:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0012_alter_user_verified_code"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="verified_code",
            field=models.CharField(
                default="x2NRTUdEyyHqUuSa1PxabwejsBurIwZPi6fuo8LxfMbob8FrDQ0EKDX3WkGuZhZMtS8WffWJ9z2FgxjAIRjTI9E5WijE07rDsEZ5jGMRV4cO4rK2Ihr492wftWFvPTV5Ahm01RgFMCbWI02eBuaMhB8CQupZnA7VDzqOkV3gMlZqleJxt9dPQKOUR4M1QC0jY1Lz0xhd5hzPZQ8huGDEiFWF3BELDEVlOy6EFmOWCS2YEVFoz8UKfIi9EACcT9N",
                max_length=255,
            ),
        ),
    ]