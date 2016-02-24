# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0004_pollresultspluginmodel_ordering'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pollresultspluginmodel',
            name='ordering',
            field=models.CharField(default='pk', max_length=16, choices=[('pk', 'natural'), ('-votes', 'vote (descending)'), ('votes', 'vote (ascending)'), ('choice_text', 'choice (a-z)')]),
        ),
    ]
