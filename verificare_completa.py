# -*- coding: utf-8 -*-
import pandas as pd
import re
from collections import defaultdict
import sys

sys.stdout.reconfigure(encoding='utf-8')

def extrageInfoProdus(text_produs):
    if 'Decant' not in text_produs:
        return None
    match_ml = re.search(r'Decant (\d+) ml parfum (.+?),', text_produs)
    if not match_ml:
        return None
    cantitate_ml = int(match_ml.group(1))
    nume_parfum = match_ml.group(2).strip()
    match_bucati = re.search(r'(\d+\.\d+)$', text_produs.strip())
    if match_bucati:
        numar_bucati = float(match_bucati.group(1))
    else:
        numar_bucati = 1.0
    return (nume_parfum, cantitate_ml, int(numar_bucati))

# Citire fișier
df = pd.read_excel('45.xlsx')
df_finalizate = df[df['Status Comanda'] == 'Comanda Finalizata (Facturata)']

print(f'COMENZI FINALIZATE: {len(df_finalizate)}')
print('\n' + '='*100)

# Procesare comenzi
raport = defaultdict(int)
total_produse_procesate = 0
total_decanturi_procesate = 0

for idx, row in df_finalizate.iterrows():
    print(f"\nComanda #{row['Numar Comanda']}:")
    produse_text = str(row['Produse comandate'])
    produse = produse_text.split(' | ')

    print(f"  Total produse în comandă: {len(produse)}")

    for produs in produse:
        produs = produs.strip()
        print(f"  - Procesare: {produs[:80]}...")

        info = extrageInfoProdus(produs)
        if info:
            nume_parfum, cantitate_ml, numar_bucati = info
            raport[(nume_parfum, cantitate_ml)] += numar_bucati
            total_decanturi_procesate += 1
            print(f"    ✓ Adăugat: {nume_parfum} {cantitate_ml}ml x{numar_bucati}")
        else:
            print(f"    ⚠ IGNORAT (nu e decant)")

        total_produse_procesate += 1

print('\n' + '='*100)
print('RAPORT FINAL:')
print('='*100)

for (nume_parfum, cantitate_ml), bucati in sorted(raport.items()):
    print(f'{nume_parfum:50s} {cantitate_ml:3d}ml: {bucati:3d} bucăți')

print('\n' + '='*100)
print(f'Total produse procesate din Excel: {total_produse_procesate}')
print(f'Total decanturi adăugate în raport: {total_decanturi_procesate}')
print(f'Total parfumuri unice în raport: {len(raport)}')
print(f'Total bucăți decanturi: {sum(raport.values())}')
print('='*100)
