# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.views.generic import DetailView, ListView

from .models import ProductType, Product


class ProductTypeListView(ListView):
    model = ProductType


class ProductTypeDetailView(DetailView):
    model = ProductType
    slug_url_kwarg = "product_type_slug"


class ProductDetailView(DetailView):
    model = Product
    slug_url_kwarg = "product_slug"

    def get_context_data(self, **kwargs):
        context = super(ProductDetailView, self).get_context_data(**kwargs)
        product = self.get_object()
        if product:
            context["product_type"] = product.product_type
        return context
