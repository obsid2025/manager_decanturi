# -*- coding: utf-8 -*-
import pandas as pd
import sys

# Configurare encoding pentru output
sys.stdout.reconfigure(encoding='utf-8')

# Citire fișier
df = pd.read_excel(r'C:\OBSID SRL\Script-uri Obsid\pregatire_decanturi\45.xlsx')

# Filtrare comenzi finalizate
df_finalizate = df[df['Status Comanda'] == 'Comanda Finalizata (Facturata)']

print(f'COMENZI FINALIZATE: {len(df_finalizate)} din {len(df)} total')
print(f'COMENZI ANULATE: {len(df[df["Status Comanda"] == "Anulata"])}')

print('\n' + '='*80)
print('EXEMPLE DE PRODUSE:')
print('='*80)

for idx, row in df_finalizate.head(5).iterrows():
    print(f'\n--- Comanda #{row["Numar Comanda"]} ---')
    produse = str(row['Produse comandate']).split(' | ')
    for p in produse:
        print(f'  - {p}')
