# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0007_auto_20160210_1337'),
    ]

    operations = [
        migrations.AlterField(
            model_name='polllistpluginmodel',
            name='polls',
            field=models.ManyToManyField(default=None, to='polls.Question', blank=True),
        ),
    ]
