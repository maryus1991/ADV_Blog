# Generated by Django 5.1.1 on 2024-10-20 17:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0009_alter_user_verified_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='verified_code',
            field=models.CharField(default='XWIGTbqmQ31iWqFKJlmcfTXeQhwL93evHeX8KtbofTF1PCMhUVwiL06HiR8fdyZEJWG8mw9T6yoi7kxHawqaM8k8srjy8PaP0xCBnU0ahPsX3uG5zfKveyOmy93Nr3WPs0sPnOzw5DMDCfUAPJuGB9TRFHBHpn4x4QXTh55h8yajc7rBMRhlsDVM5giYrfRF5rfP9BbjjMfQRFEduwlyUBom8rEEQJDlTK8yaFa1RQsMFTD591w9SmZln34Vh5W', max_length=255),
        ),
    ]
