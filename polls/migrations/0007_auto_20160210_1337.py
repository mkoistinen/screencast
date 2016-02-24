# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0013_urlconfrevision'),
        ('polls', '0006_auto_20160202_1612'),
    ]

    operations = [
        migrations.CreateModel(
            name='PollListPluginModel',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='cms.CMSPlugin')),
                ('polls', models.ManyToManyField(default=None, to='polls.Question', null=True, blank=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('cms.cmsplugin',),
        ),
        migrations.AlterField(
            model_name='pollresultspluginmodel',
            name='ordering',
            field=models.CharField(default='pk', max_length=32, choices=[('pk', 'natural'), ('-votes,choice_text', 'vote (descending)'), ('votes,choice_text', 'vote (ascending)'), ('choice_text', 'choice (a-z)')]),
        ),
    ]
