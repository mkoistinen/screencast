# -*- coding: utf-8 -*-

from __future__ import unicode_literals

try:
    from urllib import urlencode
except ImportError:  # pragma: no cover
    from urllib.parse import urlencode

from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from cms.toolbar_base import CMSToolbar
from cms.toolbar_pool import toolbar_pool
from cms.utils.urlutils import admin_reverse

from .models import ProductType, Product


def get_admin_url(action, action_args=[], **url_args):
    """
    Convenience method for constructing admin-urls with GET parameters.
    """
    base_url = admin_reverse(action, args=action_args)
    url_args_tuple = sorted([(k, v) for k, v in url_args.items()])
    params = urlencode(url_args_tuple)
    if params:
        return "?".join([base_url, params])
    else:
        return base_url


@toolbar_pool.register
class ProductsToolbar(CMSToolbar):
    watch_models = [Product, ProductType, ]
    supported_apps = ('products',)

    def get_on_delete_redirect_url(self, object):
        if hasattr(object, "product_type"):
            url = reverse(
                'products:product_type_detail',
                kwargs={"product_type_slug": object.product_type.slug}
            )
        else:
            url = reverse('products:product_type_list')
        return url

    def is_app(self, request):
        if request and request.app_name:
            return request.app_name in self.supported_apps

    def get_view_object(self, request, model=None, slug_field="slug",
                        slug_url_kwarg=None):
        if model and slug_url_kwarg:
            queryset = model.objects
            if request and request.resolver_match:
                kwargs = request.resolver_match.kwargs
                slug = kwargs.get(slug_url_kwarg, None)
                if slug is not None:
                    queryset = queryset.filter(**{slug_field: slug})
                    return queryset.first()
            return queryset.none()
        return None

    def get_product(self, request):
        return self.get_view_object(
            request, model=Product, slug_url_kwarg="product_slug")

    def get_product_type(self, request):
        return self.get_view_object(
            request, model=ProductType, slug_url_kwarg="product_type_slug")

    def populate(self):
        user = getattr(self.request, 'user', None)

        try:
            view_name = self.request.resolver_match.view_name
        except AttributeError:
            view_name = None

        if user and view_name:
            try:
                app_name = self.request.resolver_match.app_name
            except AttributeError:
                app_name = None
            if app_name != "products":
                return

            product = self.get_product(self.request)
            product_type = self.get_product_type(self.request)
            menu = self.toolbar.get_or_create_menu("products-app", "Products")

            change_product_perm = user.has_perm('products.change_product')
            add_product_perm = user.has_perm('products.add_product')
            delete_product_perm = user.has_perm('products.delete_product')
            product_perms = [change_product_perm, add_product_perm,
                             delete_product_perm]

            change_product_type_perm = user.has_perm(
                'products.change_producttype')
            add_product_type_perm = user.has_perm('products.add_producttype')
            delete_product_type_perm = user.has_perm(
                'products.delete_producttype')
            product_type_perms = [change_product_type_perm,
                                  add_product_type_perm,
                                  delete_product_type_perm]

            if add_product_type_perm:
                url_args = {}
                url = get_admin_url('products_producttype_add', **url_args)
                menu.add_modal_item(_('Add new product type'), url=url)

            if change_product_type_perm and product_type:
                url_args = {}
                url = get_admin_url('products_producttype_change',
                                    [product_type.pk, ], **url_args)
                menu.add_modal_item(_('Edit {0}'.format(product_type.name)),
                                    url=url, active=True)

            if delete_product_type_perm and product_type:
                redirect_url = self.get_on_delete_redirect_url(product_type)
                url = get_admin_url('products_producttype_delete',
                                    [product_type.pk, ])
                menu.add_modal_item(_('Delete {0}'.format(product_type.name)),
                                    url=url, on_close=redirect_url)

            if any(product_perms) and any(product_type_perms):
                menu.add_break()

            if add_product_perm:
                url_args = {}
                if product_type:
                    url_args.update({"product_type": product_type.pk})
                if product:
                    url_args.update({"product_type": product.product_type.pk})
                url = get_admin_url('products_product_add', **url_args)
                menu.add_modal_item(_('Add new product'), url=url)

            if change_product_perm and product:
                url_args = {}
                url = get_admin_url('products_product_change',
                                    [product.pk, ], **url_args)
                menu.add_modal_item(_('Edit {0}'.format(product.name)),
                                    url=url, active=True)

            if delete_product_perm and product:
                redirect_url = self.get_on_delete_redirect_url(product)
                url = get_admin_url('products_product_delete',
                                    [product.pk, ])
                menu.add_modal_item(_('Delete {0}'.format(product.name)),
                                    url=url, on_close=redirect_url)
