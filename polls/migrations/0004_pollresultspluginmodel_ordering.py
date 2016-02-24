# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0003_auto_20160202_1530'),
    ]

    operations = [
        migrations.AddField(
            model_name='pollresultspluginmodel',
            name='ordering',
            field=models.CharField(default='pk', max_length=8, choices=[('natural', 'pk'), ('descending', '-votes'), ('ascending', 'votes')]),
        ),
    ]
