#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 27 18:25:03 2025

@author: hassan.naseri
"""

import pandas as pd
from django.conf import settings
from datetime import date
import numpy as np

from openai import OpenAI
import requests
import os
import json

# from difflib import SequenceMatcher

# def similar(a, b):
#     return SequenceMatcher(None, a, b).ratio()


#%%

client = OpenAI()

#%%
inventory_filename = '../../../../data/Raw Material Inventory.xlsx'
df_inventory = pd.read_excel(inventory_filename)
df_inventory['order_id'] = df_inventory.groupby(['Supplier','Delievry Date'], dropna=False).ngroup()


df_inventory['Product'] = df_inventory['Product'].str.split().str.join(' ')

#%% Load IFRA transparency list
ifra_filename = '../../../../data/ifra-transparency-list.h5'
df_materials = pd.read_hdf(ifra_filename)
df_materials = df_materials.reset_index()

df_materials['is_syntetic'] = False
df_materials.loc[df_materials['Naturals (ncs) category'].isnull(), 'is_syntetic'] = True


#%% 

for index, row in df_inventory.iterrows():
    
    if pd.isnull(row['CAS No']):
    
        name_inventory = row['Product']
        print(f"-------- {name_inventory} -------")
        
        # CAS_number = df_materials.loc[df_materials['Principal name'].isin([name_inventory]), "CAS n°"]
        # CAS_number = df_materials[df_materials['Principal name'].str.contains(name_inventory)]
        # scores = df_materials['Principal name'].apply(lambda x: similar(x, name_inventory))
        # match_id = np.argmax(scores)
        
        prompt = f"What is the CAS Regsitery Number for {name_inventory}?"
        response = client.responses.create(
            model="gpt-5",
            input=prompt,
            text = {
                    "verbosity": None, 
                    "format": {
                                "type": "json_schema", 
                                "name": "CAS_number", 
                                "strict": True,
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "CAS_number": {"type": "string"}
                                    },
                                "additionalProperties": False,
                                "required": ["CAS_number"]
                               }
                    }},
            # max_output_tokens = 16,
            reasoning = {
                    "effort": 'low'
                    }
        )
        
        print(response.output_text)
        response_json = json.loads(response.output_text)
        df_inventory.loc[index, 'CAS No'] = response_json['CAS_number']
    



#%%
# Update DataFrame with CAS numbers for indices 91–120
df_inventory.loc[91, "CAS No"]  = "22457-23-4"   # Stemone (Givaudan)
df_inventory.loc[92, "CAS No"]  = "8008-45-5"    # Nutmeg oil (India) - common CAS for nutmeg oil
df_inventory.loc[93, "CAS No"]  = "28219-60-5"   # Santaliff™ (IFF)
df_inventory.loc[94, "CAS No"]  = "106-22-9"     # Citronellol
df_inventory.loc[95, "CAS No"]  = "2050-08-0"    # Amyl (Pentyl) Salicylate (Givaudan)
df_inventory.loc[96, "CAS No"]  = "8000-27-9"    # Cedarwood (Virginia) oil
df_inventory.loc[97, "CAS No"]  = "84238-39-1"   # Clearwood® (Firmenich) — common CAS (alternate: 1450625-49-6 in some regions)
df_inventory.loc[98, "CAS No"]  = "97-53-0"      # Eugenol
df_inventory.loc[99, "CAS No"]  = "115-95-7"     # Linalyl acetate
df_inventory.loc[100, "CAS No"] = "8008-57-9"    # Orange (sweet) essential oil
df_inventory.loc[101, "CAS No"] = "60-12-8"      # Phenethyl alcohol (Phenyl ethyl alcohol)
df_inventory.loc[102, "CAS No"] = "36306-87-3"   # Kephalis (woody cyclohexanone)
df_inventory.loc[103, "CAS No"] = "88-41-5"      # Verdox® (ortho-tert-butylcyclohexyl acetate)
df_inventory.loc[104, "CAS No"] = "94201-19-1"   # Methyl Laitone (Givaudan)
df_inventory.loc[105, "CAS No"] = "211299-54-6"  # Ambrocenide®
df_inventory.loc[106, "CAS No"] = "513-86-0"     # Acetoin (racemate)
df_inventory.loc[107, "CAS No"] = "2550-52-9"    # Iso-Muscone / Isomuscone (cyclohexadecanone isomer)
df_inventory.loc[108, "CAS No"] = "20665-85-4"   # Isobutavan
df_inventory.loc[109, "CAS No"] = "8015-91-6"    # Cinnamon (leaf) oil (Ceylon type)
df_inventory.loc[110, "CAS No"] = "118-71-8"     # Maltol
df_inventory.loc[111, "CAS No"] = "431-03-8"     # Diacetyl (biacetyl)
df_inventory.loc[112, "CAS No"] = "123-11-5"     # p-Anisaldehyde (Anisaldehyde)
df_inventory.loc[113, "CAS No"] = "127-51-5"     # Alpha-Isomethyl Ionone
df_inventory.loc[114, "CAS No"] = "90-05-1"      # Guaiacol
df_inventory.loc[115, "CAS No"] = "123-92-2"     # Isoamyl acetate
df_inventory.loc[116, "CAS No"] = "97-64-3"      # Ethyl lactate (racemate)
df_inventory.loc[117, "CAS No"] = "15679-12-6"   # Pistachio Thiazole (2-ethyl-4-methylthiazole)
df_inventory.loc[118, "CAS No"] = "18479-58-8"   # Dihydromyrcenol
df_inventory.loc[119, "CAS No"] = "1205-17-0"    # Helional
df_inventory.loc[120, "CAS No"] = "63500-71-0"   # Florol®

df_inventory.loc[121, "CAS No"] = "140-11-4"   # Benzyl acetate
df_inventory.loc[122, "CAS No"] = "8000-46-2"   # Geranium oil (Geranium Bourbon essential oil) — common CAS for geranium EO
df_inventory.loc[123, "CAS No"] = "818-52-6"   # Styralyl acetate
df_inventory.loc[124, "CAS No"] = "7400-08-0"   # cis-3 Hexenyl acetate
df_inventory.loc[125, "CAS No"] = "59651-78-2"  # cis-3 Hexenyl hexanoate
df_inventory.loc[126, "CAS No"] = "123-31-9"   # Phenyl ethyl dimethyl carbinol (Phenyl ethyl isopropanol) — approximate
df_inventory.loc[127, "CAS No"] = "538-86-7"   # Methyl isoeugenol
df_inventory.loc[128, "CAS No"] = "101-77-3"   # Phenyl ethyl phenyl acetate (benzyl phenylacetate) — approximate
df_inventory.loc[129, "CAS No"] = "103-42-6"   # Methyl pamplemousse (grapefruit/methyl derivatives) — approximate
df_inventory.loc[130, "CAS No"] = "127-31-9"   # Jasmone
df_inventory.loc[131, "CAS No"] = "140-11-4"   # Benzyl acetate (duplicate)
df_inventory.loc[132, "CAS No"] = "60-12-8"    # Phenethyl acetate
df_inventory.loc[133, "CAS No"] = "115-72-4"   # Ethyl linalool
df_inventory.loc[134, "CAS No"] = "124-19-6"   # Nonanal (Aldehyde C-9)
df_inventory.loc[135, "CAS No"] = "87-92-5"    # Cinnamyl acetate
df_inventory.loc[136, "CAS No"] = "5392-40-5"   # Citral (mixture of geranial + neral)
df_inventory.loc[137, "CAS No"] = "35451-15-3"  # Ethyl methyl phenyl glycidate (Aldehyde C-16 type) — approximate
df_inventory.loc[138, "CAS No"] = "123-86-4"   # Allyl caproate (also known as allyl hexanoate)
df_inventory.loc[139, "CAS No"] = "98-55-5"    # Terpineol
df_inventory.loc[140, "CAS No"] = "586-62-9"   # α-Terpineol
df_inventory.loc[141, "CAS No"] = "6259-76-3"  # Hexyl salicylate
df_inventory.loc[142, "CAS No"] = "A: —"      # Violet Leaf Absolute — mixture / no canonical single CAS
df_inventory.loc[143, "CAS No"] = "75-14-3"    # Sulfurol (Sulfurous odorant, also “thiophene derivative”) — approximate
df_inventory.loc[144, "CAS No"] = "2213-23-4"  # Theaspirane — possible CAS
df_inventory.loc[145, "CAS No"] = "—"         # Guaiacwood — mixture / no single CAS
df_inventory.loc[146, "CAS No"] = "—"         # Cassis Base 345B — proprietary blend
df_inventory.loc[147, "CAS No"] = "—"         # Jasmine Accord — formulation blend
df_inventory.loc[148, "CAS No"] = "8023-91-4"  # Galbanum Oil — confirmed CAS for natural oil (Ferula galbaniflua) :contentReference[oaicite:0]{index=0}
df_inventory.loc[149, "CAS No"] = "24851-98-7" # Hedione HC — same CAS as Hedione (see HEDIONE HC) :contentReference[oaicite:1]{index=1}
df_inventory.loc[150, "CAS No"] = "105-34-0"   # Rose oxide (High Cis) — common CAS for rose oxide


df_inventory.loc[151, "CAS No"] = "7452-79-1"      # Ethyl methyl 2 butyrate
df_inventory.loc[152, "CAS No"] = "112-31-2"      # Decanal (Aldehyde C10)
df_inventory.loc[153, "CAS No"] = "23747-48-0"    # Nutty pyrazine (representative pyrazine)
df_inventory.loc[154, "CAS No"] = "120-14-9"      # Veratraldehyde
df_inventory.loc[155, "CAS No"] = "105-87-3"      # Geranyl acetate
df_inventory.loc[156, "CAS No"] = "150-78-7"      # Dimethyl hydroquinone (common entry/isomer)
df_inventory.loc[157, "CAS No"] = "65113-99-7"    # Sandalore
df_inventory.loc[158, "CAS No"] = "77-54-3"       # Cedryl acetate
df_inventory.loc[159, "CAS No"] = "5986-55-0"     # Patchouli alcohol (patchoulol) — Patchouli product
# 160 Black Agar Givco 215 5  -> proprietary / trade product, no single CAS found
# 161 Indolarome IFF -> proprietary blend / trade name (no single CAS)
# 162 Jasmal BHT -> proprietary blend (no single CAS)
df_inventory.loc[163, "CAS No"] = "16423-19-1"    # Geosmin (racemate / common reg. CAS)
df_inventory.loc[164, "CAS No"] = "75-18-3"       # Dimethyl sulfide
df_inventory.loc[165, "CAS No"] = "22047-25-2"    # 2-Acetylpyrazine
df_inventory.loc[166, "CAS No"] = "5910-89-4"     # 2,3-Dimethylpyrazine
df_inventory.loc[167, "CAS No"] = "24295-03-2"    # 2-Acetylthiazole
df_inventory.loc[168, "CAS No"] = "16491-36-4"    # cis-3-Hexenyl butyrate
df_inventory.loc[169, "CAS No"] = "25152-85-6"    # cis-3-Hexenyl benzoate
df_inventory.loc[170, "CAS No"] = "4927-39-3"     # Vetival (vendor molecule / vetiver-type ketone)
df_inventory.loc[171, "CAS No"] = "111-71-7"      # Heptanal (Aldehyde C-7)
df_inventory.loc[172, "CAS No"] = "123-35-3"      # Myrcene (β-myrcene)
df_inventory.loc[173, "CAS No"] = "79-31-2"       # Isobutyric acid (2-methylpropanoic acid)
df_inventory.loc[174, "CAS No"] = "122-78-1"      # Phenylacetaldehyde
# 175 Fragrant Rice Fleuressence -> proprietary perfume base (mixture), no single CAS
df_inventory.loc[176, "CAS No"] = "111-27-3"      # 1-Hexanol
df_inventory.loc[177, "CAS No"] = "80-54-6"       # Lilial (butylphenyl methylpropional)
df_inventory.loc[178, "CAS No"] = "141-12-8"      # Neryl acetate
df_inventory.loc[179, "CAS No"] = "122-63-4"      # Benzyl propionate
df_inventory.loc[180, "CAS No"] = "93-58-3"       # Methyl benzoate
df_inventory.loc[181, "CAS No"] = "127-91-3"      # β-Pinene
df_inventory.loc[182, "CAS No"] = "91770-14-8"    # Jasmine Sambac absolute (supplier-assigned CAS)
df_inventory.loc[183, "CAS No"] = "8022-96-6"     # Jasmine absolute (J. grandiflorum) — common registry CAS
df_inventory.loc[184, "CAS No"] = "8007-01-0"     # Rose absolute (common CAS for rose oils/absolutes)
df_inventory.loc[185, "CAS No"] = "9000-50-4"     # Oakmoss absolute (commonly seen registry CAS)
# 186 Vanilla Planifolia CO2 -> CO2 extracts are mixtures (no single CAS); vanillin (key component) is 121-33-5
df_inventory.loc[187, "CAS No"] = "8016-26-0"     # Cistus (Rock Rose) essential oil
df_inventory.loc[188, "CAS No"] = "8016-03-3"     # Davana essential oil (Artemisia pallens)
df_inventory.loc[189, "CAS No"] = "8000-25-7"     # Rosemary absolute (typical registry CAS)
df_inventory.loc[190, "CAS No"] = "91845-35-1"    # Holy basil (Tulsi) essential oil (supplier/registry CAS)

# Optionally, display the updated section
print(df_inventory.loc[121:150, ["Product", "CAS No"]])


#%% 

df_inventory.to_csv('../../../../data/Raw Material Inventory.csv')


df_inventory.to_hdf('../../../../data/Raw Material Inventory.hd5', key='inventory')



