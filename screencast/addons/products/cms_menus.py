# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from cms.menu_bases import CMSAttachMenu

from menus.base import NavigationNode
from menus.menu_pool import menu_pool

from .models import ProductType


class ProductsMenu(CMSAttachMenu):
    name = _('Products Menu')

    def get_nodes(self, request):
        nodes = []
        product_type_node_start = 1000000

        for product_type in ProductType.objects.all():
            product_type_node = NavigationNode(
                product_type.name,
                product_type.get_absolute_url(),
                product_type.pk + product_type_node_start,
            )
            nodes.append(product_type_node)

            for product in product_type.products.all():
                product_node = NavigationNode(
                    product.name,
                    product.get_absolute_url(),
                    product.pk,
                    product_type.pk + product_type_node_start,
                )
                nodes.append(product_node)

        return nodes

menu_pool.register_menu(ProductsMenu)
