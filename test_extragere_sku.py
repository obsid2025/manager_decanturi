# -*- coding: utf-8 -*-
"""
Test extragere SKU-uri din coloana Atribute
"""
import pandas as pd
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

# Citire fișier
df = pd.read_excel('45.xlsx')

# Filtrare comenzi finalizate
df_finalizate = df[df['Status Comanda'] == 'Comanda Finalizata (Facturata)']

print(f'COMENZI FINALIZATE: {len(df_finalizate)}\n')
print('='*100)

# Procesare comenzi
bonuri_productie = []

for idx, row in df_finalizate.iterrows():
    print(f"\n=== Comanda #{row['Numar Comanda']} ===")

    produse_text = str(row['Produse comandate'])
    atribute_text = str(row['Atributele produselor comandate'])

    # Split produse
    produse = produse_text.split(' | ')

    # Extrage SKU-uri din atribute
    # Format: "SKU: (atribute), SKU2: (atribute2)"
    sku_matches = re.findall(r'([^,\s]+):\s*\(', atribute_text)

    print(f"Produse: {len(produse)}")
    print(f"SKU-uri gasite: {len(sku_matches)}")

    # Match produse cu SKU-uri
    for i, produs in enumerate(produse):
        produs = produs.strip()

        # Extrage cantitatea din produs (ultima valoare X.00)
        match_cantitate = re.search(r'(\d+\.\d+)$', produs)
        cantitate = int(float(match_cantitate.group(1))) if match_cantitate else 1

        # SKU pentru acest produs
        sku = sku_matches[i] if i < len(sku_matches) else 'N/A'

        # Extrage numele parfumului
        match_parfum = re.search(r'Decant \d+ ml parfum (.+?),', produs)
        nume_parfum = match_parfum.group(1) if match_parfum else produs[:50]

        print(f"\n  Produs {i+1}:")
        print(f"    Nume: {nume_parfum}")
        print(f"    SKU: {sku}")
        print(f"    Cantitate: {cantitate}")

        # Adaugă la lista de bonuri
        for _ in range(cantitate):
            bonuri_productie.append({
                'comanda': row['Numar Comanda'],
                'sku': sku,
                'nume': nume_parfum,
                'produs_full': produs
            })

print('\n' + '='*100)
print(f'\nTOTAL BONURI DE PRODUCTIE DE CREAT: {len(bonuri_productie)}')
print('='*100)

print('\n\nPRIMELE 10 BONURI:')
for i, bon in enumerate(bonuri_productie[:10], 1):
    print(f"{i}. SKU: {bon['sku']} | Nume: {bon['nume'][:40]}")
