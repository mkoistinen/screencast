# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool

from .urls import urlpatterns


class ProductsApphook(CMSApp):
    name = "Products"
    urls = [urlpatterns, ]
    app_name = "products"

apphook_pool.register(ProductsApphook)
