# -*- coding: utf-8 -*-
"""
Script pentru procesarea comenzilor de decanturi
Generează un raport de producție cu numărul exact de decanturi necesare
pentru fiecare parfum și cantitate (3ml, 5ml, 10ml)
"""

import pandas as pd
import sys
import re
from collections import defaultdict
from pathlib import Path

# Configurare encoding pentru output
sys.stdout.reconfigure(encoding='utf-8')


def extrageInfoProdus(text_produs):
    """
    Extrage informații din textul produsului
    Returns: (nume_parfum, cantitate_ml, numar_bucati) sau None dacă nu e decant
    """
    # Verifică dacă este un decant
    if 'Decant' not in text_produs:
        return None

    # Extrage cantitatea în ml (3 ml, 5 ml, 10 ml)
    match_ml = re.search(r'Decant (\d+) ml parfum (.+?),', text_produs)
    if not match_ml:
        return None

    cantitate_ml = int(match_ml.group(1))
    nume_parfum = match_ml.group(2).strip()

    # Extrage numărul de bucăți (ultimul număr din șir, format X.00)
    match_bucati = re.search(r'(\d+\.\d+)$', text_produs.strip())
    if match_bucati:
        numar_bucati = float(match_bucati.group(1))
    else:
        numar_bucati = 1.0

    return (nume_parfum, cantitate_ml, int(numar_bucati))


def detecteazaColoane(df):
    """
    Detectează automat coloanele necesare din Excel
    Returns: (coloana_status, coloana_produse, coloana_atribute)
    """
    coloane = df.columns.tolist()

    # Detectare coloană Status
    coloana_status = None
    for col in coloane:
        col_lower = str(col).lower()
        if any(keyword in col_lower for keyword in ['status', 'stare', 'statu']):
            coloana_status = col
            break

    # Detectare coloană Produse
    coloana_produse = None
    for col in coloane:
        col_lower = str(col).lower()
        if any(keyword in col_lower for keyword in ['produse', 'produs', 'articol', 'item']):
            coloana_produse = col
            break

    # Detectare coloană Atribute
    coloana_atribute = None
    for col in coloane:
        col_lower = str(col).lower()
        if any(keyword in col_lower for keyword in ['atribute', 'atribut']):
            coloana_atribute = col
            break

    if not coloana_status:
        raise ValueError('Nu s-a găsit coloana cu statusul comenzii (trebuie să conțină "Status" în nume)')

    if not coloana_produse:
        raise ValueError('Nu s-a găsit coloana cu produsele comandate (trebuie să conțină "Produse" în nume)')

    return coloana_status, coloana_produse, coloana_atribute


def proceseazaComenzi(cale_fisier):
    """
    Procesează fișierul cu comenzi și returnează raportul de producție
    """
    # Citire fișier Excel
    df = pd.read_excel(cale_fisier)

    # Detectare coloane
    try:
        coloana_status, coloana_produse, coloana_atribute = detecteazaColoane(df)
    except ValueError as e:
        print(f"Eroare structură fișier: {e}")
        return {}, 0, len(df)

    # Filtrare comenzi finalizate (include și Confirmata pentru flexibilitate)
    # Caută 'Finalizata' sau 'Confirmata' (case insensitive)
    df_finalizate = df[df[coloana_status].astype(str).str.contains('Finalizata|Confirmata', case=False, na=False)]

    # Dicționar pentru agregare: {(nume_parfum, cantitate_ml): total_bucati}
    raport = defaultdict(int)

    # Procesare comenzi
    for idx, row in df_finalizate.iterrows():
        # Split produse separate prin ' | '
        produse = str(row[coloana_produse]).split(' | ')
        atribute_text = str(row[coloana_atribute]) if coloana_atribute else ''

        # Extrage SKU-uri din atribute
        sku_matches = re.findall(r'([^,\s]+):\s*\(', atribute_text) if atribute_text else []

        for i, produs in enumerate(produse):
            info = extrageInfoProdus(produs.strip())
            if info:
                nume_parfum, cantitate_ml, numar_bucati = info

                # Verificare SKU (dacă există)
                # User request: exclude produsele care nu au extensie -3/-5/-10 (parfumuri întregi)
                if i < len(sku_matches):
                    sku = sku_matches[i]
                    # Verifică dacă SKU se termină în -cifră (ex: -3, -5, -10)
                    if not re.search(r'-\d+$', sku):
                        # Dacă SKU-ul nu are extensie de decant, îl ignorăm
                        # Chiar dacă numele conține "Decant" (posibilă eroare în denumire sau parsare)
                        continue

                raport[(nume_parfum, cantitate_ml)] += numar_bucati

    return raport, len(df_finalizate), len(df)


def afiseazaRaport(raport, comenzi_finalizate, total_comenzi):
    """
    Afișează raportul de producție într-un format clar și ușor de citit
    """
    print('\n' + '='*100)
    print('RAPORT DE PRODUCȚIE - DECANTURI PARFUMURI'.center(100))
    print('='*100)
    print(f'\nComenzi procesate: {comenzi_finalizate} finalizate din {total_comenzi} total')
    print(f'Comenzi anulate/excluse: {total_comenzi - comenzi_finalizate}')
    print('\n' + '='*100)

    # Grupare pe parfum
    parfumuri = {}
    for (nume_parfum, cantitate_ml), bucati in raport.items():
        if nume_parfum not in parfumuri:
            parfumuri[nume_parfum] = {}
        parfumuri[nume_parfum][cantitate_ml] = bucati

    # Sortare alfabetică după nume parfum
    for nume_parfum in sorted(parfumuri.keys()):
        print(f'\n📦 {nume_parfum}')
        print('-' * 100)

        cantitati = parfumuri[nume_parfum]
        total_bucati_parfum = sum(cantitati.values())

        # Afișare pe cantități (3ml, 5ml, 10ml)
        for ml in sorted(cantitati.keys()):
            bucati = cantitati[ml]
            print(f'   • {ml:2d} ml: {bucati:3d} bucăți')

        print(f'   {"─" * 50}')
        print(f'   TOTAL: {total_bucati_parfum} bucăți')

    print('\n' + '='*100)
    print('SUMAR GLOBAL'.center(100))
    print('='*100)

    # Sumar pe cantități
    sumar_cantitati = defaultdict(int)
    for (nume_parfum, cantitate_ml), bucati in raport.items():
        sumar_cantitati[cantitate_ml] += bucati

    print('\nTotal decanturi pe cantități:')
    for ml in sorted(sumar_cantitati.keys()):
        print(f'   • {ml:2d} ml: {sumar_cantitati[ml]:3d} bucăți')

    total_global = sum(sumar_cantitati.values())
    print(f'\n   TOTAL GENERAL: {total_global} bucăți')
    print('='*100 + '\n')


def salveazaRaportExcel(raport, cale_fisier_iesire):
    """
    Salvează raportul într-un fișier Excel structurat
    """
    # Pregătire date pentru Excel
    date_raport = []

    for (nume_parfum, cantitate_ml), bucati in sorted(raport.items()):
        date_raport.append({
            'Parfum': nume_parfum,
            'Cantitate (ml)': cantitate_ml,
            'Bucăți': bucati
        })

    # Creare DataFrame și salvare
    df_raport = pd.DataFrame(date_raport)

    if df_raport.empty:
        print(f'⚠ Nu au fost găsite decanturi de procesat.')
        # Creăm un DataFrame gol cu coloanele corecte pentru a evita erorile
        df_raport = pd.DataFrame(columns=['Parfum', 'Cantitate (ml)', 'Bucăți'])
        df_sumar = pd.DataFrame(columns=['Parfum', 'Total Bucăți'])
    else:
        # Grupare pe parfum pentru sumar
        df_sumar = df_raport.groupby('Parfum').agg({
            'Bucăți': 'sum'
        }).reset_index()
        df_sumar.columns = ['Parfum', 'Total Bucăți']

    # Salvare în Excel cu mai multe sheet-uri
    with pd.ExcelWriter(cale_fisier_iesire, engine='openpyxl') as writer:
        df_raport.to_excel(writer, sheet_name='Raport Detaliat', index=False)
        df_sumar.to_excel(writer, sheet_name='Sumar pe Parfum', index=False)

    print(f'✓ Raport salvat în: {cale_fisier_iesire}')


def main():
    """
    Funcție principală
    """
    # Verifică argumentele din linia de comandă
    if len(sys.argv) < 2:
        print('Utilizare: python procesare_comenzi_decanturi.py <fisier_comenzi.xlsx>')
        print('\nExemplu: python procesare_comenzi_decanturi.py 45.xlsx')
        sys.exit(1)

    cale_fisier_intrare = sys.argv[1]

    # Verifică dacă fișierul există
    if not Path(cale_fisier_intrare).exists():
        print(f'✗ Eroare: Fișierul {cale_fisier_intrare} nu există!')
        sys.exit(1)

    # Procesare comenzi
    print(f'\n📊 Procesare fișier: {cale_fisier_intrare}')
    raport, comenzi_finalizate, total_comenzi = proceseazaComenzi(cale_fisier_intrare)

    # Afișare raport
    afiseazaRaport(raport, comenzi_finalizate, total_comenzi)

    # Salvare raport Excel
    nume_fisier_iesire = Path(cale_fisier_intrare).stem + '_raport_productie.xlsx'
    salveazaRaportExcel(raport, nume_fisier_iesire)


if __name__ == '__main__':
    main()
