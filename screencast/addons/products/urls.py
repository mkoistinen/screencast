# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.conf.urls import patterns, url

from .views import (
    ProductTypeListView,
    ProductTypeDetailView,
    ProductDetailView,
)


urlpatterns = patterns(
    '',

    # [app-root]/
    # ------------------------------------
    url(r'^$', ProductTypeListView.as_view(), name='product_type_list'),

    # [app-root]/[product-type]/
    # ------------------------------------
    url(r'^(?P<product_type_slug>\w[-\w]+)/$', ProductTypeDetailView.as_view(),
        name='product_type_detail'),

    # [app-root]/[product-type]/[product]/
    # ------------------------------------
    url(r'^(?P<product_type_slug>\w[-\w]+)/(?P<product_slug>\w[-\w]+)/$',
        ProductDetailView.as_view(), name='product_detail'),)
