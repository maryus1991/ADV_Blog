# Generated by Django 5.1.1 on 2024-11-23 15:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0022_alter_user_verified_code"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="verified_code",
            field=models.CharField(
                default="ece2tGUUUrb3PB2KpOB4PglkfSjdKBuZDKVXDJB6DII4WwskILNz490eEkJOKmKjMZoSd3SlIET9EMkmZpM4S2vDE06RHWVJp9a3YViXCBtkMj2Nm7uKgwPAnFPWhd2ljyXIMBHRXcPt3LaYPdWcXNtnJ4DSsOUMS9ymtYQ5c55sSZTo7SGnkrpPdjTllKZpSotBS9yBvxTroJcJUHvvcYrmpiGh7uBGzQ1y9WQSR8glhTMAxfNNdGZ4JuieMXP",
                max_length=255,
            ),
        ),
    ]
