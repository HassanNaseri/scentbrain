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

# Update df_inventory CAS numbers for indices 191-220
df_inventory.loc[191, "CAS No"] = "84696-51-5"   # Spearmint Absolute (Mentha spicata extract)
df_inventory.loc[192, "CAS No"] = "8006-76-6"    # Magnolia Leaf Oil
df_inventory.loc[193, "CAS No"] = "8002-68-4"    # Juniper Berry Oil (use for Juniper CO2 if no supplier CAS)
df_inventory.loc[194, "CAS No"] = "8000-46-2"    # Geranium (Rose Geranium) Oil
df_inventory.loc[195, "CAS No"] = "8023-99-2"    # Pine Absolute (Scotch pine absolute)
df_inventory.loc[196, "CAS No"] = "68916-73-4"   # Black Tea CO2 (supplier Robertet / product CAS)
df_inventory.loc[197, "CAS No"] = "84650-60-2"   # Green Tea CO2 extract (common registry CAS)
df_inventory.loc[198, "CAS No"] = "68991-25-3"   # Cedrat (Citrus medica) / cedrat peel oil
df_inventory.loc[199, "CAS No"] = ""            # Butter CO2 (SELECT) — CO2 extracts often have no single CAS (leave supplier-specific)
df_inventory.loc[200, "CAS No"] = "8014-13-9"    # Cumin Seed Oil
df_inventory.loc[201, "CAS No"] = "8014-09-3"    # Patchouli Oil (Patchouli Essential Oil LIGHT)
df_inventory.loc[202, "CAS No"] = ""            # Jasmophore (Firmenich) — proprietary accord, no single CAS
df_inventory.loc[203, "CAS No"] = "51608-18-5"   # Jasminone B (Jasminone B N° 497)
df_inventory.loc[204, "CAS No"] = "23696-85-7"   # Damascenone Total
df_inventory.loc[205, "CAS No"] = "16251-77-7"   # Trifernal® (Firmenich)
df_inventory.loc[206, "CAS No"] = "1125-21-9"    # 4-Oxoisophorone
df_inventory.loc[207, "CAS No"] = "93-92-5"      # Styrallyl Acetate
df_inventory.loc[208, "CAS No"] = "24851-98-7"   # Hedione (Methyl dihydrojasmonate)
df_inventory.loc[209, "CAS No"] = "68916-26-7"   # Civet Absolute (natural civet absolute CAS)
df_inventory.loc[210, "CAS No"] = ""            # Tuberose “Signature” Absolute — supplier-specific (absolutes have various CAS)
df_inventory.loc[211, "CAS No"] = "8031-03-6"    # Mimosa Absolute
df_inventory.loc[212, "CAS No"] = "8007-47-4"    # Fir Balsam Absolute
df_inventory.loc[213, "CAS No"] = "8000-66-6"    # Cardamom Seed Oil (Elettaria cardamomum oil)
df_inventory.loc[214, "CAS No"] = "8021-36-1"    # Opoponax (Opopanax) Resinoid
df_inventory.loc[215, "CAS No"] = "89-88-3"      # Vetiverol (Vetiverol ex Vetiver Haiti) — vendor/SDS-listed CAS
df_inventory.loc[216, "CAS No"] = "8006-77-7"    # Pimento / Pimento (Allspice) Berry Oil
df_inventory.loc[217, "CAS No"] = "8000-28-0"    # Lavender oil (general Lavender CAS; specific cultivars may differ)
df_inventory.loc[218, "CAS No"] = "8022-91-1"    # Ho Wood (Cinnamomum camphora linalooliferum) Oil
df_inventory.loc[219, "CAS No"] = "121-33-5"     # Vanillin (vanillin ex clove — dominant component CAS)
df_inventory.loc[220, "CAS No"] = "140-11-4"     # Benzyl Acetate

df_inventory.loc[221, "CAS No"] = ""             # Paradisamide (Givaudan) - proprietary, no public CAS
df_inventory.loc[222, "CAS No"] = "142-92-7"     # Hexyl acetate
df_inventory.loc[223, "CAS No"] = "54464-57-2"   # Iso E Super / Timbersilk
df_inventory.loc[224, "CAS No"] = "8030-97-5"    # Cocoa Absolute
df_inventory.loc[225, "CAS No"] = "8023-85-6"    # Cedarwood Atlas Absolute
df_inventory.loc[226, "CAS No"] = "88-41-5"      # Vertofix (methyl cedryl ketone)
df_inventory.loc[227, "CAS No"] = "28219-61-6"   # Bacdanol
df_inventory.loc[228, "CAS No"] = "79-69-6"      # Alpha-Irone
df_inventory.loc[229, "CAS No"] = ""             # Jonquille Absolute - mixture, no unique CAS
df_inventory.loc[230, "CAS No"] = ""             # Paradise Molecule® - proprietary, no public CAS
df_inventory.loc[231, "CAS No"] = "8024-16-8"    # Orris Absolute
df_inventory.loc[232, "CAS No"] = ""             # Tubereuse 184018 - proprietary base, no CAS
df_inventory.loc[233, "CAS No"] = "502-61-4"     # Alpha-Farnesene
df_inventory.loc[234, "CAS No"] = "111-12-6"     # Methyl Heptine Carbonate
df_inventory.loc[235, "CAS No"] = "101-94-0"     # Para Cresyl Caprylate
df_inventory.loc[236, "CAS No"] = "101-67-7"     # Para Cresyl Phenyl Acetate
df_inventory.loc[237, "CAS No"] = "24851-98-7"   # Hedione High Cis (Methyl dihydrojasmonate)
df_inventory.loc[238, "CAS No"] = "106-25-2"     # Nerol
df_inventory.loc[239, "CAS No"] = "120-51-4"     # Benzyl Benzoate
df_inventory.loc[240, "CAS No"] = "93-19-6"      # Isobutyl Quinoline
df_inventory.loc[241, "CAS No"] = "101-86-0"     # Hexyl Cinnamic Aldehyde (Lyral-type substitute)
df_inventory.loc[242, "CAS No"] = "100-51-6"     # Benzyl Alcohol
df_inventory.loc[243, "CAS No"] = "24851-98-7"   # Hedione (Methyl dihydrojasmonate)
df_inventory.loc[244, "CAS No"] = ""             # Cascalone® - proprietary (Firmenich), no public CAS
df_inventory.loc[245, "CAS No"] = ""             # Rum CO2 - extract, no universal CAS
df_inventory.loc[246, "CAS No"] = "15356-74-8"   # Dihydroactinidiolide
df_inventory.loc[247, "CAS No"] = ""             # Compound Black® - proprietary, no CAS
df_inventory.loc[248, "CAS No"] = "8016-38-4"    # Neroli Oil (Morocco)
df_inventory.loc[249, "CAS No"] = ""             # Pineapple Supreme - proprietary base, no CAS
df_inventory.loc[250, "CAS No"] = "1195-79-5"    # Alpha-Fenchone

df_inventory.loc[251, "CAS No"] = ""             # Elderflower TruAbs® - proprietary accord
df_inventory.loc[252, "CAS No"] = "68916-99-4"   # Osmanthus Absolute (flowers)
df_inventory.loc[253, "CAS No"] = "8007-08-7"    # Ginger Oil
df_inventory.loc[254, "CAS No"] = ""             # Cascalone® - proprietary (Firmenich)
df_inventory.loc[255, "CAS No"] = "8046-22-8"    # Tonka Bean Absolute
df_inventory.loc[256, "CAS No"] = "106-02-5"     # Exaltolide® (15-pentadecanolide)
df_inventory.loc[257, "CAS No"] = ""             # Z11™ - proprietary material (IFF)
df_inventory.loc[258, "CAS No"] = "141773-73-1"  # Helvetolide®
df_inventory.loc[259, "CAS No"] = "118-58-1"     # Maple Lactone (Methyl cyclopentenolone)
df_inventory.loc[260, "CAS No"] = "71077-29-9"   # Milk Lactone (gamma-Decenoic lactone)
df_inventory.loc[261, "CAS No"] = "557-48-2"     # trans-2,cis-6-Nonadienal
df_inventory.loc[262, "CAS No"] = "141773-73-1"  # Edenolide (same CAS family as Helvetolide-type musks)
df_inventory.loc[263, "CAS No"] = "56177-11-4"   # Labdamate
df_inventory.loc[264, "CAS No"] = ""             # Trimofix® - proprietary (IFF)
df_inventory.loc[265, "CAS No"] = "110-41-8"     # Aldehyde C-12 MNA (2-methylundecanal)
df_inventory.loc[266, "CAS No"] = ""             # Solgard® (E) - proprietary
df_inventory.loc[267, "CAS No"] = "93-29-8"      # Isoeugenyl Acetate
df_inventory.loc[268, "CAS No"] = "68039-49-6"   # Triplal
df_inventory.loc[269, "CAS No"] = "106-72-9"     # Melonal
df_inventory.loc[270, "CAS No"] = "104-93-8"     # Phenoxanol® (Phenoxyethanol base)
df_inventory.loc[271, "CAS No"] = "16409-43-1"   # Neobutenone® Alpha
df_inventory.loc[272, "CAS No"] = ""             # Floralozone® - proprietary (IFF)
df_inventory.loc[273, "CAS No"] = "105-54-4"     # Ethyl Butyrate
df_inventory.loc[274, "CAS No"] = "141773-73-1"  # Helvetolide® (repeat)
df_inventory.loc[275, "CAS No"] = "67746-30-9"   # Manzanate (cis-3-hexenyl 2-methylbutyrate)
df_inventory.loc[276, "CAS No"] = "65405-77-8"   # cis-3-Hexenyl Salicylate
df_inventory.loc[277, "CAS No"] = "16423-19-1"   # Geosmin
df_inventory.loc[278, "CAS No"] = "698-76-0"     # Methyl Laitone (gamma-Undecalactone methyl ether)
df_inventory.loc[279, "CAS No"] = "141-78-6"     # Ethyl Acetate
df_inventory.loc[280, "CAS No"] = "32388-55-9"   # Cedramber
df_inventory.loc[281, "CAS No"] = "103-95-7"     # Cyclamen Aldehyde
df_inventory.loc[282, "CAS No"] = ""             # Globanone® - proprietary (IFF woody ketone)
df_inventory.loc[283, "CAS No"] = "103-26-4"     # Methyl Cinnamate
df_inventory.loc[284, "CAS No"] = "3658-77-3"    # Strawberry Furanone (Furaneol)
df_inventory.loc[285, "CAS No"] = ""             # Pharaone - proprietary
df_inventory.loc[286, "CAS No"] = "8023-91-4"    # Galbanum Resinoid
df_inventory.loc[287, "CAS No"] = "2705-87-5"    # Allyl Cyclohexyl Propionate
df_inventory.loc[288, "CAS No"] = ""             # Fleuramone - proprietary
df_inventory.loc[289, "CAS No"] = "36653-82-4"   # Cetanol (Cetyl Alcohol)
df_inventory.loc[290, "CAS No"] = ""             # Koavone - proprietary
df_inventory.loc[291, "CAS No"] = "8023-91-4"    # Galbanum Resinoid (same as 286)
df_inventory.loc[292, "CAS No"] = ""             # Maritima - proprietary (IFF/Firmenich base)
df_inventory.loc[293, "CAS No"] = "79-76-5"      # alpha-Damascone
df_inventory.loc[294, "CAS No"] = "198404-98-7"  # Javanol

df_inventory.loc[160, "CAS No"] = ""             # Black Agar Givco 215/2 (mixture / proprietary)
df_inventory.loc[161, "CAS No"] = "18096-62-3"   # Indolarome (IFF)
df_inventory.loc[162, "CAS No"] = ""             # Jasmal BHT (proprietary mix; contains BHT 128-37-0 as stabilizer)
df_inventory.loc[175, "CAS No"] = ""             # Fragrant Rice Fleuressence (mixture)
df_inventory.loc[186, "CAS No"] = "8024-06-4"    # Vanilla planifolia CO2 (absolute/CO2 extract registry CAS)
df_inventory.loc[199, "CAS No"] = "91745-88-9"   # Butter CO2 (common supplier CAS for butter CO2 extracts)
df_inventory.loc[202, "CAS No"] = ""             # Jasmophore (Firmenich) - proprietary (no public CAS)
df_inventory.loc[210, "CAS No"] = "8024-05-03"   # Tuberose absolute (generic absolute CAS)
df_inventory.loc[221, "CAS No"] = ""             # Paradisamide (Givaudan) - proprietary molecule
df_inventory.loc[229, "CAS No"] = "8023-75-4"    # Jonquille (Narcissus jonquilla) absolute
df_inventory.loc[230, "CAS No"] = ""             # Paradise Molecule® - proprietary blend
df_inventory.loc[232, "CAS No"] = ""             # Tubereuse 184018 (proprietary base)
df_inventory.loc[244, "CAS No"] = "950919-28-5"  # Cascalone® (Firmenich)
df_inventory.loc[245, "CAS No"] = ""             # Rum CO2 (CO2 extract - supplier-specific)
df_inventory.loc[247, "CAS No"] = ""             # Compound Black® - proprietary
df_inventory.loc[249, "CAS No"] = ""             # Pineapple Supreme - proprietary
df_inventory.loc[251, "CAS No"] = ""             # Elderflower TruAbs® - proprietary
df_inventory.loc[254, "CAS No"] = "950919-28-5"  # Cascalone® (duplicate entry)
df_inventory.loc[257, "CAS No"] = ""             # Z11™ - proprietary
df_inventory.loc[264, "CAS No"] = ""             # Trimofix® - proprietary
df_inventory.loc[266, "CAS No"] = ""             # Solgard® (E) - proprietary
df_inventory.loc[272, "CAS No"] = ""             # Floralozone® - proprietary
df_inventory.loc[282, "CAS No"] = "3100-36-5"    # Globanone® (registered CAS for globanone)
df_inventory.loc[285, "CAS No"] = "313973-37-4"  # Pharaone® (product CAS as listed for Pharaone 10% in DPG)
df_inventory.loc[288, "CAS No"] = "137-03-1"     # Fleuramone (projasmone / 2-heptylcyclopentan-1-one)
df_inventory.loc[290, "CAS No"] = "81786-75-6"   # Koavone (IFF – one commonly cited CAS for product)
df_inventory.loc[292, "CAS No"] = "38462-23-6"   # Maritima (IFF)


#%% 

df_inventory.to_csv('../../../../data/Raw Material Inventory.csv')


df_inventory.to_hdf('../../../../data/Raw Material Inventory.hd5', key='inventory')



