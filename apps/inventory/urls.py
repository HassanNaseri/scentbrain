#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 15 23:14:08 2025

@author: hassan.naseri
"""

from django.urls import path

from . import views

urlpatterns = [
    # ex: /inventory/
    path("", views.index, name="index"),
    # ex: /inventory/5/products/
    path("<int:order_id>/products/", views.products, name="products"),
]


