#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep 14 23:39:49 2025

@author: hassan.naseri
"""

import pandas as pd
import requests
import io


# filename = "data/ifra-transparency-list.txt"
# df = pd.read_csv(filename, sep='\t')


header = {
  "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36",
  "X-Requested-With": "XMLHttpRequest"
}

# for page_num in range(1,155):

# df_all = pd.DataFrame()
# for page_num in range(1,155):
#     url = f'https://ifrafragrance.org/transparency-list?page={page_num}'
#     print(url)
#     req = requests.get(url, headers=header)
#     html = io.StringIO(req.text)
    
#     all_tables = pd.read_html(
#         html,
#         match="Principal name"
#     )
#     df = all_tables[0]
#     df_all = pd.concat([df_all, df])
    

#%%

with pd.ExcelWriter('ifra-transparency-list.xlsx') as writer:
    df_all.to_excel(writer)
    
#%%
store = pd.HDFStore('ifra-transparency-list.h5')
store['df'] = df_all  