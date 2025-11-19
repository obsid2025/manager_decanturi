# -*- coding: utf-8 -*-
import pandas as pd
import sys

sys.stdout.reconfigure(encoding='utf-8')

df = pd.read_excel('45.xlsx')

toate_produse_list = []
for produse_str in df['Produse comandate'].dropna():
    produse_list = str(produse_str).split(' | ')
    toate_produse_list.extend(produse_list)

produse_yara_moi = [p for p in toate_produse_list if 'Yara Moi' in p]

print(f'Găsit {len(produse_yara_moi)} produse cu "Yara Moi":')
for p in set(produse_yara_moi):
    count = produse_yara_moi.count(p)
    print(f'  {count}x - {p}')
