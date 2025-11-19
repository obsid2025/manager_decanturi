# -*- coding: utf-8 -*-
"""
Test extragere bonuri de producție AGREGATE (grupate pe SKU cu cantități)
"""
import pandas as pd
import re
import sys
from collections import defaultdict

sys.stdout.reconfigure(encoding='utf-8')

# Citire fișier
df = pd.read_excel('45.xlsx')

# Filtrare comenzi finalizate
df_finalizate = df[df['Status Comanda'] == 'Comanda Finalizata (Facturata)']

print(f'COMENZI FINALIZATE: {len(df_finalizate)}\n')
print('='*100)

# Agregare bonuri pe SKU
bonuri_agregate = defaultdict(lambda: {'nume': '', 'cantitate': 0, 'comenzi': []})

for idx, row in df_finalizate.iterrows():
    produse_text = str(row['Produse comandate'])
    atribute_text = str(row['Atributele produselor comandate'])

    # Split produse
    produse = produse_text.split(' | ')

    # Extrage SKU-uri din atribute
    sku_matches = re.findall(r'([^,\s]+):\s*\(', atribute_text)

    # Match produse cu SKU-uri
    for i, produs in enumerate(produse):
        produs = produs.strip()

        # Doar decanturi
        if 'Decant' not in produs:
            continue

        # Extrage cantitatea din produs
        match_cantitate = re.search(r'(\d+\.\d+)$', produs)
        cantitate = int(float(match_cantitate.group(1))) if match_cantitate else 1

        # SKU pentru acest produs
        sku = sku_matches[i] if i < len(sku_matches) else 'N/A'

        # Extrage numele parfumului
        match_parfum = re.search(r'Decant (\d+) ml parfum (.+?),', produs)
        if match_parfum:
            ml = match_parfum.group(1)
            nume_parfum = match_parfum.group(2)
            nume_complet = f"Decant {ml}ml {nume_parfum}"
        else:
            nume_complet = produs[:60]

        # Agregare
        bonuri_agregate[sku]['nume'] = nume_complet
        bonuri_agregate[sku]['cantitate'] += cantitate
        bonuri_agregate[sku]['comenzi'].append(row['Numar Comanda'])

# Sortare după cantitate (descrescător)
bonuri_sortate = sorted(bonuri_agregate.items(), key=lambda x: x[1]['cantitate'], reverse=True)

print('\n=== BONURI DE PRODUCTIE AGREGATE (pe SKU) ===\n')
print(f'{"SKU":<20} {"Cantitate":>10} {"Nume Produs":<50} {"Comenzi"}')
print('='*120)

for sku, info in bonuri_sortate:
    comenzi_unice = list(set(info['comenzi']))[:5]
    comenzi_str = ', '.join([f"#{c}" for c in comenzi_unice])
    if len(set(info['comenzi'])) > 5:
        comenzi_str += '...'
    print(f'{sku:<20} {info["cantitate"]:>10} {info["nume"]:<50} {comenzi_str}')

print('='*120)
print(f'\nTOTAL BONURI DE CREAT: {len(bonuri_agregate)}')
print(f'TOTAL BUCATI (toate cantitatile): {sum(b["cantitate"] for b in bonuri_agregate.values())}')
print('='*120)
