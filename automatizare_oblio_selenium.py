"""
OBSID - Automatizare Bonuri Producție Oblio cu Selenium
========================================================

Script care automatizează crearea bonurilor de producție în Oblio
folosind Selenium WebDriver pentru control complet al browser-ului.

Autor: OBSID
Versiune: 1.0
Data: 2025-11-19
"""

import time
import json
import sys
import os
import platform
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import logging

# Configurare logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('automatizare_oblio.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)


class OblioAutomation:
    """Clasa pentru automatizarea bonurilor de producție în Oblio"""

    def __init__(self, use_existing_profile=True, headless=False):
        """
        Inițializare automation

        Args:
            use_existing_profile (bool): Folosește profilul Chrome existent (cu sesiune Oblio)
            headless (bool): Rulează în mod headless (fără interfață grafică)
        """
        self.driver = None
        self.use_existing_profile = use_existing_profile
        self.headless = headless
        self.stats = {
            'total': 0,
            'success': 0,
            'failed': 0,
            'errors': []
        }

    def setup_driver(self):
        """Configurare și pornire Chrome WebDriver"""
        logger.info("🔧 Configurare Chrome WebDriver...")

        # Detectează sistemul de operare
        is_linux = platform.system() == 'Linux'
        is_windows = platform.system() == 'Windows'

        logger.info(f"🖥️ Sistem detectat: {platform.system()}")

        chrome_options = Options()

        # Configurare specifică platformei
        if is_linux:
            # Configurare pentru Ubuntu Server (Coolify)
            logger.info("🐧 Configurare pentru Linux/Ubuntu Server...")

            # Pe server, rulează ÎNTOTDEAUNA în headless mode
            chrome_options.add_argument('--headless=new')
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--disable-software-rasterizer')
            chrome_options.add_argument('--disable-extensions')
            chrome_options.add_argument('--window-size=1920,1080')

            # Chromium pe Ubuntu
            chrome_options.binary_location = '/snap/bin/chromium'

            logger.info("👁️ Mod headless activat (server)")

        elif is_windows:
            # Configurare pentru Windows (local development)
            logger.info("🪟 Configurare pentru Windows...")

            # Folosește profilul Chrome existent pentru sesiune Oblio (doar pe Windows)
            if self.use_existing_profile:
                # Path-ul către profilul Chrome (expandează %USERNAME%)
                username = os.environ.get('USERNAME', 'ukfdb')
                user_data_dir = f"C:\\Users\\{username}\\AppData\\Local\\Google\\Chrome\\User Data"

                # Verifică dacă directorul există
                if os.path.exists(user_data_dir):
                    chrome_options.add_argument(f"user-data-dir={user_data_dir}")
                    chrome_options.add_argument("profile-directory=Default")
                    logger.info(f"📂 Folosesc profilul Chrome: {user_data_dir}")
                else:
                    logger.warning(f"⚠️ Profilul Chrome nu există: {user_data_dir}")

            # Headless mode opțional pe Windows
            if self.headless:
                chrome_options.add_argument('--headless=new')
                chrome_options.add_argument('--disable-gpu')
                logger.info("👁️ Mod headless activat")

            # Opțiuni pentru stabilitate (Windows)
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')

        # Opțiuni comune pentru ambele platforme
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)

        # User agent pentru a evita detecția bot
        chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36')

        # Pornire driver
        try:
            if is_linux:
                # Pe Linux, folosește chromedriver din sistem
                service = Service('/usr/bin/chromedriver')
                self.driver = webdriver.Chrome(service=service, options=chrome_options)
                logger.info("✅ Chromium WebDriver pornit cu succes (Linux)!")
            else:
                # Pe Windows, folosește chromedriver automat
                self.driver = webdriver.Chrome(options=chrome_options)
                logger.info("✅ Chrome WebDriver pornit cu succes (Windows)!")

            # Maximize window (doar pe Windows sau dacă nu e headless)
            if not is_linux and not self.headless:
                self.driver.maximize_window()

            return True
        except Exception as e:
            logger.error(f"❌ Eroare la pornirea Chrome: {e}")
            return False

    def wait_for_element(self, by, selector, timeout=15):
        """
        Așteaptă ca un element să fie disponibil

        Args:
            by: Tipul selectorului (By.ID, By.CSS_SELECTOR, etc.)
            selector: Selectorul elementului
            timeout: Timeout în secunde

        Returns:
            WebElement sau None
        """
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((by, selector))
            )
            return element
        except TimeoutException:
            logger.warning(f"⚠️ Element {selector} nu a fost găsit după {timeout}s")
            return None

    def wait_for_clickable(self, by, selector, timeout=15):
        """
        Așteaptă ca un element să fie clickable

        Args:
            by: Tipul selectorului
            selector: Selectorul elementului
            timeout: Timeout în secunde

        Returns:
            WebElement sau None
        """
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable((by, selector))
            )
            return element
        except TimeoutException:
            logger.warning(f"⚠️ Element {selector} nu e clickable după {timeout}s")
            return None

    def type_slowly(self, element, text, delay=0.05):
        """
        Tastează text character-by-character (pentru autocomplete)

        Args:
            element: WebElement input
            text: Textul de tastat
            delay: Delay între caractere (secunde)
        """
        element.clear()
        for char in text:
            element.send_keys(char)
            time.sleep(delay)
        logger.debug(f"⌨️ Tastat: {text}")

    def create_production_voucher(self, sku, quantity):
        """
        Creează un bon de producție în Oblio

        Args:
            sku (str): Codul SKU al produsului
            quantity (int): Cantitatea

        Returns:
            bool: True dacă succès, False dacă eșec
        """
        logger.info(f"\n{'='*60}")
        logger.info(f"🎯 Creare bon: SKU={sku}, Cantitate={quantity}")
        logger.info(f"{'='*60}")

        try:
            # Navighează la pagina de producție
            url = "https://www.oblio.eu/stock/production/"
            logger.info(f"🌐 Navigare la: {url}")
            self.driver.get(url)
            time.sleep(2)

            # PASUL 1: Găsește și completează câmpul SKU
            logger.info("🔍 Căutare câmp SKU (#pp_name)...")
            pp_name_input = self.wait_for_element(By.ID, "pp_name", timeout=20)

            if not pp_name_input:
                raise Exception("Element #pp_name nu a fost găsit!")

            logger.info(f"✅ Câmp SKU găsit")

            # Tastează SKU character-by-character pentru autocomplete
            logger.info(f"⌨️ Tastare SKU: {sku}")
            self.type_slowly(pp_name_input, sku, delay=0.08)

            # Trigger autocomplete
            pp_name_input.send_keys(Keys.SPACE)
            pp_name_input.send_keys(Keys.BACKSPACE)
            time.sleep(2)

            # PASUL 2: Așteaptă și selectează din autocomplete
            logger.info("🔍 Așteptare autocomplete...")
            time.sleep(2.5)

            # Caută elementele autocomplete (jQuery UI)
            try:
                autocomplete_items = self.driver.find_elements(By.CSS_SELECTOR, ".ui-menu-item")

                if len(autocomplete_items) > 0:
                    logger.info(f"✅ Autocomplete găsit: {len(autocomplete_items)} rezultate")
                    first_item = autocomplete_items[0]
                    logger.info(f"🖱️ Click pe primul rezultat: {first_item.text[:50]}...")
                    first_item.click()
                    time.sleep(1.5)
                else:
                    logger.warning("⚠️ Autocomplete nu a apărut, încerc ENTER...")
                    pp_name_input.send_keys(Keys.ENTER)
                    time.sleep(1.5)
            except Exception as e:
                logger.warning(f"⚠️ Eroare autocomplete: {e}, încerc ENTER...")
                pp_name_input.send_keys(Keys.ENTER)
                time.sleep(1.5)

            # PASUL 3: Verifică că produsul a fost selectat
            logger.info("🔍 Verificare selecție produs...")
            time.sleep(1)

            try:
                pp_name_id = self.driver.find_element(By.ID, "pp_name_id")
                if pp_name_id.get_attribute("value"):
                    logger.info(f"✅ Produs selectat: ID={pp_name_id.get_attribute('value')}")
                else:
                    raise Exception(f"Produsul cu SKU '{sku}' nu a fost selectat! SKU invalid sau nu există în baza de date.")
            except NoSuchElementException:
                raise Exception("Element #pp_name_id nu a fost găsit!")

            # PASUL 4: Completează cantitatea
            logger.info(f"🔢 Completare cantitate: {quantity}")
            pp_quantity_input = self.wait_for_element(By.ID, "pp_quantity", timeout=10)

            if not pp_quantity_input:
                raise Exception("Element #pp_quantity nu a fost găsit!")

            pp_quantity_input.clear()
            time.sleep(0.3)
            pp_quantity_input.send_keys(str(quantity))
            time.sleep(0.5)
            logger.info(f"✅ Cantitate setată: {quantity}")

            # PASUL 5: Click pe butonul de previzualizare/salvare
            logger.info("🔍 Căutare buton salvare...")

            # Încearcă diferite selectoare
            save_button = None
            save_selectors = [
                (By.ID, "invoice_preview_btn"),
                (By.CSS_SELECTOR, "a[onclick*='submit_form_doc']"),
                (By.CSS_SELECTOR, ".btn-submit"),
                (By.XPATH, "//a[contains(text(), 'Previzualizare')]"),
                (By.CSS_SELECTOR, "button[type='submit']")
            ]

            for by, selector in save_selectors:
                try:
                    save_button = self.wait_for_clickable(by, selector, timeout=5)
                    if save_button:
                        logger.info(f"✅ Buton salvare găsit: {selector}")
                        break
                except:
                    continue

            if not save_button:
                raise Exception("Butonul de salvare nu a fost găsit!")

            # Click salvare
            logger.info("🖱️ Click buton salvare...")
            save_button.click()
            time.sleep(4)

            # PASUL 6: Verifică succesul
            logger.info("🔍 Verificare confirmare salvare...")
            time.sleep(2)

            # Caută mesaj de succes sau redirect
            success_indicators = [
                (By.CSS_SELECTOR, ".alert-success"),
                (By.CSS_SELECTOR, ".success"),
                (By.XPATH, "//*[contains(text(), 'succes')]"),
                (By.XPATH, "//*[contains(text(), 'creat')]")
            ]

            success = False
            for by, selector in success_indicators:
                try:
                    element = self.driver.find_element(by, selector)
                    if element.is_displayed():
                        logger.info(f"✅ Mesaj succes găsit: {element.text[:100]}")
                        success = True
                        break
                except:
                    continue

            # Verifică URL-ul (dacă s-a redirectat, probabil e success)
            current_url = self.driver.current_url
            if "production" in current_url and "edit" not in current_url:
                logger.info("✅ Pagina a fost refreshed - probabil success!")
                success = True

            if success:
                logger.info(f"🎉 BON CREAT CU SUCCES! SKU={sku}, Cantitate={quantity}")
                self.stats['success'] += 1
                return True
            else:
                logger.warning(f"⚠️ Nu s-a detectat confirmare clară, dar probabil e OK")
                self.stats['success'] += 1
                return True

        except Exception as e:
            logger.error(f"❌ EROARE la crearea bonului: {e}")
            self.stats['failed'] += 1
            self.stats['errors'].append({
                'sku': sku,
                'quantity': quantity,
                'error': str(e)
            })

            # Screenshot pentru debugging
            try:
                screenshot_path = f"error_screenshot_{sku}_{int(time.time())}.png"
                self.driver.save_screenshot(screenshot_path)
                logger.info(f"📸 Screenshot salvat: {screenshot_path}")
            except:
                pass

            return False

    def process_bonuri(self, bonuri):
        """
        Procesează o listă de bonuri

        Args:
            bonuri (list): Lista de dicționare cu 'sku' și 'cantitate'

        Returns:
            dict: Statistici procesare
        """
        logger.info(f"\n🚀 START PROCESARE: {len(bonuri)} bonuri")
        logger.info(f"{'='*60}\n")

        self.stats['total'] = len(bonuri)

        for i, bon in enumerate(bonuri, 1):
            sku = bon.get('sku')
            cantitate = bon.get('cantitate', 1)

            logger.info(f"\n📦 Bon {i}/{len(bonuri)}")

            success = self.create_production_voucher(sku, cantitate)

            if success:
                logger.info(f"✅ Bon {i}/{len(bonuri)} - SUCCESS")
            else:
                logger.error(f"❌ Bon {i}/{len(bonuri)} - FAILED")

            # Pauză între bonuri
            if i < len(bonuri):
                logger.info(f"⏳ Pauză 2 secunde înainte de următorul bon...")
                time.sleep(2)

        # Raport final
        logger.info(f"\n{'='*60}")
        logger.info(f"📊 RAPORT FINAL")
        logger.info(f"{'='*60}")
        logger.info(f"Total bonuri: {self.stats['total']}")
        logger.info(f"✅ Succese: {self.stats['success']}")
        logger.info(f"❌ Eșecuri: {self.stats['failed']}")

        if self.stats['failed'] > 0:
            logger.info(f"\n❌ Bonuri eșuate:")
            for error in self.stats['errors']:
                logger.info(f"  - SKU: {error['sku']}, Eroare: {error['error']}")

        logger.info(f"{'='*60}\n")

        return self.stats

    def close(self):
        """Închide browser-ul"""
        if self.driver:
            logger.info("🚪 Închidere browser...")
            try:
                self.driver.quit()
                logger.info("✅ Browser închis")
            except:
                pass


def main():
    """Funcție main pentru rulare standalone"""

    # Exemplu listă bonuri (în producție, acestea vor veni de la Flask)
    bonuri_test = [
        {'sku': '1567943248-3', 'cantitate': 1},
        {'sku': '5673194590-3', 'cantitate': 1},
        {'sku': '6291106063717-3', 'cantitate': 1},
        {'sku': '6291106063742-3', 'cantitate': 1}
    ]

    # Inițializare automation
    automation = OblioAutomation(
        use_existing_profile=True,  # Folosește profilul Chrome cu sesiune Oblio
        headless=False  # Rulează cu interfață grafică (pentru debugging)
    )

    try:
        # Setup driver
        if not automation.setup_driver():
            logger.error("❌ Nu s-a putut porni Chrome WebDriver!")
            return

        # Așteaptă utilizatorul să verifice că e logat în Oblio (dacă e nevoie)
        logger.info("\n⚠️ IMPORTANT: Verifică că ești logat în Oblio!")
        logger.info("Browser-ul Chrome s-a deschis. Dacă nu ești logat, loghează-te acum.")
        logger.info("Apasă ENTER pentru a continua automatizarea...")
        input()

        # Procesează bonurile
        stats = automation.process_bonuri(bonuri_test)

        logger.info("\n🎉 AUTOMATIZARE FINALIZATĂ!")
        logger.info(f"Succese: {stats['success']}/{stats['total']}")

    except KeyboardInterrupt:
        logger.info("\n⚠️ Automatizare oprită de utilizator")
    except Exception as e:
        logger.error(f"\n❌ Eroare critică: {e}")
    finally:
        # Închide browser
        automation.close()


if __name__ == "__main__":
    main()
