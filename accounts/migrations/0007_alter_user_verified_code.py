# Generated by Django 5.1.1 on 2024-10-19 15:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_alter_user_verified_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='verified_code',
            field=models.CharField(default='VGiuPhrl7viOhpc6ng0tvtSU1U9LPpZ9rhsl82ZM2EOgLziJaFgzgEPAHzmvq85MyAY17Ki1IIbxMwNbZYKJGMSuZ0sGp0jiFHm5BcHWMM089QAgw3iDCVpVWVHzaI7iNlVXhpNZF99chEXvNS4aN3hr7SQUHCxAw8PoKuoGzSTPfKR39eJchPIvCVczxF6q8Zs1v7NnSDcCivQ3rCW7YZrSjnC2BrQQ1ANphTy13lARSfka6N6VMlgUe6jh4eE', max_length=255),
        ),
    ]