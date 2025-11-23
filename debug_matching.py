import pandas as pd
import re
import os

def normalize_name(text):
    """
    Normalizează numele produsului pentru matching:
    - lowercase
    - elimină 'parfum'
    - elimină caractere non-alfanumerice
    """
    if not isinstance(text, str):
        return ""
    text = text.lower()
    text = text.replace('parfum', '')
    text = re.sub(r'[^a-z0-9]', '', text)
    return text

# Load DB
print("Loading DB...")
# Adjust path if necessary. Assuming script is in root and xlsx is in manager_decanturi/
db_path = r'c:\DEV\Python\manager_decanturi\manager_decanturi\produse.xlsx'
if not os.path.exists(db_path):
    # Fallback to root 51.xlsx if produse.xlsx not found
    db_path = r'c:\DEV\Python\manager_decanturi\51.xlsx'

print(f"Reading DB from: {db_path}")
df_db = pd.read_excel(db_path)
PRODUCT_DB = {}
for _, row in df_db.iterrows():
    nume = str(row['Denumire Produs'])
    sku = str(row['Cod Produs (SKU)']).strip()
    if nume and sku:
        norm_nume = normalize_name(nume)
        PRODUCT_DB[norm_nume] = sku

print(f"Loaded {len(PRODUCT_DB)} products in DB.")

# Load Orders
print("Loading Orders...")
orders_path = r'c:\DEV\Python\manager_decanturi\50.xlsx'
df_orders = pd.read_excel(orders_path)

print("\nChecking matches with NEW logic:")
matches = 0
mismatches = 0

# Simulate the logic in app.py
for idx, row in df_orders.iterrows():
    # Detect columns dynamically if needed, but assuming 'Produse comandate' exists based on previous file
    col_produse = 'Produse comandate'
    if col_produse not in df_orders.columns:
        # Try to find it
        for c in df_orders.columns:
            if 'produse' in str(c).lower():
                col_produse = c
                break
    
    produse_text = str(row[col_produse])
    produse = produse_text.split(' | ')
    
    for produs in produse:
        produs = produs.strip()
        if 'Decant' not in produs:
            continue
            
        # Logic from app.py
        produs_clean = re.sub(r', \d+\.\d+$', '', produs)
        produs_norm = normalize_name(produs_clean)
        
        if produs_norm in PRODUCT_DB:
            sku = PRODUCT_DB[produs_norm]
            if matches < 10:
                print(f"[MATCH] '{produs_clean}' -> SKU: {sku}")
            matches += 1
        else:
            print(f"[NO MATCH] '{produs_clean}'")
            print(f"   Normalized: '{produs_norm}'")
            mismatches += 1

print(f"\nTotal Matches: {matches}")
print(f"Total Mismatches: {mismatches}")
