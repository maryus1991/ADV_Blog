# Generated by Django 5.1.1 on 2024-10-18 17:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_alter_user_updated_at_alter_user_verified_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='verified_code',
            field=models.CharField(default='5Ns2AMfp2uK48QQl6lg0JfmePGKXoiR11BazDWedxmU5KOjvYNz1itXa3d65AOLLB2AqQRNIEev4ZCZCMV9E4y5YedgnqczfNp9CiDiW1Y4fILpIumFzbhwftycplu8NSfuuF0Z8q7JiJ8illOpuPX2MVEkNHijfmhb0SiJSYJBILLlbXaxVvsNYCo0Krcu8pIFLk13zfFJajNyFscOQ9FTVqflqmfNLcXwcZa64Nz9sRDCpkFijVPXnHzs35Gg', max_length=255),
        ),
    ]
