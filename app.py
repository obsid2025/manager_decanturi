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
import logging

# Configurare logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

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
    Returnează și SKU-urile pentru fiecare produs
    """
    df = pd.read_excel(fisier_path)

    # Detectare automată coloane
    coloana_status, coloana_produse = detecteazaColoane(df)

    # Verificare coloană atribute (pentru SKU)
    coloana_atribute = None
    for col in df.columns:
        col_lower = str(col).lower()
        if any(keyword in col_lower for keyword in ['atribute', 'atribut']):
            coloana_atribute = col
            break

    # Filtrare comenzi finalizate (flexibil - acceptă variante)
    df_finalizate = df[df[coloana_status].astype(str).str.contains('Finalizata', case=False, na=False)]

    # Raport agregat pe SKU (în loc de doar pe nume+cantitate)
    raport = defaultdict(lambda: {'nume': '', 'cantitate_ml': 0, 'bucati': 0})

    for idx, row in df_finalizate.iterrows():
        produse_text = str(row[coloana_produse])
        atribute_text = str(row[coloana_atribute]) if coloana_atribute else ''

        produse = produse_text.split(' | ')

        # Extrage SKU-uri din atribute
        sku_matches = re.findall(r'([^,\s]+):\s*\(', atribute_text) if atribute_text else []

        for i, produs in enumerate(produse):
            info = extrageInfoProdus(produs.strip())
            if info:
                nume_parfum, cantitate_ml, numar_bucati = info

                # Obține SKU pentru acest produs
                sku = sku_matches[i] if i < len(sku_matches) else 'N/A'

                # Agregare pe SKU
                raport[sku]['nume'] = nume_parfum
                raport[sku]['cantitate_ml'] = cantitate_ml
                raport[sku]['bucati'] += numar_bucati

    return raport, len(df_finalizate), len(df)


def genereazaTabelRaport(raport):
    """
    Generează datele pentru tabel în format optimizat
    (parfumul apare o singură dată pe coloana A, cu SKU inclus)
    """
    # Grupare pe parfum
    parfumuri = {}
    for sku, info in raport.items():
        nume_parfum = info['nume']
        cantitate_ml = info['cantitate_ml']
        bucati = info['bucati']

        if nume_parfum not in parfumuri:
            parfumuri[nume_parfum] = {}
        if cantitate_ml not in parfumuri[nume_parfum]:
            parfumuri[nume_parfum][cantitate_ml] = []

        parfumuri[nume_parfum][cantitate_ml].append({
            'sku': sku,
            'bucati': bucati
        })

    # Construire rânduri pentru tabel
    randuri = []
    for nume_parfum in sorted(parfumuri.keys()):
        cantitati = parfumuri[nume_parfum]
        total_bucati = sum(sum(item['bucati'] for item in items) for items in cantitati.values())

        # Sortare cantități
        cantitati_sortate = sorted(cantitati.items())

        # Primul rând - cu numele parfumului
        primul_rand = True
        for ml, items in cantitati_sortate:
            for item in items:
                randuri.append({
                    'parfum': nume_parfum if primul_rand else '',
                    'sku': item['sku'],
                    'cantitate_ml': ml,
                    'bucati': item['bucati'],
                    'total': total_bucati if primul_rand else '',
                    'este_prim': primul_rand
                })
                primul_rand = False

    return randuri


def proceseazaBonuriProductie(fisier_path):
    """
    Procesează fișierul și extrage bonuri de producție agregate pe SKU
    Returns: lista de bonuri cu SKU, nume produs, cantitate agregată
    """
    df = pd.read_excel(fisier_path)

    # Detectare automată coloane
    coloana_status, coloana_produse = detecteazaColoane(df)

    # Verificare coloană atribute
    coloana_atribute = None
    for col in df.columns:
        col_lower = str(col).lower()
        if any(keyword in col_lower for keyword in ['atribute', 'atribut']):
            coloana_atribute = col
            break

    if not coloana_atribute:
        raise ValueError('Nu s-a găsit coloana cu atributele produselor')

    # Filtrare comenzi finalizate
    df_finalizate = df[df[coloana_status].astype(str).str.contains('Finalizata', case=False, na=False)]

    # Agregare bonuri pe SKU
    bonuri_agregate = defaultdict(lambda: {'nume': '', 'cantitate': 0, 'comenzi': []})

    for idx, row in df_finalizate.iterrows():
        produse_text = str(row[coloana_produse])
        atribute_text = str(row[coloana_atribute])

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
            bonuri_agregate[sku]['comenzi'].append(str(row.get('Numar Comanda', '')))

    # Sortare după cantitate (descrescător)
    bonuri_sortate = sorted(bonuri_agregate.items(), key=lambda x: x[1]['cantitate'], reverse=True)

    # Convertire la format pentru JSON
    rezultat = []
    for sku, info in bonuri_sortate:
        comenzi_unice = list(set(info['comenzi']))[:5]
        rezultat.append({
            'sku': sku,
            'nume': info['nume'],
            'cantitate': info['cantitate'],
            'comenzi': comenzi_unice,
            'total_comenzi': len(set(info['comenzi']))
        })

    return rezultat


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

        # Procesare comenzi (returnează raport cu SKU-uri)
        raport, comenzi_finalizate, total_comenzi = proceseazaComenzi(filepath)

        # Generare tabel pentru Tab 1 (Raport Decanturi)
        randuri = genereazaTabelRaport(raport)

        # Calcul sumar pentru Tab 1
        sumar_cantitati = defaultdict(int)
        for sku, info in raport.items():
            sumar_cantitati[info['cantitate_ml']] += info['bucati']

        total_decanturi = sum(sumar_cantitati.values())

        # Generare date pentru Tab 2 (Bonuri de Producție)
        # Sortare după cantitate (descrescător)
        bonuri_sortate = sorted(raport.items(), key=lambda x: x[1]['bucati'], reverse=True)
        bonuri = []
        for sku, info in bonuri_sortate:
            bonuri.append({
                'sku': sku,
                'nume': f"Decant {info['cantitate_ml']}ml {info['nume']}",
                'cantitate': info['bucati']
            })

        # Pregătire răspuns (include date pentru ambele taburi)
        return jsonify({
            'success': True,
            'filename': save_filename,
            'comenzi_finalizate': comenzi_finalizate,
            'total_comenzi': total_comenzi,
            'comenzi_anulate': total_comenzi - comenzi_finalizate,
            # Date pentru Tab 1 (Raport Decanturi)
            'randuri': randuri,
            'sumar': {
                'cantitati': dict(sorted(sumar_cantitati.items())),
                'total': total_decanturi
            },
            # Date pentru Tab 2 (Bonuri de Producție)
            'bonuri': bonuri,
            'total_bonuri': len(bonuri),
            'total_bucati': total_decanturi
        })

    except Exception as e:
        return jsonify({'error': f'Eroare la procesare: {str(e)}'}), 500


@app.route('/process-vouchers', methods=['POST'])
def process_vouchers():
    """
    Procesare fișier pentru bonuri de producție (agregate pe SKU)
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

        # Procesare bonuri de producție
        bonuri = proceseazaBonuriProductie(filepath)

        total_bonuri = len(bonuri)
        total_bucati = sum(bon['cantitate'] for bon in bonuri)

        # Pregătire răspuns
        return jsonify({
            'success': True,
            'filename': save_filename,
            'bonuri': bonuri,
            'total_bonuri': total_bonuri,
            'total_bucati': total_bucati
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

        # Procesare comenzi (returnează raport cu SKU-uri)
        raport, comenzi_finalizate, total_comenzi = proceseazaComenzi(filepath)

        # Pregătire date pentru Excel (include SKU)
        date_raport = []
        for sku, info in sorted(raport.items(), key=lambda x: (x[1]['nume'], x[1]['cantitate_ml'])):
            date_raport.append({
                'SKU': sku,
                'Parfum': info['nume'],
                'Cantitate (ml)': info['cantitate_ml'],
                'Bucăți': info['bucati']
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


@app.route('/start-automation-selenium', methods=['POST'])
def start_automation_selenium():
    """
    Pornește automatizarea Selenium pentru crearea bonurilor în Oblio
    """
    try:
        data = request.get_json()
        bonuri = data.get('bonuri', [])
        oblio_cookies = data.get('oblio_cookies')  # Cookies trimise din frontend

        if not bonuri:
            return jsonify({'error': 'Nu există bonuri de procesat'}), 400

        # Import automation class
        from automatizare_oblio_selenium import OblioAutomation
        import platform

        # Detectează dacă rulează în container/Linux (server) sau Windows (local)
        is_linux = platform.system() == 'Linux'

        # Inițializare automation cu parametri corecți
        automation = OblioAutomation(
            use_existing_profile=not is_linux,  # False pe server, True pe Windows local
            headless=is_linux  # True pe server (headless), False pe Windows (cu GUI)
        )

        # Setup driver
        if not automation.setup_driver():
            error_msg = 'Nu s-a putut porni Chrome WebDriver.'
            if is_linux:
                error_msg += ' Verifică logs în automatizare_oblio.log pentru detalii.'
            else:
                error_msg += ' Verifică că Chrome este instalat și rulează cu --remote-debugging-port=9222'

            return jsonify({
                'error': error_msg,
                'hint': 'Windows: Pornește Chrome cu remote debugging. Linux: Verifică logs.'
            }), 500

        # Citește credențialele Oblio din environment variables
        oblio_email = os.environ.get('OBLIO_EMAIL')
        oblio_password = os.environ.get('OBLIO_PASSWORD')
        
        # Log informații despre autentificare
        if oblio_cookies and len(oblio_cookies) > 0:
            logger.info(f"🍪 Cookies primite din frontend: {len(oblio_cookies)} cookies")
            logger.info("🍪 Autentificare cu cookies din frontend")
        else:
            logger.info("⚠️ Cookies Oblio NU au fost primite (normal - sunt HttpOnly)")
            
        if oblio_email and oblio_password:
            logger.info("🔐 Credențiale Oblio disponibile din environment variables")
            logger.info("🔐 Voi folosi autentificare cu email/password")
        else:
            # Verifică că avem cel puțin credențiale
            if not (oblio_email and oblio_password):
                return jsonify({
                    'error': 'Credențiale Oblio lipsă! Setează OBLIO_EMAIL și OBLIO_PASSWORD în environment variables.',
                    'hint': 'Cookies HttpOnly nu pot fi accesate din JavaScript - folosim email/password.'
                }), 500
        
        # Procesează bonurile
        stats = automation.process_bonuri(bonuri, oblio_cookies, oblio_email, oblio_password)

        # Închide browser
        automation.close()

        # Returnează rezultatul
        return jsonify({
            'success': True,
            'stats': stats,
            'message': f'Automatizare finalizată! {stats["success"]}/{stats["total"]} bonuri create cu succes.'
        })

    except Exception as e:
        return jsonify({'error': f'Eroare la automatizare: {str(e)}'}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
