import pandas as pd
import re
import os
from collections import defaultdict

# --- LOGIC COPIED FROM app.py ---

def normalize_name(text):
    if not isinstance(text, str):
        return ""
    text = text.lower()
    text = text.replace('parfum', '')
    text = re.sub(r'[^a-z0-9]', '', text)
    return text

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

def detecteazaColoane(df):
    coloane = df.columns.tolist()
    coloana_status = None
    for col in coloane:
        col_lower = str(col).lower()
        if any(keyword in col_lower for keyword in ['status', 'stare', 'statu']):
            coloana_status = col
            break
    coloana_produse = None
    for col in coloane:
        col_lower = str(col).lower()
        if any(keyword in col_lower for keyword in ['produse', 'produs', 'articol', 'item']):
            coloana_produse = col
            break
    return coloana_status, coloana_produse

# --- MAIN SCRIPT ---

def main():
    print("Loading DB...")
    db_path = r'c:\DEV\Python\manager_decanturi\manager_decanturi\produse.xlsx'
    if not os.path.exists(db_path):
        db_path = 'produse.xlsx'
    
    df_db = pd.read_excel(db_path)
    PRODUCT_DB = {}
    for _, row in df_db.iterrows():
        nume = str(row['Denumire Produs'])
        sku = str(row['Cod Produs (SKU)']).strip()
        if nume and sku:
            norm_nume = normalize_name(nume)
            PRODUCT_DB[norm_nume] = sku

    print(f"Loaded {len(PRODUCT_DB)} products in DB.")

    orders_path = '52.xlsx'
    if not os.path.exists(orders_path):
        print(f"File {orders_path} not found!")
        return

    print(f"Processing {orders_path}...")
    df = pd.read_excel(orders_path)

    coloana_status, coloana_produse = detecteazaColoane(df)
    
    # Filter finalized (simulated)
    df_finalizate = df[df[coloana_status].astype(str).str.contains('Finalizata|Confirmata', case=False, na=False)]
    
    raport = defaultdict(lambda: {'nume': '', 'cantitate_ml': 0, 'bucati': 0})

    for idx, row in df_finalizate.iterrows():
        produse_text = str(row[coloana_produse])
        produse = produse_text.split(' | ')

        for produs in produse:
            info = extrageInfoProdus(produs.strip())
            if info:
                nume_parfum, cantitate_ml, numar_bucati = info
                
                # DB Lookup
                produs_clean = re.sub(r', \d+\.\d+$', '', produs.strip())
                produs_norm = normalize_name(produs_clean)
                
                found_sku = 'N/A'
                if produs_norm in PRODUCT_DB:
                    found_sku = PRODUCT_DB[produs_norm]
                
                sku = found_sku
                
                # Filter non-decants
                if sku != 'N/A' and not re.search(r'-\d+$', sku):
                    continue

                raport[sku]['nume'] = nume_parfum
                raport[sku]['cantitate_ml'] = cantitate_ml
                raport[sku]['bucati'] += numar_bucati

    # Generate Export Data
    date_raport = []
    for sku, info in sorted(raport.items(), key=lambda x: (x[1]['nume'], x[1]['cantitate_ml'])):
        date_raport.append({
            'SKU': sku,
            'Parfum': info['nume'],
            'Cantitate (ml)': info['cantitate_ml'],
            'Bucăți': info['bucati']
        })

    df_raport = pd.DataFrame(date_raport)
    
    if not df_raport.empty:
        df_sumar = df_raport.groupby('Parfum').agg({'Bucăți': 'sum'}).reset_index()
        df_sumar.columns = ['Parfum', 'Total Bucăți']
    else:
        df_sumar = pd.DataFrame()

    output_file = 'test_export_50.xlsx'
    with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
        df_raport.to_excel(writer, sheet_name='Raport Detaliat', index=False)
        if not df_sumar.empty:
            df_sumar.to_excel(writer, sheet_name='Sumar pe Parfum', index=False)
            
    print(f"Export generated successfully: {output_file}")
    print(df_raport.head(10).to_string())

if __name__ == "__main__":
    main()
