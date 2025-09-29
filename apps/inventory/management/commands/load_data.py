#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 16 11:42:23 2025

@author: hassan.naseri
"""

import pandas as pd
from django.conf import settings
from datetime import date
import numpy as np

filename = settings.BASE_DIR / 'data/Raw Material Inventory.xlsx'
df_inventory = pd.read_excel(filename)

#%%
df_inventory['order_id'] = df_inventory.groupby(['Supplier','Delievry Date'], dropna=False).ngroup()
df_orders = df_inventory.drop_duplicates('order_id')[['order_id','Supplier','Delievry Date']]
df_orders = df_orders.set_index('order_id').sort_index()
df_orders.replace({np.nan: None}, inplace = True)

#%%
from django.core.management.base import BaseCommand
from inventory.models import Order, Product


class Command(BaseCommand):
    def handle(self, **options):  
        
        # Creating invoices
        Order_list = [
            Order(
                supplier = row['Supplier'],
                delivery_date = row['Delievry Date']
                )
            for idx, row in df_orders.iterrows()
            ]
        Order.objects.bulk_create(Order_list)
        
        self.stdout.write(self.style.SUCCESS('Successfully imported orders.'))
        
        # Inserting invoice items
        Product_list = [
            Product(
                order = Order_list[row['order_id']],
                code = row['Code'],
                CAS = row['CAS No'],
                name = row['Product'],
                manufacturer = '',
                dilution = row['Dilution'],
                solvent = '',
                quantity = row['Quantity'],
                quantity_unit = row['Unit'],
                unit_price = row['Unit Price'],
                price = row['Price'],
                currency = row['Currency'],
                comments = '',
                test_by_date = date.today() 
            )
            for idx, row in df_inventory.iterrows()
        ]
        Product.objects.bulk_create(Product_list)
        
        self.stdout.write(self.style.SUCCESS('Successfully loaded all inventory items.'))
