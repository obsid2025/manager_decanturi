# -*- coding: utf-8 -*-
"""
Aplicație web pentru procesarea comenzilor de decanturi
OBSID - Platformă de management decanturi parfumuri
"""

from flask import Flask, render_template, request, jsonify, send_file
import pandas as pd
import re
from collections import defaultdict
from pathlib import Path
import os
from datetime import datetime
from werkzeug.utils import secure_filename
import io

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['EXPORT_FOLDER'] = 'exports'

# Creare directoare dacă nu există
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['EXPORT_FOLDER'], exist_ok=True)

ALLOWED_EXTENSIONS = {'xlsx', 'xls'}


def allowed_file(filename):
    """Verifică dacă fișierul are extensie permisă"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def extrageInfoProdus(text_produs):
    """
    Extrage informații din textul produsului
    Returns: (nume_parfum, cantitate_ml, numar_bucati) sau None dacă nu e decant
    """
    if 'Decant' not in text_produs:
        return None

    # Extrage cantitatea în ml (3 ml, 5 ml, 10 ml)
    match_ml = re.search(r'Decant (\d+) ml parfum (.+?),', text_produs)
    if not match_ml:
        return None

    cantitate_ml = int(match_ml.group(1))
    nume_parfum = match_ml.group(2).strip()

    # Extrage numărul de bucăți
    match_bucati = re.search(r'(\d+\.\d+)$', text_produs.strip())
    if match_bucati:
        numar_bucati = float(match_bucati.group(1))
    else:
        numar_bucati = 1.0

    return (nume_parfum, cantitate_ml, int(numar_bucati))


def detecteazaColoane(df):
    """
    Detectează automat coloanele necesare din Excel
    Returns: (coloana_status, coloana_produse)
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

    if not coloana_status:
        raise ValueError('Nu s-a găsit coloana cu statusul comenzii (trebuie să conțină "Status" în nume)')

    if not coloana_produse:
        raise ValueError('Nu s-a găsit coloana cu produsele comandate (trebuie să conțină "Produse" în nume)')

    return coloana_status, coloana_produse


def proceseazaComenzi(fisier_path):
    """
    Procesează fișierul cu comenzi și returnează raportul de producție
    Detectează automat coloanele necesare (ordinea nu mai contează)
    """
    df = pd.read_excel(fisier_path)

    # Detectare automată coloane
    coloana_status, coloana_produse = detecteazaColoane(df)

    # Filtrare comenzi finalizate (flexibil - acceptă variante)
    df_finalizate = df[df[coloana_status].astype(str).str.contains('Finalizata', case=False, na=False)]

    raport = defaultdict(int)

    for idx, row in df_finalizate.iterrows():
        produse = str(row[coloana_produse]).split(' | ')
        for produs in produse:
            info = extrageInfoProdus(produs.strip())
            if info:
                nume_parfum, cantitate_ml, numar_bucati = info
                raport[(nume_parfum, cantitate_ml)] += numar_bucati

    return raport, len(df_finalizate), len(df)


def genereazaTabelRaport(raport):
    """
    Generează datele pentru tabel în format optimizat
    (parfumul apare o singură dată pe coloana A)
    """
    # Grupare pe parfum
    parfumuri = {}
    for (nume_parfum, cantitate_ml), bucati in raport.items():
        if nume_parfum not in parfumuri:
            parfumuri[nume_parfum] = {}
        parfumuri[nume_parfum][cantitate_ml] = bucati

    # Construire rânduri pentru tabel
    randuri = []
    for nume_parfum in sorted(parfumuri.keys()):
        cantitati = parfumuri[nume_parfum]
        total_bucati = sum(cantitati.values())

        # Sortare cantități
        cantitati_sortate = sorted(cantitati.items())

        # Primul rând - cu numele parfumului
        primul_rand = True
        for ml, bucati in cantitati_sortate:
            randuri.append({
                'parfum': nume_parfum if primul_rand else '',
                'cantitate_ml': ml,
                'bucati': bucati,
                'total': total_bucati if primul_rand else '',
                'este_prim': primul_rand
            })
            primul_rand = False

    return randuri


@app.route('/')
def index():
    """Pagina principală"""
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    """
    Upload și procesare fișier Excel
    """
    if 'file' not in request.files:
        return jsonify({'error': 'Nu a fost selectat niciun fișier'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'Nu a fost selectat niciun fișier'}), 400

    if not allowed_file(file.filename):
        return jsonify({'error': 'Tipul fișierului nu este permis. Folosiți .xlsx sau .xls'}), 400

    try:
        # Salvare fișier temporar
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        save_filename = f"{timestamp}_{filename}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], save_filename)
        file.save(filepath)

        # Procesare comenzi
        raport, comenzi_finalizate, total_comenzi = proceseazaComenzi(filepath)

        # Generare tabel
        randuri = genereazaTabelRaport(raport)

        # Calcul sumar
        sumar_cantitati = defaultdict(int)
        for (nume_parfum, cantitate_ml), bucati in raport.items():
            sumar_cantitati[cantitate_ml] += bucati

        total_decanturi = sum(sumar_cantitati.values())

        # Pregătire răspuns
        return jsonify({
            'success': True,
            'filename': save_filename,
            'comenzi_finalizate': comenzi_finalizate,
            'total_comenzi': total_comenzi,
            'comenzi_anulate': total_comenzi - comenzi_finalizate,
            'randuri': randuri,
            'sumar': {
                'cantitati': dict(sorted(sumar_cantitati.items())),
                'total': total_decanturi
            }
        })

    except Exception as e:
        return jsonify({'error': f'Eroare la procesare: {str(e)}'}), 500


@app.route('/export/<filename>')
def export_excel(filename):
    """
    Export raport în Excel
    """
    try:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)

        if not os.path.exists(filepath):
            return jsonify({'error': 'Fișierul nu există'}), 404

        # Procesare comenzi
        raport, comenzi_finalizate, total_comenzi = proceseazaComenzi(filepath)

        # Pregătire date pentru Excel
        date_raport = []
        for (nume_parfum, cantitate_ml), bucati in sorted(raport.items()):
            date_raport.append({
                'Parfum': nume_parfum,
                'Cantitate (ml)': cantitate_ml,
                'Bucăți': bucati
            })

        df_raport = pd.DataFrame(date_raport)

        # Sumar pe parfum
        df_sumar = df_raport.groupby('Parfum').agg({'Bucăți': 'sum'}).reset_index()
        df_sumar.columns = ['Parfum', 'Total Bucăți']

        # Creare Excel în memorie
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df_raport.to_excel(writer, sheet_name='Raport Detaliat', index=False)
            df_sumar.to_excel(writer, sheet_name='Sumar pe Parfum', index=False)

        output.seek(0)

        # Nume fișier export
        export_filename = f"raport_productie_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"

        return send_file(
            output,
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            as_attachment=True,
            download_name=export_filename
        )

    except Exception as e:
        return jsonify({'error': f'Eroare la export: {str(e)}'}), 500


@app.route('/download-model')
def download_model():
    """
    Download fișier model de import
    """
    try:
        # Creare model în memorie
        data = {
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

        df_model = pd.DataFrame(data)

        # Creare Excel în memorie
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df_model.to_excel(writer, sheet_name='Model Import', index=False)

            # Adaugă sheet cu instrucțiuni
            instructiuni = pd.DataFrame({
                'INSTRUCȚIUNI UTILIZARE': [
                    '1. Coloane OBLIGATORII:',
                    '   - Status Comanda: trebuie să conțină "Finalizata" pentru comenzi procesate',
                    '   - Produse comandate: lista de produse separate prin " | "',
                    '',
                    '2. Coloanele pot fi în orice ordine',
                    '',
                    '3. Format produse:',
                    '   Decant [CANTITATE] ml parfum [NUME PARFUM], [sex], [NUMĂR BUCĂȚI]',
                    '',
                    '4. Exemple valide:',
                    '   - Decant 3 ml parfum Yara Lattafa, parfum femei, 1.00',
                    '   - Decant 10 ml parfum Khamrah Lattafa, unisex, 2.00',
                    '',
                    '5. Multiple produse separate prin " | "',
                    '',
                    '6. Comenzile anulate sunt automat excluse din raport'
                ]
            })
            instructiuni.to_excel(writer, sheet_name='Instrucțiuni', index=False)

        output.seek(0)

        return send_file(
            output,
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            as_attachment=True,
            download_name='model_import_obsid_decanturi.xlsx'
        )

    except Exception as e:
        return jsonify({'error': f'Eroare la generare model: {str(e)}'}), 500


@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'service': 'OBSID Decant Manager'})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
