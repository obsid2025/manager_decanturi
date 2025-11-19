# -*- coding: utf-8 -*-
import pandas as pd
import sys

sys.stdout.reconfigure(encoding='utf-8')

df = pd.read_excel('45.xlsx')

print('=== CAUTARE COMPLETA "YARA MOI" IN FISIER ===\n')

found_count = 0
for idx, row in df.iterrows():
    produse_text = str(row['Produse comandate'])
    if 'Yara Moi' in produse_text or 'yara moi' in produse_text.lower():
        found_count += 1
        print(f'\n--- RANDUL {idx+2} (Comanda #{row["Numar Comanda"]}) ---')
        print(f'Status: {row["Status Comanda"]}')
        print(f'Produse comandate:')

        # Split si afiseaza fiecare produs
        produse = produse_text.split(' | ')
        for i, p in enumerate(produse, 1):
            marker = '>>> ' if 'Yara Moi' in p else '    '
            print(f'{marker}{i}. {p}')

print(f'\n\n=== TOTAL GASIT: {found_count} comenzi cu "Yara Moi" ===')

# Afiseaza TOATE produsele Yara Moi gasite
print('\n=== TOATE PRODUSELE YARA MOI GASITE ===')
all_yara_moi = []
for idx, row in df.iterrows():
    produse_text = str(row['Produse comandate'])
    produse = produse_text.split(' | ')
    for p in produse:
        if 'Yara Moi' in p:
            all_yara_moi.append((row['Numar Comanda'], row['Status Comanda'], p.strip()))

for comanda, status, produs in all_yara_moi:
    print(f'\nComanda #{comanda} ({status}):')
    print(f'  {produs}')
