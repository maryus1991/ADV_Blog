# Generated by Django 5.1.1 on 2024-11-13 15:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0015_alter_user_verified_code"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="verified_code",
            field=models.CharField(
                default="eebTFqK7i4CMVcXDKwKvmtBEg0UUmk1XSaxExI8Uq0snXrg3oEUUuB6EJpLWnq4b1vzbjCUDdicui6dW5pTABCZt8Wi48TWUBmNSzyfMSPgWXiyxtOBn4DHNy2craszEbcVihZa4dt48SNxOLZkiq6Pv2oKmVCgLZX99Bceap11vLieMtkDGIouOQ3y0HRYmClCTp3JDJwaVIZk4YDizir3OPFtCRh12NdEpOxTPQ4lgm4LJswpLB6TZSpEqdyK",
                max_length=255,
            ),
        ),
    ]
