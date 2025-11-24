import os
import logging
import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import datetime

# Configurare logging
logger = logging.getLogger(__name__)

def get_db_connection():
    """
    Creează o conexiune la baza de date PostgreSQL folosind variabila de mediu DATABASE_URL
    """
    database_url = os.environ.get('DATABASE_URL')
    if not database_url:
        # Fallback pentru dezvoltare locală (dacă e cazul) sau eroare
        logger.warning("⚠️ DATABASE_URL nu este setat! Încerc conexiune locală default...")
        # Poți seta un default aici sau returna None
        return None
        
    try:
        conn = psycopg2.connect(database_url)
        return conn
    except Exception as e:
        logger.error(f"❌ Eroare conectare DB: {e}")
        return None

def init_db():
    """Inițializează tabelul dacă nu există"""
    conn = get_db_connection()
    if not conn:
        return

    try:
        cur = conn.cursor()
        
        # Tabel pentru bonuri de producție
        cur.execute('''
            CREATE TABLE IF NOT EXISTS bonuri_procesate (
                id SERIAL PRIMARY KEY,
                sku VARCHAR(50) NOT NULL,
                nume_produs TEXT,
                cantitate DECIMAL(10, 2),
                data_procesare DATE DEFAULT CURRENT_DATE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Index pentru căutare rapidă după dată și SKU
        cur.execute('''
            CREATE INDEX IF NOT EXISTS idx_data_sku 
            ON bonuri_procesate (data_procesare, sku)
        ''')
        
        conn.commit()
        cur.close()
        conn.close()
        logger.info("✅ Baza de date PostgreSQL inițializată cu succes.")
    except Exception as e:
        logger.error(f"❌ Eroare inițializare DB: {e}")

def adauga_bon(sku, nume, cantitate):
    """Salvează un bon procesat cu succes"""
    conn = get_db_connection()
    if not conn:
        return False

    try:
        cur = conn.cursor()
        today = datetime.now().strftime('%Y-%m-%d')
        
        cur.execute('''
            INSERT INTO bonuri_procesate (sku, nume_produs, cantitate, data_procesare)
            VALUES (%s, %s, %s, %s)
        ''', (sku, nume, cantitate, today))
        
        conn.commit()
        cur.close()
        conn.close()
        logger.info(f"💾 Bon salvat în DB: {sku}")
        return True
    except Exception as e:
        logger.error(f"❌ Eroare salvare în DB: {e}")
        return False

def get_bonuri_azi():
    """Returnează lista de SKU-uri procesate astăzi"""
    conn = get_db_connection()
    if not conn:
        return []

    try:
        cur = conn.cursor(cursor_factory=RealDictCursor)
        today = datetime.now().strftime('%Y-%m-%d')
        
        cur.execute('''
            SELECT sku, nume_produs FROM bonuri_procesate 
            WHERE data_procesare = %s
        ''', (today,))
        
        rows = cur.fetchall()
        cur.close()
        conn.close()
        
        rezultate = []
        for row in rows:
            rezultate.append({
                'sku': row['sku'],
                'nume': row['nume_produs']
            })
            
        return rezultate
    except Exception as e:
        logger.error(f"❌ Eroare citire din DB: {e}")
        return []
