# Generated by Django 5.1.1 on 2024-10-16 13:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="verified_code",
            field=models.CharField(
                default="DBGHEX3OPvN7YWTgzeWOaRSTCMiGZJNrP58hMteOgpMzOcLFilezDozNs0pNvx6siTlDeSC0z3Ex4luACVgUdpPnm26O2pCd2N4jkicHyQnqHniGCcbl6mb9ua5lp6jmdnpOsvBeZFBDMONoiHR4xIR3aWHVVkOUNc5WuY2FDuqJmoqPIA4oKAgQewSLlVcUICiOcxuyziGr7zAIdblN67YEbqqFnRC3jT44ExgxUxYakTi9CGBbl4BbpIiDY0P",
                max_length=255,
            ),
        ),
    ]
