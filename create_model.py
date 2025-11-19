# -*- coding: utf-8 -*-
"""
Creează fișier model de import pentru OBSID Decant Manager
"""
import pandas as pd
import sys

sys.stdout.reconfigure(encoding='utf-8')

# Datele pentru model (exemple)
data = {
    'ID Comanda': [1, 2, 3],
    'Numar Comanda': [100, 101, 102],
    'Status Comanda': [
        'Comanda Finalizata (Facturata)',
        'Comanda Finalizata (Facturata)',
        'Anulata'
    ],
    'Produse comandate': [
        'Decant 3 ml parfum Yara Lattafa, parfum femei, 1.00 | Decant 5 ml parfum Eclaire Lattafa, parfum femei, 2.00',
        'Decant 10 ml parfum Yum Yum Armaf, parfum femei, 1.00',
        'Decant 3 ml parfum Khamrah Lattafa, unisex, 1.00'
    ]
}

df = pd.DataFrame(data)

# Salvare în Excel
df.to_excel('model_import.xlsx', index=False, engine='openpyxl')

print('✓ Fișier model_import.xlsx creat cu succes!')
print('\nColoane obligatorii:')
print('  1. Status Comanda - trebuie să conțină "Finalizata" pentru comenzi procesate')
print('  2. Produse comandate - lista de produse separate prin " | "')
print('\nColoane opționale:')
print('  - ID Comanda')
print('  - Numar Comanda')
print('  - Orice alte coloane (vor fi ignorate)')
