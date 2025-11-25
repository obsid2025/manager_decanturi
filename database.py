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
        logger.warning("⚠️ DATABASE_URL nu este setat!")
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

        # Tabel pentru bonuri de producție cu order tracking
        cur.execute('''
            CREATE TABLE IF NOT EXISTS bonuri_procesate (
                id SERIAL PRIMARY KEY,
                sku VARCHAR(100) NOT NULL,
                nume_produs TEXT,
                cantitate DECIMAL(10, 2),
                order_id INTEGER,
                order_number INTEGER,
                data_procesare DATE DEFAULT CURRENT_DATE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # Index unic pentru a preveni duplicate (același SKU + același order_number)
        cur.execute('''
            CREATE UNIQUE INDEX IF NOT EXISTS idx_sku_order_unique
            ON bonuri_procesate (sku, order_number)
        ''')

        # Index pentru căutare rapidă după dată
        cur.execute('''
            CREATE INDEX IF NOT EXISTS idx_data_procesare
            ON bonuri_procesate (data_procesare)
        ''')

        conn.commit()
        cur.close()
        conn.close()
        logger.info("✅ Baza de date PostgreSQL inițializată cu succes.")
    except Exception as e:
        logger.error(f"❌ Eroare inițializare DB: {e}")


def adauga_bon(sku, nume, cantitate, order_id=None, order_number=None):
    """
    Salvează un bon procesat cu succes.

    Args:
        sku: Codul SKU al produsului
        nume: Numele produsului
        cantitate: Cantitatea procesată
        order_id: ID-ul comenzii din Excel (opțional)
        order_number: Numărul comenzii vizibil (opțional)

    Returns:
        True dacă salvarea a reușit, False altfel
    """
    conn = get_db_connection()
    if not conn:
        return False

    try:
        cur = conn.cursor()
        today = datetime.now().strftime('%Y-%m-%d')

        # INSERT cu ON CONFLICT pentru a evita duplicate
        cur.execute('''
            INSERT INTO bonuri_procesate (sku, nume_produs, cantitate, order_id, order_number, data_procesare)
            VALUES (%s, %s, %s, %s, %s, %s)
            ON CONFLICT (sku, order_number) DO UPDATE SET
                cantitate = EXCLUDED.cantitate,
                data_procesare = EXCLUDED.data_procesare
            RETURNING id
        ''', (sku, nume, cantitate, order_id, order_number, today))

        result = cur.fetchone()
        conn.commit()
        cur.close()
        conn.close()

        logger.info(f"💾 Bon salvat în DB: {sku} (comanda #{order_number})")
        return True
    except Exception as e:
        logger.error(f"❌ Eroare salvare în DB: {e}")
        return False


def verificare_bon_exista(sku, order_number):
    """
    Verifică dacă un bon pentru un SKU și o comandă specifică există deja.

    Args:
        sku: Codul SKU
        order_number: Numărul comenzii

    Returns:
        True dacă există, False altfel
    """
    conn = get_db_connection()
    if not conn:
        return False

    try:
        cur = conn.cursor()
        cur.execute('''
            SELECT id FROM bonuri_procesate
            WHERE sku = %s AND order_number = %s
        ''', (sku, order_number))

        result = cur.fetchone()
        cur.close()
        conn.close()

        return result is not None
    except Exception as e:
        logger.error(f"❌ Eroare verificare în DB: {e}")
        return False


def get_bonuri_procesate_pentru_comenzi(order_numbers):
    """
    Returnează toate bonurile procesate pentru o listă de comenzi.
    Util pentru Smart Resume - verifică ce s-a procesat deja.

    Args:
        order_numbers: Lista de numere de comenzi

    Returns:
        Set de tuple (sku, order_number) deja procesate
    """
    conn = get_db_connection()
    if not conn:
        return set()

    try:
        cur = conn.cursor()

        # Folosim ANY pentru a căuta în lista de comenzi
        cur.execute('''
            SELECT sku, order_number FROM bonuri_procesate
            WHERE order_number = ANY(%s)
        ''', (list(order_numbers),))

        rows = cur.fetchall()
        cur.close()
        conn.close()

        # Returnăm set de tuple pentru căutare rapidă O(1)
        return {(row[0], row[1]) for row in rows}
    except Exception as e:
        logger.error(f"❌ Eroare citire din DB: {e}")
        return set()


def get_bonuri_azi():
    """Returnează lista de bonuri procesate astăzi (pentru compatibilitate)"""
    conn = get_db_connection()
    if not conn:
        return []

    try:
        cur = conn.cursor(cursor_factory=RealDictCursor)
        today = datetime.now().strftime('%Y-%m-%d')

        cur.execute('''
            SELECT sku, nume_produs, order_id, order_number
            FROM bonuri_procesate
            WHERE data_procesare = %s
        ''', (today,))

        rows = cur.fetchall()
        cur.close()
        conn.close()

        rezultate = []
        for row in rows:
            rezultate.append({
                'sku': row['sku'],
                'nume': row['nume_produs'],
                'order_id': row['order_id'],
                'order_number': row['order_number']
            })

        return rezultate
    except Exception as e:
        logger.error(f"❌ Eroare citire din DB: {e}")
        return []


def get_statistici_azi():
    """Returnează statistici pentru ziua curentă"""
    conn = get_db_connection()
    if not conn:
        return {}

    try:
        cur = conn.cursor(cursor_factory=RealDictCursor)
        today = datetime.now().strftime('%Y-%m-%d')

        cur.execute('''
            SELECT
                COUNT(*) as total_bonuri,
                COUNT(DISTINCT order_number) as total_comenzi,
                SUM(cantitate) as total_cantitate
            FROM bonuri_procesate
            WHERE data_procesare = %s
        ''', (today,))

        row = cur.fetchone()
        cur.close()
        conn.close()

        return {
            'total_bonuri': row['total_bonuri'] or 0,
            'total_comenzi': row['total_comenzi'] or 0,
            'total_cantitate': float(row['total_cantitate'] or 0)
        }
    except Exception as e:
        logger.error(f"❌ Eroare statistici DB: {e}")
        return {}
