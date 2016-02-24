# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productpropertypluginmodel',
            name='product',
            field=models.ForeignKey(default=None, blank=True, to='products.Product', help_text='Choose a product or leave blank to use the current view\u2019s product, if any.', null=True),
        ),
    ]
