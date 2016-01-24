# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.contrib import admin

from .models import ProductType, Product, Layout


class LayoutAdmin(admin.ModelAdmin):
    pass

admin.site.register(Layout, LayoutAdmin)


class ProductTypeAdmin(admin.ModelAdmin):
    pass

admin.site.register(ProductType, ProductTypeAdmin)


class ProductAdmin(admin.ModelAdmin):
    pass

admin.site.register(Product, ProductAdmin)
