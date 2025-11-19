# -*- coding: utf-8 -*-
"""
Script de automatizare pentru crearea bonurilor de producție în Oblio
Folosește Selenium pentru a interacționa cu interfața web Oblio
"""

import time
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import pandas as pd

sys.stdout.reconfigure(encoding='utf-8')


class OblioAutomation:
    def __init__(self, headless=False):
        """
        Inițializează browser-ul pentru automatizare

        Args:
            headless: Dacă True, rulează browser-ul fără interfață grafică
        """
        self.headless = headless
        self.driver = None
        self.wait = None

    def setup_driver(self):
        """Configurează driver-ul Selenium (Edge sau Chrome)"""
        from selenium.webdriver.edge.service import Service as EdgeService
        from selenium.webdriver.edge.options import Options as EdgeOptions

        options = EdgeOptions()
        if self.headless:
            options.add_argument('--headless')

        # Opțiuni pentru stabilitate
        options.add_argument('--start-maximized')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)

        self.driver = webdriver.Edge(options=options)
        self.wait = WebDriverWait(self.driver, 15)

        print("✅ Browser pornit cu succes")

    def login_oblio(self, email=None, password=None):
        """
        Autentificare în Oblio
        Dacă email/password sunt None, așteaptă login manual
        """
        print("\n🔐 Navigare la pagina Oblio...")
        self.driver.get("https://www.oblio.eu/stock/production/")

        # Verifică dacă e deja logat
        time.sleep(2)
        current_url = self.driver.current_url

        if 'login' in current_url.lower():
            if email and password:
                print("🔑 Autentificare automată...")
                # Găsește câmpurile de login
                email_input = self.wait.until(
                    EC.presence_of_element_located((By.ID, "email"))
                )
                password_input = self.driver.find_element(By.ID, "password")

                email_input.send_keys(email)
                password_input.send_keys(password)
                password_input.send_keys(Keys.RETURN)

                time.sleep(3)
            else:
                print("⏳ MANUAL LOGIN NECESAR!")
                print("Te rog autentifică-te în browser...")
                print("Apasă ENTER după ce te-ai autentificat:")
                input()

        # Navighează la pagina de producție
        self.driver.get("https://www.oblio.eu/stock/production/")
        time.sleep(2)

        print("✅ Autentificare reușită!")

    def creeaza_bon_productie(self, sku, cantitate, nume_produs=""):
        """
        Creează un bon de producție pentru un produs

        Args:
            sku: SKU-ul produsului
            cantitate: Cantitatea de produs
            nume_produs: Numele produsului (pentru log)

        Returns:
            True dacă bonul a fost creat cu succes, False altfel
        """
        try:
            print(f"\n📦 Procesare: {nume_produs}")
            print(f"   SKU: {sku}")
            print(f"   Cantitate: {cantitate}")

            # 1. Găsește input-ul pentru numele produsului
            pp_name_input = self.wait.until(
                EC.presence_of_element_located((By.ID, "pp_name"))
            )

            # 2. Șterge conținutul existent
            pp_name_input.clear()
            time.sleep(0.5)

            # 3. Scrie SKU-ul
            pp_name_input.send_keys(sku)
            print(f"   ⌨️  SKU introdus: {sku}")

            # 4. Așteaptă autocomplete să apară
            time.sleep(1.5)

            # 5. Selectează primul rezultat din autocomplete (apasă ENTER sau DOWN + ENTER)
            try:
                # Încearcă să găsească dropdown-ul autocomplete
                autocomplete = self.driver.find_elements(By.CLASS_NAME, "ui-autocomplete")
                if autocomplete and autocomplete[0].is_displayed():
                    pp_name_input.send_keys(Keys.ARROW_DOWN)
                    time.sleep(0.3)
                    pp_name_input.send_keys(Keys.RETURN)
                    print("   ✅ Produs selectat din autocomplete")
                else:
                    # Dacă nu există autocomplete, încearcă ENTER direct
                    pp_name_input.send_keys(Keys.RETURN)
                    print("   ⚠️  Autocomplete nu a apărut, trimis ENTER direct")
            except Exception as e:
                print(f"   ⚠️  Eroare autocomplete: {e}")
                pp_name_input.send_keys(Keys.RETURN)

            time.sleep(1)

            # 6. Verifică dacă produsul a fost selectat (pp_name_id ar trebui completat)
            pp_name_id = self.driver.find_element(By.ID, "pp_name_id").get_attribute("value")
            if not pp_name_id:
                print("   ❌ Produsul nu a fost găsit/selectat!")
                return False

            print(f"   ✅ Produs ID: {pp_name_id}")

            # 7. Completează cantitatea
            pp_quantity_input = self.driver.find_element(By.ID, "pp_quantity")
            pp_quantity_input.clear()
            pp_quantity_input.send_keys(str(cantitate))
            print(f"   ✅ Cantitate setată: {cantitate}")

            time.sleep(0.5)

            # 8. Găsește și apasă butonul de salvare
            # Caută butonul prin mai multe metode
            save_button = None
            try:
                # Încearcă să găsească butonul prin text
                save_button = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Salvare')]")
            except:
                try:
                    # Încearcă prin ID sau class
                    save_button = self.driver.find_element(By.ID, "save_production_btn")
                except:
                    try:
                        # Încearcă prin tip submit
                        save_button = self.driver.find_element(By.XPATH, "//button[@type='submit']")
                    except:
                        print("   ⚠️  Nu s-a găsit butonul de salvare automat")
                        print("   👆 Apasă manual butonul de salvare în browser și apoi ENTER aici:")
                        input()
                        return True

            if save_button:
                save_button.click()
                print("   ✅ Buton salvare apăsat")
                time.sleep(2)

            # 9. Verifică dacă a apărut mesaj de succes
            try:
                # Caută mesaj de succes (poate varia în funcție de versiunea Oblio)
                success_msg = self.driver.find_elements(By.CLASS_NAME, "alert-success")
                if success_msg:
                    print("   🎉 BON CREAT CU SUCCES!")
                else:
                    print("   ⚠️  Nu s-a detectat mesaj de confirmare")
            except:
                pass

            # 10. Așteaptă un pic pentru refresh
            time.sleep(1.5)

            return True

        except TimeoutException:
            print(f"   ❌ TIMEOUT: Elementul nu a fost găsit la timp")
            return False
        except Exception as e:
            print(f"   ❌ EROARE: {str(e)}")
            return False

    def proceseaza_lista_bonuri(self, bonuri_list):
        """
        Procesează o listă de bonuri de producție

        Args:
            bonuri_list: Lista de dict-uri cu 'sku', 'cantitate', 'nume'

        Returns:
            Dict cu statistici (succes, eșec)
        """
        total = len(bonuri_list)
        succes = 0
        esec = 0

        print(f"\n{'='*60}")
        print(f"🚀 START PROCESARE: {total} bonuri de producție")
        print(f"{'='*60}")

        for idx, bon in enumerate(bonuri_list, 1):
            print(f"\n[{idx}/{total}] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

            sku = bon.get('sku', '')
            cantitate = bon.get('cantitate', 1)
            nume = bon.get('nume', '')

            if self.creeaza_bon_productie(sku, cantitate, nume):
                succes += 1
            else:
                esec += 1
                print(f"   ⚠️  Bon EȘUAT pentru {nume}")

            # Pauză între bonuri (evită supraîncărcarea)
            if idx < total:
                time.sleep(1)

        print(f"\n{'='*60}")
        print(f"✅ PROCESARE COMPLETĂ!")
        print(f"   Succes: {succes}/{total}")
        print(f"   Eșec:   {esec}/{total}")
        print(f"{'='*60}\n")

        return {
            'total': total,
            'succes': succes,
            'esec': esec
        }

    def close(self):
        """Închide browser-ul"""
        if self.driver:
            print("\n👋 Închidere browser...")
            # Așteaptă puțin pentru ca utilizatorul să vadă rezultatele
            time.sleep(2)
            self.driver.quit()
            print("✅ Browser închis")


def citeste_bonuri_din_excel(fisier_path):
    """
    Citește bonurile de producție din fișierul Excel

    Returns:
        Lista de bonuri
    """
    df = pd.read_excel(fisier_path)

    # Presupunem că fișierul are coloanele: SKU, Nume, Cantitate
    bonuri = []
    for idx, row in df.iterrows():
        bonuri.append({
            'sku': str(row.get('SKU', '')),
            'nume': str(row.get('Parfum', '')),
            'cantitate': int(row.get('Bucăți', 1))
        })

    return bonuri


def main():
    """Funcția principală"""
    print("""
╔═══════════════════════════════════════════════════════╗
║   🤖 AUTOMATIZARE BONURI DE PRODUCȚIE OBLIO          ║
║   OBSID - Parfumuri Arabești Premium                 ║
╚═══════════════════════════════════════════════════════╝
    """)

    # Inițializare automation
    automation = OblioAutomation(headless=False)

    try:
        # Setup browser
        automation.setup_driver()

        # Login (manual sau automat)
        # Pentru securitate, LOGIN MANUAL este recomandat!
        automation.login_oblio()  # Login manual

        # Sau login automat (NESIGUR - nu recomand să salvezi parola în cod!):
        # automation.login_oblio(email="email@exemplu.ro", password="parola")

        # Citește bonurile din Excel (sau din API)
        # OPȚIUNE 1: Citește din Excel exportat
        # bonuri = citeste_bonuri_din_excel('raport_productie.xlsx')

        # OPȚIUNE 2: Listă hard-coded pentru test
        bonuri = [
            {'sku': '6291106063742-3', 'nume': 'Decant 3ml Yum Yum Armaf', 'cantitate': 5},
            {'sku': '6291106063717-3', 'nume': 'Decant 3ml Yara Lattafa', 'cantitate': 4},
            {'sku': '6291106063721-10', 'nume': 'Decant 10ml Fakhar Rose Lattafa', 'cantitate': 3},
        ]

        print(f"\n📋 S-au găsit {len(bonuri)} bonuri de creat\n")

        # Procesează bonurile
        stats = automation.proceseaza_lista_bonuri(bonuri)

        print("\n🎯 Procesare finalizată cu succes!")
        print(f"Poți verifica bonurile create în Oblio.")

    except KeyboardInterrupt:
        print("\n\n⚠️  Procesare întreruptă de utilizator (Ctrl+C)")
    except Exception as e:
        print(f"\n\n❌ EROARE CRITICĂ: {str(e)}")
        import traceback
        traceback.print_exc()
    finally:
        # Închide browser-ul
        automation.close()


if __name__ == "__main__":
    main()
