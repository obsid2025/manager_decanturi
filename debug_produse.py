# -*- coding: utf-8 -*-
import pandas as pd
import sys

sys.stdout.reconfigure(encoding='utf-8')

df = pd.read_excel('45.xlsx')
df_finalizate = df[df['Status Comanda'] == 'Comanda Finalizata (Facturata)']

print(f'COMENZI FINALIZATE: {len(df_finalizate)}')
print('\nToate produsele din comenzi finalizate:')

total_produse = 0
for idx, row in df_finalizate.iterrows():
    print(f"\n=== Comanda #{row['Numar Comanda']} ===")
    produse = str(row['Produse comandate']).split(' | ')
    print(f"Numar produse: {len(produse)}")
    for p in produse:
        print(f'  - {p}')
        total_produse += 1

print(f"\n\nTOTAL PRODUSE IN COMENZI FINALIZATE: {total_produse}")
