# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import filer.fields.image
import djangocms_text_ckeditor.fields


class Migration(migrations.Migration):

    dependencies = [
        ('filer', '0002_auto_20150606_2003'),
        ('cms', '0013_urlconfrevision'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(default='', help_text='Provide a name for this product.', max_length=8, verbose_name='code')),
                ('description', djangocms_text_ckeditor.fields.HTMLField(help_text='Please provide a description of this breed.', verbose_name='description', blank=True)),
                ('photo', filer.fields.image.FilerImageField(default=None, to=b'filer.Image', blank=True, help_text='Provide a photo of this product.', null=True, verbose_name='photo')),
            ],
        ),
        migrations.CreateModel(
            name='ProductType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(default='', help_text='Provide a name for this product type.', max_length=64, verbose_name='name')),
                ('slug', models.SlugField(default='', help_text='Provide a unique slug for this product type.', max_length=64, verbose_name='slug')),
                ('description', djangocms_text_ckeditor.fields.HTMLField(help_text='Please provide a description of this product type.', verbose_name='description', blank=True)),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='product_type',
            field=models.ForeignKey(related_name='products', default=None, to='products.ProductType', help_text='Select the product type.', null=True, verbose_name='type'),
        ),
        migrations.AlterField(
            model_name='product',
            name='name',
            field=models.CharField(default='', help_text='Provide a name for this product.', max_length=64, verbose_name='name'),
        ),
        migrations.AddField(
            model_name='product',
            name='slug',
            field=models.SlugField(default='', help_text='Provide a unique slug for this product.', max_length=64, verbose_name='slug'),
        ),
        migrations.AlterField(
            model_name='product',
            name='description',
            field=djangocms_text_ckeditor.fields.HTMLField(help_text='Please provide a description of this product.', verbose_name='description', blank=True),
        ),
        migrations.CreateModel(
            name='ProductListPluginModel',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='cms.CMSPlugin')),
                ('product_type', models.ForeignKey(default=None, blank=True, to='products.ProductType', help_text='Choose a product type or leave blank to use the current view\u2019s product type, if any.', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('cms.cmsplugin',),
        ),
        migrations.CreateModel(
            name='ProductPropertyPluginModel',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='cms.CMSPlugin')),
                ('property_name', models.CharField(default=('name', 'name'), help_text='Choose a property to display.', max_length=64, verbose_name='property name', choices=[('name', 'name'), ('product_type', 'product type'), ('description', 'description'), ('photo', 'photo')])),
                ('product', models.ForeignKey(default=None, blank=True, to='products.Product', help_text='Choose a product or leave blank to use the current view\u2019s product type, if any.', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('cms.cmsplugin',),
        ),
        migrations.CreateModel(
            name='ProductTypePropertyPluginModel',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='cms.CMSPlugin')),
                ('property_name', models.CharField(default=('name', 'name'), help_text='Choose a property to display.', max_length=64, verbose_name='property name', choices=[('name', 'name'), ('description', 'description')])),
                ('product_type', models.ForeignKey(default=None, blank=True, to='products.ProductType', help_text='Choose a product type or leave blank to use the current view\u2019s product type, if any.', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('cms.cmsplugin',),
        ),
        migrations.CreateModel(
            name='Layout',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(default='', help_text='Provide a unique name for this layout.', unique=True, max_length=64, verbose_name='name')),
            ],
        ),
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ('name',)},
        ),
        migrations.AlterModelOptions(
            name='producttype',
            options={'ordering': ('name',)},
        ),
        migrations.AddField(
            model_name='producttype',
            name='layout',
            field=models.ForeignKey(related_name='+', default=None, to='products.Layout', help_text='Select a layout for the products of this type.', null=True, verbose_name='layout'),
        ),
        migrations.AlterField(
            model_name='producttype',
            name='name',
            field=models.CharField(default='', help_text='Provide a name for this product type.', unique=True, max_length=64, verbose_name='name'),
        ),
        migrations.AlterField(
            model_name='product',
            name='name',
            field=models.CharField(default='', help_text='Provide a name for this product.', unique=True, max_length=64, verbose_name='name'),
        ),
    ]
