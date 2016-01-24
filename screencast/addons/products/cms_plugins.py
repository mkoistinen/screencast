# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.core.exceptions import ImproperlyConfigured
from django.utils.translation import ugettext_lazy as _

from cms.models import CMSPlugin
from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from .models import (
    ProductType, Product,
    ProductListPluginModel,
    ProductTypePropertyPluginModel, ProductPropertyPluginModel,
)


class ViewObjectMixin(object):
    """
    This mixin adds convenience methods for resolving model objects from the
    request object.
    """
    def get_object_queryset(self, model=None, **kwargs):
        """
        Returns the queryset to use for getting the object. It is abstracted to
        this method so that it is easily extended/overridden for application-
        specific cases.
        """
        if model:
            return model.objects.all()
        else:
            raise ImproperlyConfigured(
                "get_object_queryset() did not receive a model.")

    def get_object_from_context(self, context, model, name):
        context_object = context.get(name, None)
        if context_object and isinstance(context_object, model):
            return context_object
        else:
            return None

    def get_object_from_resolver(self, request, queryset=None, model=None,
                                 pk_url_kwarg=None, slug_field="slug",
                                 slug_url_kwarg=None):
        """
        Given the parameters provided, inspect the request object's
        `resolver_match` object to identify the desired type of object, look it
        up from the database and return it.
        """
        if queryset is None:
            queryset = self.get_object_queryset(model, request=request)

        if request and request.resolver_match:
            kwargs = request.resolver_match.kwargs
            pk = kwargs.get(pk_url_kwarg, None)
            slug = kwargs.get(slug_url_kwarg, None)
            if pk is not None:
                return queryset.filter(pk=pk).first()
            if slug is not None:
                return queryset.filter(**{slug_field: slug}).first()
        return None


class ProductTypeMixin(ViewObjectMixin):
    def get_product_type(self, context, instance):
        """
        Returns the first ProductType found by inspecting (in order):
        1. The plugin instance `product_type` field;
        2. The context;
        3. The current request's resolver_match.
        """
        return (
            getattr(instance, "product_type", None) or
            self.get_object_from_context(context, ProductType, "product_type") or
            self.get_object_from_resolver(
                context.get('request'),
                model=ProductType,
                slug_field="slug",
                slug_url_kwarg="product_type_slug"
            )
        )


class ProductMixin(ViewObjectMixin):
    def get_product(self, context, instance):
        """
        Returns the first Product found by inspecting (in order):
        1. The plugin instance `product` field;
        2. The context;
        3. The current request's resolver_match.
        """
        return (
            getattr(instance, "product", None) or
            self.get_object_from_context(context, Product, "product") or
            self.get_object_from_resolver(
                context.get('request'),
                model=Product,
                slug_field="slug",
                slug_url_kwarg="product_slug"
            )
        )


class ProductTypeListPlugin(CMSPluginBase):
    cache = False
    model = CMSPlugin
    module = 'Products App'
    name = _('Product Type List')
    render_template = 'products/plugins/producttype_list.html'
    text_enabled = True

    def render(self, context, instance, placeholder):
        context['product_types'] = ProductType.objects.all()
        return context

plugin_pool.register_plugin(ProductTypeListPlugin)


class ProductListPlugin(ProductTypeMixin, CMSPluginBase):
    """
    Displays a simple list of products relating to the indicated product_type.
    """
    cache = False
    model = ProductListPluginModel
    module = 'Products App'
    name = _('Product List')
    render_template = 'products/plugins/product_list.html'
    text_enabled = True

    def render(self, context, instance, placeholder):
        product_type = self.get_product_type(context, instance)
        if product_type is not None:
            products = product_type.products.all()
        else:
            products = Product.objects.all()
        context['instance'] = instance
        context['products'] = products
        return context

plugin_pool.register_plugin(ProductListPlugin)


class ProductTypePropertyPlugin(ProductTypeMixin, CMSPluginBase):
    cache = False
    model = ProductTypePropertyPluginModel
    module = 'Products App'
    name = _('Product Type Property')
    render_template = 'products/plugins/producttype_property.html'
    text_enabled = True

    def render(self, context, instance, placeholder):
        product_type = self.get_product_type(context, instance)
        if product_type is not None:
            property_value = getattr(product_type, instance.property_name, '')
        else:
            property_value = ''
        context['instance'] = instance
        context['product_type'] = product_type
        context['property_name'] = instance.property_name
        context['property_value'] = property_value
        return context

plugin_pool.register_plugin(ProductTypePropertyPlugin)


class ProductPropertyPlugin(ProductMixin, CMSPluginBase):
    cache = False
    model = ProductPropertyPluginModel
    module = 'Products App'
    name = _('Product Property')
    render_template = 'products/plugins/product_property.html'
    text_enabled = True

    def render(self, context, instance, placeholder):
        product = self.get_product(context, instance)
        if product:
            product_type = product.product_type
            context['product_type'] = product_type
        if product is not None:
            property_value = getattr(product, instance.property_name, '')
        else:
            property_value = ''
        context['instance'] = instance
        context['product'] = product
        context['property_name'] = instance.property_name
        context['property_value'] = property_value
        return context

plugin_pool.register_plugin(ProductPropertyPlugin)
