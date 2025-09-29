#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
from django.conf import settings
from datetime import date
import numpy as np
from django.core.management.base import BaseCommand
from materials.models import Material, IFRA_NCS_Letter, IFRA_NCS_Number


#%% Load IFRA transparency list
# filename = '../../../../data/ifra-transparency-list.h5'
filename = settings.BASE_DIR / 'data/ifra-transparency-list.h5'

df_materials = pd.read_hdf(filename)
df_materials['is_syntetic'] = False
df_materials.loc[df_materials['Naturals (ncs) category'].isnull(), 'is_syntetic'] = True

#%% Insert IFRA transparency list

class Command(BaseCommand):
    def handle(self, **options):  
              
        # Inserting materials
        Material_list = [
            Material(
                CAS = row['CAS n°'],
                name = row['Principal name'],
                is_syntetic = row['is_syntetic'],
                IFRA_NCS_category = row['Naturals (ncs) category'],
                synonyms = ""
            )
            for idx, row in df_materials.iterrows()
        ]
        
        Material.objects.bulk_create(Material_list)
        
        self.stdout.write(self.style.SUCCESS('Successfully loaded all IFRA materials.'))
     
        
#%% Load IFRA CAS categories

NCS_letter_data = [
    ("A", "Root", "Angelica root oil", ""),
    ("B", "Moss", "Oakmoss extract", ""),
    ("C", "Bark", "Cinnamon bark oil", ""),
    ("D", "Wood", "Sandalwood oil", ""),
    ("E", "Leaf/Twig", "Petitgrain oil, Peppermint oil",
     "Leaves, twigs or stems are the main target of the harvest but may include other aerial parts"),
    ("F", "Flower", "Rose petals oil", "Where the flower is the main target of the harvest"),
    ("G", "Fruit", "Orange peel oil", ""),
    ("H", "Seed or grain", "Coriander seed oil", ""),
    ("I", "Algae", "Seaweed absolute", ""),
    ("J", "Animal by-products", "Beeswax absolute", ""),
    ("K", "Exudate", "Olibanum oil", ""),
    ("L", "Twig", "Clove stem oil", ""),
    ("M", "Multiple", "Fusel oil", "Could be obtained from grain, grape, rice, etc."),
]

df_NCS_letter = pd.DataFrame(NCS_letter_data, columns=["code", "description", "example", "comments"])


NCS_number_data = [
    ("2.1", "Absolute", ""),
    ("2.1.1", "Extract of absolute", ""),
    ("2.1.2", "Absolute (x-less)", ""),
    ("2.2", "Alcoholate", ""),
    ("2.3", "Aromatic water", ""),
    ("2.4", "Balsam", ""),
    ("2.5", "Essential oil by cold expression", ""),
    ("2.6", "Folded essential oil", ""),
    ("2.7", "Concrete", ""),
    ("2.7.1", "By-product of concrete (which can be further processed)", ""),
    ("2.8", "Distillate generic", ""),
    ("2.9", "Dry-distilled oil", "Cade oil"),
    ("2.9.1", "Dry-distilled pyrogenated oil", ""),
    ("2.9.2", "Dry-distilled pyrogenated oil, purified by steam distillation", ""),
    ("2.10", "Essential essence oil (from fruit juice)", ""),
    ("2.11", "Essential oil generic", ""),
    ("2.12", "Essential oil by steam distillation", "Lavender oils"),
    ("2.12.1", "Essential oil obtained by steam distillation first grade", "Ylang oils"),
    ("2.12.2", "Essential oil obtained by steam distillation second grade", "Ylang oils"),
    ("2.12.3", "Essential oil obtained by steam distillation third grade", "Ylang oils"),
    ("2.12 X", "Essential oil obtained by steam distillation Extra grade", "Ylang oils"),
    ("2.12 XS", "Essential oil obtained by steam distillation Extra Super grade", "Ylang oils"),
    ("2.13", "Extract generic", ""),
    ("2.14", "Exudate (not gums and balsams)", ""),
    ("2.15", "Gum", ""),
    ("2.16", "Gum oleoresin", ""),
    ("2.16.1", "Gum oleoresin rectified", "turpentine stump oil"),
    ("2.17", "Gum resin", ""),
    ("2.18", "Natural oleoresin exudate", ""),
    ("2.19", "Natural raw material (includes fermentation)", ""),
    ("2.20", "Non-concentrated extract", "Asafoetida in peanut oil, benzoin in ethanol"),
    ("2.21", "Oleoresin (derived)", ""),
    ("2.22", "Pomade", ""),
    ("2.23", "Post treated", "decolorized essential oil, washed essential oil, iron eliminated essential oil"),
    ("2.24", "Rectified essential oil", ""),
    ("2.25", "Resin", ""),
    ("2.26", "Resinoid", ""),
    ("2.27", "Supercritical extract", ""),
    ("2.28", "“Terpene-less and sesquiterpene-less” essential oil", ""),
    ("2.29", "“Terpene-less” essential oil", ""),
    ("2.30", "Terpenes", ""),
    ("2.31", "Tincture and infusions", ""),
    ("2.32", "Volatile concentrate", "orange essence 5 fold"),
    ("2.33", "“x-less” essential oil", "partly dementholised"),
    ("2.50", "Fixed oil by cold expression", ""),
    ("2.51", "Essential oils obtained with significant changes in their composition", ""),
    ("2.52", "Extract obtained by ultrasonic extraction", ""),
    ("2.53", "Extract obtained by microwave extraction", ""),
    ("2.54", "Solvent extraction of distillation water", ""),
    ("2.55", "Chemically-modified essential oil", ""),
    ("2.56", "Terpeneless extraction from fruit juice", "orange essence oil terpeneless"),
    ("2.57", "Native aromatic water", "Strawberry native aromatic water, cornmint native aromatic water"),
]

df_NCS_number = pd.DataFrame(NCS_number_data, columns=["code", "description", "example"])


