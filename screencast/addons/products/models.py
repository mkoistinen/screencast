# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.core.urlresolvers import reverse
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from cms.models import CMSPlugin
from djangocms_text_ckeditor.fields import HTMLField
from filer.fields.image import FilerImageField


@python_2_unicode_compatible
class Layout(models.Model):
    """
    This is simple a unique string used to determine unique static placeholders.
    """
    name = models.CharField(
        _('name'),
        max_length=64, default='', blank=False, unique=True,
        help_text=_('Provide a unique name for this layout.')
    )

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class ProductType(models.Model):
    """
    Product type or category.
    """
    name = models.CharField(
        _('name'),
        max_length=64, default='', blank=False, unique=True,
        help_text=_('Provide a name for this product type.')
    )

    slug = models.SlugField(
        _('slug'),
        max_length=64, default='', blank=False,
        help_text=_('Provide a unique slug for this product type.')
    )

    description = HTMLField(
        _('description'), blank=True,
        help_text=_('Please provide a description of this product type.')
    )

    layout = models.ForeignKey(
        Layout, blank=False, default=None, null=True,
        verbose_name=_('layout'), related_name='+',
        help_text=_('Select a layout for the products of this type.'))

    class Meta:
        ordering = ('name', )

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('products:product_type_detail', kwargs={
            'product_type_slug': self.slug
        })


@python_2_unicode_compatible
class Product(models.Model):

    name = models.CharField(
        _('name'), max_length=64, default='', blank=False, unique=True,
        help_text=_('Provide a name for this product.')
    )

    slug = models.SlugField(
        _('slug'),
        max_length=64, default='', blank=False,
        help_text=_('Provide a unique slug for this product.')
    )

    product_type = models.ForeignKey(
        ProductType, blank=False, default=None, null=True,
        verbose_name=_('type'), related_name='products',
        help_text=_('Select the product type.')
    )

    description = HTMLField(
        _('description'), blank=True,
        help_text=_('Please provide a description of this product.')
    )

    photo = FilerImageField(
        blank=True, null=True, default=None, verbose_name=_('photo'),
        help_text=_('Provide a photo of this product.')
    )

    class Meta:
        ordering = ('name', )

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('products:product_detail', kwargs={
            'product_type_slug': self.product_type.slug,
            'product_slug': self.slug
        })


# -----------------------------------------------------------------------------
# PLUGINS MODELS
# -----------------------------------------------------------------------------


@python_2_unicode_compatible
class ProductListPluginModel(CMSPlugin):

    product_type = models.ForeignKey(
        ProductType, blank=True, null=True, default=None,
        help_text=_("Choose a product type or leave blank to use the current "
                    "view’s product type, if any."))

    def __str__(self):
        if self.product_type:
            return "Product list for {0}".format(self.product_type.name)
        else:
            return "Product list for current page's product type"


@python_2_unicode_compatible
class ProductTypePropertyPluginModel(CMSPlugin):

    PRODUCT_TYPE_PROPERTIES = (
        ('name', _('name')),
        ('description', _('description')),
    )

    product_type = models.ForeignKey(
        ProductType, blank=True, null=True, default=None,
        help_text=_("Choose a product type or leave blank to use the current "
                    "view’s product type, if any.")
    )

    property_name = models.CharField(
        _('property name'), blank=False, default=PRODUCT_TYPE_PROPERTIES[0],
        max_length=64, choices=PRODUCT_TYPE_PROPERTIES,
        help_text=_("Choose a property to display.")
    )

    def __str__(self):
        if self.product_type:
            return "Product type «{0}» for {1}".format(
                self.property_name, self.product_type.name)
        else:
            return "Product type «{0}» for current view's product type".format(
                self.property_name)


@python_2_unicode_compatible
class ProductPropertyPluginModel(CMSPlugin):

    PRODUCT_PROPERTIES = (
        ('name', _('name')),
        ('product_type', _('product type')),
        ('description', _('description')),
        ('photo', _('photo')),
    )

    product = models.ForeignKey(
        Product, blank=True, null=True, default=None,
        help_text=_("Choose a product or leave blank to use the current "
                    "view’s product, if any."))

    property_name = models.CharField(
        _('property name'), blank=False, default=PRODUCT_PROPERTIES[0],
        max_length=64, choices=PRODUCT_PROPERTIES,
        help_text=_("Choose a property to display.")
    )

    def __str__(self):
        if self.product:
            return "Product «{0}» for {1}".format(
                self.property_name, self.product.name)
        else:
            return "Product «{0}» for current view's product".format(
                self.property_name)
