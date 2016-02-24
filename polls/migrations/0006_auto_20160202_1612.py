# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0005_auto_20160202_1611'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pollresultspluginmodel',
            name='ordering',
            field=models.CharField(default='pk', max_length=32, choices=[('pk', 'natural'), ('-votes, choice_text', 'vote (descending)'), ('votes, choice_text', 'vote (ascending)'), ('choice_text', 'choice (a-z)')]),
        ),
    ]
