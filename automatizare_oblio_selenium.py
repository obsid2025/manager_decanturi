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

    def __init__(self, use_existing_profile=True, headless=False, log_callback=None, input_callback=None):
        """
        Inițializare automation

        Args:
            use_existing_profile (bool): Folosește profilul Chrome existent (cu sesiune Oblio)
            headless (bool): Rulează în mod headless (fără interfață grafică)
            log_callback (callable): Funcție pentru logging live: log_callback(message, level)
            input_callback (callable): Funcție pentru input interactiv: input_callback(prompt_dict) -> str
        """
        self.driver = None
        self.use_existing_profile = use_existing_profile
        self.headless = headless
        self.log_callback = log_callback
        self.input_callback = input_callback
        self.stats = {
            'total': 0,
            'success': 0,
            'failed': 0,
            'errors': []
        }

    def _log(self, message, level='info'):
        """
        Log message prin callback sau logger standard

        Args:
            message (str): Mesajul de logat
            level (str): Nivelul: 'info', 'warning', 'error', 'success'
        """
        # Trimite către callback dacă există
        if self.log_callback:
            try:
                self.log_callback(message, level)
            except Exception as e:
                logger.warning(f"⚠️ Eroare la log_callback: {e}")

        # Loghează și în logger standard
        if level == 'error':
            logger.error(message)
        elif level == 'warning':
            logger.warning(message)
        elif level == 'success':
            logger.info(message)
        else:
            logger.info(message)

    def _request_input(self, prompt_dict):
        """
        Cere input de la utilizator prin callback sau input() standard

        Args:
            prompt_dict (dict): Dicționar cu 'type' ('email', 'password', '2fa') și 'message'

        Returns:
            str: Input-ul utilizatorului
        """
        if self.input_callback:
            try:
                return self.input_callback(prompt_dict)
            except Exception as e:
                self._log(f"⚠️ Eroare la input_callback: {e}", 'warning')
                return None
        else:
            # Fallback la input() standard
            return input(f"{prompt_dict['message']}: ")


    def interactive_login(self):
        """
        Autentificare interactivă prin callback (suportă 2FA)

        Returns:
            bool: True dacă login reușit
        """
        self._log("🔐 Începere autentificare interactivă...", 'info')

        try:
            # Navighează la pagina de login
            login_url = "https://www.oblio.eu/login/"
            self._log(f"🌐 Navigare la: {login_url}", 'info')
            self.driver.get(login_url)
            time.sleep(2)

            # Verifică dacă suntem deja logați
            if "login" not in self.driver.current_url.lower():
                self._log("✅ Deja autentificat în Oblio!", 'success')
                return True

            # Acceptă cookie consent popup dacă există
            try:
                self._log("🍪 Verificare cookie consent popup...", 'info')
                cookie_button = WebDriverWait(self.driver, 5).until(
                    EC.element_to_be_clickable((By.ID, 'CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll'))
                )
                cookie_button.click()
                self._log("✅ Cookie consent acceptat!", 'success')
                time.sleep(1)
            except TimeoutException:
                self._log("ℹ️ Cookie consent nu a apărut (deja acceptat)", 'info')
            except Exception as e:
                self._log(f"⚠️ Eroare la cookie consent: {str(e)[:100]}", 'warning')

            # STEP 1: Cere email
            self._log("📧 Se așteaptă email-ul...", 'info')
            email = self._request_input({
                'type': 'email',
                'message': '📧 Introdu email-ul pentru Oblio'
            })

            if not email:
                raise Exception("Email-ul nu a fost furnizat!")

            self._log(f"✅ Email primit: {email}", 'info')

            # Găsește și completează câmpul de email
            email_input = self.wait_for_element(By.ID, "username", timeout=10)
            if not email_input:
                email_input = self.wait_for_element(By.NAME, "username", timeout=5)
            if not email_input:
                email_input = self.wait_for_element(By.CSS_SELECTOR, "input[type='email']", timeout=5)

            if not email_input:
                raise Exception("Câmpul de email nu a fost găsit!")

            email_input.clear()
            email_input.send_keys(email)
            time.sleep(0.5)

            # STEP 2: Cere parolă
            self._log("🔑 Se așteaptă parola...", 'info')
            password = self._request_input({
                'type': 'password',
                'message': '🔑 Introdu parola pentru Oblio'
            })

            if not password:
                raise Exception("Parola nu a fost furnizată!")

            self._log("✅ Parolă primită", 'info')

            # Găsește și completează câmpul de parolă
            password_input = self.wait_for_element(By.ID, "password", timeout=10)
            if not password_input:
                password_input = self.wait_for_element(By.NAME, "password", timeout=5)
            if not password_input:
                password_input = self.wait_for_element(By.CSS_SELECTOR, "input[type='password']", timeout=5)

            if not password_input:
                raise Exception("Câmpul de parolă nu a fost găsit!")

            password_input.clear()
            password_input.send_keys(password)
            time.sleep(0.5)

            # Găsește și click buton login
            self._log("🖱️ Click pe butonul de login...", 'info')
            login_button = None
            login_selectors = [
                (By.ID, "login-button"),
                (By.CSS_SELECTOR, "button[type='submit']"),
                (By.CSS_SELECTOR, "input[type='submit']"),
                (By.XPATH, "//button[contains(text(), 'Login')]"),
                (By.XPATH, "//button[contains(text(), 'Autentificare')]"),
            ]

            for by, selector in login_selectors:
                try:
                    login_button = self.wait_for_clickable(by, selector, timeout=3)
                    if login_button:
                        break
                except:
                    continue

            if not login_button:
                # Încearcă ENTER
                password_input.send_keys(Keys.ENTER)
            else:
                login_button.click()

            time.sleep(3)

            # Verifică dacă există erori de autentificare
            try:
                error_selectors = [
                    (By.CSS_SELECTOR, ".alert-danger"),
                    (By.CSS_SELECTOR, ".error"),
                    (By.XPATH, "//*[contains(text(), 'incorect')]"),
                    (By.XPATH, "//*[contains(text(), 'greșit')]"),
                    (By.XPATH, "//*[contains(text(), 'invalid')]"),
                ]

                for by, selector in error_selectors:
                    try:
                        error_elem = self.driver.find_element(by, selector)
                        if error_elem.is_displayed():
                            error_text = error_elem.text
                            self._log(f"❌ EROARE AUTENTIFICARE: {error_text}", 'error')
                            self._log("🔄 Email sau parolă incorectă! Rulează din nou automation-ul și introdu credențialele corecte.", 'error')
                            raise Exception(f"Credențiale incorecte: {error_text}")
                    except NoSuchElementException:
                        continue
            except Exception as e:
                if "Credențiale incorecte" in str(e):
                    raise  # Re-raise dacă e eroarea noastră
                # Altfel ignoră - poate nu există elementele de eroare

            # STEP 3: Verifică dacă e nevoie de 2FA
            current_url = self.driver.current_url
            self._log(f"🌐 URL după login: {current_url}", 'info')

            # Caută câmp 2FA
            two_fa_input = None
            try:
                two_fa_selectors = [
                    (By.ID, "sms_code"),  # Oblio folosește acest ID pentru 2FA
                    (By.ID, "two_factor_code"),
                    (By.ID, "2fa_code"),
                    (By.NAME, "code"),
                    (By.CSS_SELECTOR, "input[type='text'][maxlength='6']"),
                    (By.CSS_SELECTOR, "input[placeholder*='code']"),
                ]

                for by, selector in two_fa_selectors:
                    try:
                        two_fa_input = self.driver.find_element(by, selector)
                        if two_fa_input.is_displayed():
                            break
                        else:
                            two_fa_input = None
                    except:
                        continue
            except:
                pass

            # Dacă există câmp 2FA, cere codul
            if two_fa_input:
                self._log("🔢 2FA detectat! Se așteaptă codul...", 'warning')
                two_fa_code = self._request_input({
                    'type': '2fa',
                    'message': '🔢 Introdu codul 2FA (6 cifre)'
                })

                if not two_fa_code:
                    raise Exception("Codul 2FA nu a fost furnizat!")

                self._log("✅ Cod 2FA primit", 'info')

                # Completează codul 2FA
                two_fa_input.clear()
                two_fa_input.send_keys(two_fa_code)
                time.sleep(0.5)

                # Găsește buton submit 2FA
                submit_2fa_button = None
                submit_selectors = [
                    (By.CSS_SELECTOR, "button[type='submit']"),
                    (By.ID, "submit_2fa"),
                    (By.XPATH, "//button[contains(text(), 'Verify')]"),
                    (By.XPATH, "//button[contains(text(), 'Verifică')]"),
                ]

                for by, selector in submit_selectors:
                    try:
                        submit_2fa_button = self.wait_for_clickable(by, selector, timeout=3)
                        if submit_2fa_button:
                            break
                    except:
                        continue

                if submit_2fa_button:
                    submit_2fa_button.click()
                else:
                    two_fa_input.send_keys(Keys.ENTER)

                time.sleep(3)

            # STEP 4: Verifică succesul
            current_url = self.driver.current_url
            if "login" not in current_url.lower() and "dashboard" in current_url or "stock" in current_url or "home" in current_url:
                self._log("✅ Autentificare reușită în Oblio!", 'success')
                return True
            elif "login" not in current_url.lower():
                self._log("✅ Autentificare reușită!", 'success')
                return True
            else:
                raise Exception("Login eșuat - încă pe pagina de login")

        except Exception as e:
            self._log(f"❌ Eroare la autentificare: {e}", 'error')
            return False

    def setup_driver(self):
        """Configurare și pornire Chrome WebDriver"""
        self._log("🔧 Configurare Chrome WebDriver...", 'info')

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

            logger.info("👁️ Mod headless activat (server)")

        elif is_windows:
            # Configurare pentru Windows (local development)
            logger.info("🪟 Configurare pentru Windows...")

            # DEBUGGING MODE: Încearcă să se conecteze la Chrome existent cu remote debugging
            # Pornește Chrome manual cu: chrome.exe --remote-debugging-port=9222
            if self.use_existing_profile:
                try:
                    logger.info("🔍 Încerc să mă conectez la Chrome cu remote debugging (port 9222)...")
                    chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
                    logger.info("✅ Configurare remote debugging activată")
                    logger.info("📌 IMPORTANT: Asigură-te că Chrome rulează cu --remote-debugging-port=9222")
                except Exception as e:
                    logger.warning(f"⚠️ Nu pot configura remote debugging: {e}")
                    logger.info("📌 Voi porni un Chrome nou cu profil...")
                    
                    # Fallback: folosește profilul Chrome (ca înainte)
                    username = os.environ.get('USERNAME', 'ukfdb')
                    user_data_dir = f"C:\\Users\\{username}\\AppData\\Local\\Google\\Chrome\\User Data"

                    if os.path.exists(user_data_dir):
                        chrome_options.add_argument(f"user-data-dir={user_data_dir}")
                        chrome_options.add_argument("profile-directory=Default")
                        logger.info(f"📂 Folosesc profilul Chrome: {user_data_dir}")
                    else:
                        logger.warning(f"⚠️ Profilul Chrome nu există: {user_data_dir}")

            # NICIODATĂ headless pe Windows pentru debugging
            if self.headless:
                logger.warning("⚠️ Headless dezactivat pe Windows pentru debugging vizual")
                self.headless = False

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
                chromedriver_path = os.environ.get('CHROMEDRIVER_PATH', '/usr/bin/chromedriver')

                # Verifică dacă ChromeDriver există
                if os.path.exists(chromedriver_path):
                    service = Service(chromedriver_path)
                    self.driver = webdriver.Chrome(service=service, options=chrome_options)
                    logger.info(f"✅ Chromium WebDriver pornit cu succes (Linux)! Path: {chromedriver_path}")
                else:
                    # Încearcă fără service explicit (pentru snap pe Ubuntu)
                    logger.warning(f"⚠️ ChromeDriver nu găsit la {chromedriver_path}, încerc autodetectare...")
                    self.driver = webdriver.Chrome(options=chrome_options)
                    logger.info("✅ Chromium WebDriver pornit cu succes (Linux - autodetectat)!")
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
            logger.error(f"💡 Asigură-te că: Chromium și ChromeDriver sunt instalate")

            # Log paths pentru debugging
            if is_linux:
                chromedriver_path = os.environ.get('CHROMEDRIVER_PATH', '/usr/bin/chromedriver')
                chrome_bin = os.environ.get('CHROME_BIN', '/usr/bin/chromium')
                logger.error(f"🔍 ChromeDriver path: {chromedriver_path} (exists: {os.path.exists(chromedriver_path)})")
                logger.error(f"🔍 Chrome binary: {chrome_bin} (exists: {os.path.exists(chrome_bin)})")

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

    def load_cookies_from_json(self, cookies_json):
        """
        Încarcă cookies din JSON în browser pentru sesiune Oblio

        Args:
            cookies_json (str or dict): Cookies în format JSON

        Returns:
            bool: True dacă cookies au fost încărcate cu succes
        """
        logger.info("🍪 Începere încărcare cookies în browser...")
        
        try:
            # Parse cookies dacă e string
            if isinstance(cookies_json, str):
                cookies = json.loads(cookies_json)
            else:
                cookies = cookies_json
            
            # Navighează la domeniul Oblio mai întâi (necesar pentru a seta cookies)
            logger.info("🌐 Navigare la domeniul Oblio pentru a seta cookies...")
            self.driver.get("https://www.oblio.eu")
            time.sleep(1)
            
            # Adaugă fiecare cookie
            logger.info(f"🍪 Încărcare {len(cookies)} cookies...")
            cookies_loaded = 0
            
            for cookie in cookies:
                try:
                    # Selenium necesită doar anumite câmpuri
                    cookie_dict = {
                        'name': cookie['name'],
                        'value': cookie['value'],
                        'domain': cookie.get('domain', '.oblio.eu'),
                    }
                    
                    # Adaugă câmpuri opționale dacă există
                    if 'path' in cookie:
                        cookie_dict['path'] = cookie['path']
                    if 'secure' in cookie:
                        cookie_dict['secure'] = cookie['secure']
                    if 'httpOnly' in cookie:
                        cookie_dict['httpOnly'] = cookie['httpOnly']
                    if 'sameSite' in cookie:
                        cookie_dict['sameSite'] = cookie['sameSite']
                    
                    self.driver.add_cookie(cookie_dict)
                    cookies_loaded += 1
                    logger.debug(f"✅ Cookie încărcat: {cookie['name']}")
                    
                except Exception as e:
                    logger.warning(f"⚠️ Nu pot încărca cookie {cookie.get('name', 'unknown')}: {e}")
            
            logger.info(f"✅ {cookies_loaded}/{len(cookies)} cookies încărcate cu succes!")
            
            # Refresh pagina pentru a aplica cookies
            logger.info("🔄 Refresh pagină pentru aplicare cookies...")
            self.driver.refresh()
            time.sleep(2)
            
            # Verifică dacă suntem autentificați
            current_url = self.driver.current_url
            if "login" not in current_url.lower():
                logger.info("✅ Cookies aplicate cu succes - sesiune activă!")
                return True
            else:
                logger.warning("⚠️ Încă pe pagina de login după aplicare cookies")
                return False
                
        except Exception as e:
            logger.error(f"❌ Eroare la încărcarea cookies: {e}")
            return False

    def wait_for_manual_login(self, timeout=90):
        """
        Așteaptă ca utilizatorul să se logheze manual (inclusiv 2FA)
        
        Args:
            timeout (int): Timeout în secunde pentru login manual
            
        Returns:
            bool: True dacă utilizatorul s-a logat cu succes
        """
        logger.info("👤 Așteaptă login manual...")
        logger.info(f"⏰ Ai {timeout} secunde să te loghezi în Oblio (inclusiv 2FA)")
        logger.info("🌐 Browser-ul va fi deschis - loghează-te acum!")
        
        # Navighează la pagina de login
        login_url = "https://www.oblio.eu/login/"
        logger.info(f"🌐 Navigare la: {login_url}")
        self.driver.get(login_url)
        time.sleep(2)
        
        # Așteaptă ca utilizatorul să se logheze
        start_time = time.time()
        logged_in = False
        
        while time.time() - start_time < timeout:
            current_url = self.driver.current_url
            
            # Verifică dacă nu mai suntem pe pagina de login
            if "login" not in current_url.lower():
                logger.info(f"✅ Login detectat! URL curent: {current_url}")
                logged_in = True
                break
            
            # Verifică periodic
            elapsed = int(time.time() - start_time)
            remaining = timeout - elapsed
            
            if elapsed % 10 == 0:  # Log la fiecare 10 secunde
                logger.info(f"⏳ Așteaptă login... ({remaining}s rămase)")
            
            time.sleep(1)
        
        if logged_in:
            logger.info("✅ Utilizator autentificat cu succes!")
            return True
        else:
            logger.error(f"❌ Timeout - utilizatorul nu s-a autentificat în {timeout}s")
            return False

    def login_to_oblio(self, email, password):
        """
        Autentificare automată în Oblio (NU funcționează cu 2FA activat!)

        Args:
            email (str): Email-ul utilizatorului Oblio
            password (str): Parola utilizatorului Oblio

        Returns:
            bool: True dacă login reușit, False altfel
        """
        logger.info("🔐 Începere autentificare automată în Oblio...")
        logger.warning("⚠️ ATENȚIE: Această metodă NU funcționează dacă 2FA este activat!")
        logger.warning("💡 Pentru 2FA, folosește metoda wait_for_manual_login()")
        
        try:
            # Navighează la pagina de login
            login_url = "https://www.oblio.eu/login/"
            logger.info(f"🌐 Navigare la: {login_url}")
            self.driver.get(login_url)
            time.sleep(2)
            
            # Verifică dacă suntem deja logați (redirectați către dashboard)
            if "dashboard" in self.driver.current_url or "stock" in self.driver.current_url:
                logger.info("✅ Deja autentificat în Oblio!")
                return True
            
            # Găsește câmpul de email
            logger.info("🔍 Căutare câmp email...")
            email_input = self.wait_for_element(By.ID, "username", timeout=10)
            if not email_input:
                # Încearcă alte selectoare
                email_input = self.wait_for_element(By.NAME, "username", timeout=5)
            if not email_input:
                email_input = self.wait_for_element(By.CSS_SELECTOR, "input[type='email']", timeout=5)
            
            if not email_input:
                raise Exception("Câmpul de email nu a fost găsit!")
            
            logger.info("✅ Câmp email găsit")
            email_input.clear()
            email_input.send_keys(email)
            logger.info(f"⌨️ Email introdus: {email}")
            time.sleep(0.5)
            
            # Găsește câmpul de parolă
            logger.info("🔍 Căutare câmp parolă...")
            password_input = self.wait_for_element(By.ID, "password", timeout=10)
            if not password_input:
                password_input = self.wait_for_element(By.NAME, "password", timeout=5)
            if not password_input:
                password_input = self.wait_for_element(By.CSS_SELECTOR, "input[type='password']", timeout=5)
            
            if not password_input:
                raise Exception("Câmpul de parolă nu a fost găsit!")
            
            logger.info("✅ Câmp parolă găsit")
            password_input.clear()
            password_input.send_keys(password)
            logger.info("⌨️ Parolă introdusă")
            time.sleep(0.5)
            
            # Verifică și închide cookie banner dacă există
            try:
                logger.info("🍪 Verificare cookie banner...")
                cookie_accept_selectors = [
                    (By.ID, "CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll"),
                    (By.CSS_SELECTOR, ".CybotCookiebotDialogBodyButton"),
                    (By.XPATH, "//button[contains(text(), 'Accept')]"),
                    (By.XPATH, "//button[contains(text(), 'Acceptă')]"),
                ]
                
                for by, selector in cookie_accept_selectors:
                    try:
                        cookie_button = self.driver.find_element(by, selector)
                        if cookie_button.is_displayed():
                            logger.info("🍪 Click pe buton 'Accept Cookies'...")
                            cookie_button.click()
                            time.sleep(1)
                            break
                    except:
                        continue
            except:
                logger.debug("ℹ️ Nu există cookie banner")
            
            # Găsește și apasă butonul de login
            logger.info("🔍 Căutare buton login...")
            login_button = None
            login_selectors = [
                (By.ID, "login-button"),
                (By.CSS_SELECTOR, "button[type='submit']"),
                (By.CSS_SELECTOR, "input[type='submit']"),
                (By.XPATH, "//button[contains(text(), 'Login')]"),
                (By.XPATH, "//button[contains(text(), 'Autentificare')]"),
                (By.CSS_SELECTOR, ".btn-login"),
            ]
            
            for by, selector in login_selectors:
                try:
                    login_button = self.wait_for_clickable(by, selector, timeout=3)
                    if login_button:
                        logger.info(f"✅ Buton login găsit: {selector}")
                        break
                except:
                    continue
            
            if not login_button:
                # Încearcă să dai ENTER pe câmpul de parolă
                logger.info("⚠️ Buton login nu găsit, încerc ENTER...")
                password_input.send_keys(Keys.ENTER)
            else:
                logger.info("🖱️ Click pe butonul de login...")
                login_button.click()
            
            # Așteaptă să se încarce pagina după login
            time.sleep(3)
            
            # Verifică dacă login-ul a reușit
            current_url = self.driver.current_url
            logger.info(f"🌐 URL curent după login: {current_url}")
            
            # Verifică dacă suntem pe dashboard sau stock
            if "dashboard" in current_url or "stock" in current_url or "home" in current_url:
                logger.info("✅ Autentificare reușită în Oblio!")
                return True
            
            # Verifică dacă există mesaj de eroare
            error_elements = self.driver.find_elements(By.CSS_SELECTOR, ".alert-danger, .error, .alert-error")
            if error_elements:
                error_msg = error_elements[0].text
                logger.error(f"❌ Eroare la autentificare: {error_msg}")
                raise Exception(f"Login eșuat: {error_msg}")
            
            # Dacă suntem încă pe pagina de login, probabil e o eroare
            if "login" in current_url:
                raise Exception("Login eșuat - încă pe pagina de login")
            
            logger.warning("⚠️ Nu pot confirma 100% login-ul, dar continui...")
            return True
            
        except Exception as e:
            logger.error(f"❌ Eroare la autentificare: {e}")
            
            # Screenshot pentru debugging
            try:
                screenshot_path = f"error_login_{int(time.time())}.png"
                self.driver.save_screenshot(screenshot_path)
                logger.info(f"📸 Screenshot salvat: {screenshot_path}")
            except:
                pass
            
            return False

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

    def create_production_voucher(self, sku, quantity, oblio_cookies=None, oblio_email=None, oblio_password=None):
        """
        Creează un bon de producție în Oblio

        Args:
            sku (str): Codul SKU al produsului
            quantity (int): Cantitatea
            oblio_cookies (str/dict): Cookies Oblio pentru sesiune (PREFERAT - pe Linux)
            oblio_email (str): Email Oblio (fallback pentru autentificare)
            oblio_password (str): Parolă Oblio (fallback pentru autentificare)

        Returns:
            bool: True dacă succès, False dacă eșec
        """
        self._log(f"{'='*60}", 'info')
        self._log(f"🎯 Creare bon: SKU={sku}, Cantitate={quantity}", 'info')
        self._log(f"{'='*60}", 'info')

        try:
            # Navighează la pagina de producție
            url = "https://www.oblio.eu/stock/production/"
            self._log(f"🌐 Navigare la: {url}", 'info')
            self.driver.get(url)
            time.sleep(2)
            
            # Verifică dacă suntem pe pagina de login (nu suntem autentificați)
            if "login" in self.driver.current_url.lower():
                self._log("⚠️ Nu suntem autentificați!", 'warning')

                # PRIORITATE 1: Încearcă cookies (dacă sunt disponibile)
                if oblio_cookies and len(oblio_cookies) > 0:
                    self._log("🍪 Încerc autentificare cu cookies...", 'info')
                    if self.load_cookies_from_json(oblio_cookies):
                        self._log("✅ Autentificare cu cookies reușită!", 'success')
                        # Navighează din nou la pagina de producție
                        self._log(f"🌐 Re-navigare la: {url}", 'info')
                        self.driver.get(url)
                        time.sleep(2)
                    else:
                        self._log("⚠️ Autentificare cu cookies eșuată", 'warning')

                # PRIORITATE 2: Login interactiv (dacă avem callback) sau login manual
                if "login" in self.driver.current_url.lower():
                    if self.input_callback:
                        # Folosește login interactiv cu callback
                        self._log("🔐 Pornire login interactiv (cu callback)...", 'info')
                        if not self.interactive_login():
                            raise Exception("Login interactiv eșuat!")
                    else:
                        # Fallback la wait_for_manual_login (fără callback)
                        self._log("👤 Voi aștepta login manual (suportă 2FA)", 'info')
                        if not self.wait_for_manual_login(timeout=90):
                            raise Exception("Login manual eșuat sau timeout!")

                    # După login, navighează la pagina de producție
                    self._log(f"🌐 Navigare la pagina de producție...", 'info')
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

            # Încearcă să închidă orice modal care ar putea bloca butonul
            try:
                logger.info("🔍 Verificare modal-uri care ar putea bloca...")
                modal_close_selectors = [
                    (By.CSS_SELECTOR, "#modal-message .ok-message-modal"),
                    (By.CSS_SELECTOR, "#modal-message .message-modal-close"),
                    (By.CSS_SELECTOR, ".modal.show .btn[data-dismiss='modal']"),
                    (By.CSS_SELECTOR, ".modal.show button[type='button']"),
                ]

                for by, selector in modal_close_selectors:
                    try:
                        modal_button = self.driver.find_element(by, selector)
                        if modal_button.is_displayed():
                            logger.info(f"✅ Modal găsit, închid: {selector}")
                            modal_button.click()
                            time.sleep(1)
                            break
                    except:
                        continue
            except Exception as e:
                logger.debug(f"ℹ️ Nu există modal de închis: {e}")

            # Click salvare
            logger.info("🖱️ Click buton salvare...")
            save_button.click()
            time.sleep(4)

            # PASUL 6: Verifică succesul REAL în baza de date Oblio
            logger.info("🔍 Verificare dacă bonul a fost creat în baza de date Oblio...")
            time.sleep(3)  # Așteptăm să se proceseze complet

            current_url = self.driver.current_url
            logger.info(f"📍 URL curent după submit: {current_url}")

            success = False
            production_id = None

            # Metodă 1: Verifică dacă am fost redirectat la preview_production (cel mai sigur indicator)
            if "/stock/preview_production/" in current_url:
                # Extragem ID-ul bonului din URL
                import re
                match = re.search(r'/preview_production/(\d+)', current_url)
                if match:
                    production_id = match.group(1)
                    logger.info(f"✅ REDIRECT LA BON NOU! ID producție: {production_id}")

                    # Verificăm că există badge de status pe pagină
                    try:
                        badge = WebDriverWait(self.driver, 5).until(
                            EC.presence_of_element_located((By.CSS_SELECTOR, ".badge"))
                        )
                        badge_text = badge.text
                        logger.info(f"✅ Status bon: {badge_text}")
                        success = True
                    except:
                        logger.warning("⚠️ Nu s-a găsit badge de status, dar URL-ul e corect")
                        success = True  # URL-ul e indicator suficient

            # Metodă 2: Dacă nu am fost redirectat, verificăm în raportul de producție
            if not success:
                logger.info("🔍 Navigare la raportul de producție pentru verificare...")
                self.driver.get("https://www.oblio.eu/report/production")
                time.sleep(3)

                # Căutăm un bon cu data de azi și SKU-ul nostru
                from datetime import datetime
                today = datetime.now().strftime("%d.%m.%Y")
                logger.info(f"🔍 Căutare bon cu data {today} și SKU {sku}...")

                try:
                    # Căutăm în tabel un rând care conține data de azi
                    rows = self.driver.find_elements(By.CSS_SELECTOR, "#content-table tbody tr.table_row")
                    logger.info(f"📊 Găsite {len(rows)} bonuri în raport")

                    for row in rows[:10]:  # Verificăm primele 10 bonuri (cele mai recente)
                        try:
                            # Verificăm data
                            date_elem = row.find_element(By.CSS_SELECTOR, ".text-muted")
                            date_text = date_elem.text.strip()

                            if today in date_text:
                                logger.info(f"🔍 Găsit bon cu data de azi: {date_text}")

                                # Verificăm SKU-ul (există în text sau în link)
                                row_text = row.text.lower()
                                sku_lower = sku.lower()

                                # Căutăm SKU-ul în textul rândului
                                if sku_lower in row_text or sku.replace("-", " ").lower() in row_text:
                                    # Extragem numărul bonului
                                    bon_link = row.find_element(By.CSS_SELECTOR, "a.font-bold")
                                    bon_number = bon_link.text.strip()

                                    logger.info(f"✅ GĂSIT BON NOU! {bon_number} din {date_text}")
                                    logger.info(f"✅ Conține SKU: {sku}")

                                    # Extragem ID-ul din link
                                    bon_href = bon_link.get_attribute('href')
                                    match = re.search(r'/preview_production/(\d+)', bon_href)
                                    if match:
                                        production_id = match.group(1)
                                        logger.info(f"✅ ID producție: {production_id}")

                                    success = True
                                    break
                        except Exception as e:
                            logger.debug(f"⏭️ Rând ignorat: {e}")
                            continue

                    if not success:
                        logger.warning(f"⚠️ NU s-a găsit niciun bon nou cu data {today} și SKU {sku}")

                except Exception as e:
                    logger.error(f"❌ Eroare la verificarea raportului: {e}")

            # Rezultat final
            if success:
                msg = f"🎉 BON CREAT CU SUCCES! SKU={sku}, Cantitate={quantity}"
                if production_id:
                    msg += f", ID={production_id}"
                self._log(msg, 'success')
                self.stats['success'] += 1
                return True
            else:
                self._log(f"❌ BONUL NU A FOST CREAT! SKU={sku} nu apare în raportul de producție", 'error')
                self.stats['failed'] += 1
                self.stats['errors'].append({
                    'sku': sku,
                    'quantity': quantity,
                    'error': 'Bon nu a fost găsit în raportul de producție după submit'
                })
                return False

        except Exception as e:
            self._log(f"❌ EROARE la crearea bonului: {e}", 'error')
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
                self._log(f"📸 Screenshot salvat: {screenshot_path}", 'info')
            except:
                pass

            return False

    def process_bonuri(self, bonuri, oblio_cookies=None, oblio_email=None, oblio_password=None):
        """
        Procesează o listă de bonuri

        Args:
            bonuri (list): Lista de dicționare cu 'sku' și 'cantitate'
            oblio_cookies (str/dict): Cookies Oblio pentru sesiune (PREFERAT)
            oblio_email (str): Email Oblio (fallback pentru autentificare)
            oblio_password (str): Parolă Oblio (fallback pentru autentificare)

        Returns:
            dict: Statistici procesare
        """
        self._log(f"🚀 START PROCESARE: {len(bonuri)} bonuri", 'info')
        self._log(f"{'='*60}", 'info')

        self.stats['total'] = len(bonuri)

        for i, bon in enumerate(bonuri, 1):
            sku = bon.get('sku')
            cantitate = bon.get('cantitate', 1)

            self._log(f"📦 Bon {i}/{len(bonuri)}", 'info')

            success = self.create_production_voucher(sku, cantitate, oblio_cookies, oblio_email, oblio_password)

            if success:
                self._log(f"✅ Bon {i}/{len(bonuri)} - SUCCESS", 'success')
            else:
                self._log(f"❌ Bon {i}/{len(bonuri)} - FAILED", 'error')

            # Pauză între bonuri
            if i < len(bonuri):
                self._log(f"⏳ Pauză 2 secunde înainte de următorul bon...", 'info')
                time.sleep(2)

        # Raport final
        self._log(f"{'='*60}", 'info')
        self._log(f"📊 RAPORT FINAL", 'info')
        self._log(f"{'='*60}", 'info')
        self._log(f"Total bonuri: {self.stats['total']}", 'info')
        self._log(f"✅ Succese: {self.stats['success']}", 'success')
        self._log(f"❌ Eșecuri: {self.stats['failed']}", 'error' if self.stats['failed'] > 0 else 'info')

        if self.stats['failed'] > 0:
            self._log(f"❌ Bonuri eșuate:", 'error')
            for error in self.stats['errors']:
                self._log(f"  - SKU: {error['sku']}, Eroare: {error['error']}", 'error')

        self._log(f"{'='*60}", 'info')

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
