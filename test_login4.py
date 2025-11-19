from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import base64

print("=" * 60)
print("TEST LOGIN OBLIO + 2FA (v4 - cu debug complet)")
print("=" * 60)

email = 'obsidparfume@gmail.com'
password = 'M@83LFdkc.Mgcx3'

opts = Options()
opts.add_argument('--headless=new')
opts.add_argument('--no-sandbox')
opts.add_argument('--disable-dev-shm-usage')
opts.add_argument('--window-size=1920,1080')

service = Service('/usr/bin/chromedriver')
driver = webdriver.Chrome(service=service, options=opts)
wait = WebDriverWait(driver, 15)

try:
    print("\n1. Pornire Chrome...")
    print("✅ Chrome pornit!")

    print("\n2. Navigare la Oblio...")
    driver.get('https://www.oblio.eu/login/')
    print(f"📍 URL inițial: {driver.current_url}")

    # Dismiss cookie consent popup first
    print("\n3. Aștept popup cookie consent...")
    try:
        cookie_button = wait.until(EC.element_to_be_clickable((By.ID, 'CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll')))
        cookie_button.click()
        print("✅ Cookie consent acceptat!")
        time.sleep(1)
    except Exception as e:
        print(f"⚠️  Cookie popup nu a apărut: {str(e)[:100]}")

    print("\n4. Completare câmp email...")
    email_input = wait.until(EC.element_to_be_clickable((By.ID, 'username')))
    email_input.clear()
    email_input.send_keys(email)
    print(f"✅ Email: {email}")

    print("\n5. Completare câmp password...")
    password_input = wait.until(EC.element_to_be_clickable((By.ID, 'password')))
    password_input.clear()
    password_input.send_keys(password)
    print("✅ Password: ********")

    # Take screenshot before submit
    print("\n6. Screenshot ÎNAINTE de login...")
    screenshot_before = driver.get_screenshot_as_base64()
    print(f"📸 Screenshot luat (lungime: {len(screenshot_before)} chars)")

    print("\n7. Click login...")
    login_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[type="submit"]')))
    login_button.click()
    print("✅ Buton login apăsat!")

    print("\n8. Aștept 12 secunde pentru răspuns server...")
    time.sleep(12)

    # Check URL after login
    current_url = driver.current_url
    print(f"\n📍 URL după login: {current_url}")

    # Take screenshot after submit
    print("\n9. Screenshot DUPĂ login...")
    screenshot_after = driver.get_screenshot_as_base64()
    print(f"📸 Screenshot luat (lungime: {len(screenshot_after)} chars)")

    # Check for error messages
    print("\n10. Verific mesaje de eroare...")
    try:
        error_elements = driver.find_elements(By.CLASS_NAME, 'error')
        if error_elements:
            for err in error_elements:
                if err.is_displayed():
                    print(f"❌ EROARE GĂSITĂ: {err.text}")
    except:
        pass

    try:
        alert_elements = driver.find_elements(By.CLASS_NAME, 'alert')
        if alert_elements:
            for alert in alert_elements:
                if alert.is_displayed():
                    print(f"⚠️  ALERT: {alert.text}")
    except:
        pass

    # Check for 2FA popup
    print("\n11. Verific dacă există popup 2FA...")
    try:
        sms_input = driver.find_element(By.ID, 'sms_code')
        if sms_input.is_displayed():
            print("\n" + "=" * 60)
            print("🎉 SUCCES! POPUP 2FA GĂSIT ȘI VIZIBIL!")
            print("📱 VERIFICĂ TELEFONUL PENTRU SMS!")
            print("=" * 60)

            # Check if it's really a popup (modal)
            parent = sms_input.find_element(By.XPATH, './ancestor::div[contains(@class, "modal")]')
            if parent:
                print(f"✅ Confirmat: Este într-un modal dialog")
        else:
            print("⚠️  Element #sms_code există dar NU este vizibil")
    except Exception as e:
        print(f"❌ Popup 2FA NU a fost găsit: {str(e)[:150]}")

        # Debug: check what's on the page
        print("\n🔍 DEBUG - Verificare pagină curentă:")
        if 'login' in current_url:
            print("❌ ÎNCĂ PE PAGINA DE LOGIN - probabil credențiale greșite!")
        elif 'dashboard' in current_url or 'home' in current_url:
            print("✅ Redirectat la dashboard - login FĂRĂ 2FA?")
        else:
            print(f"📍 URL necunoscut: {current_url}")

        # Check page source for common error indicators
        page_source = driver.page_source
        if 'incorect' in page_source.lower() or 'invalid' in page_source.lower():
            print("❌ Pagina conține text despre eroare de autentificare")

    print("\n12. Title pagină: " + driver.title)

except Exception as e:
    print(f"\n❌ EROARE CRITICĂ: {e}")
    import traceback
    traceback.print_exc()

finally:
    print("\n13. Închidere...")
    driver.quit()
    print("DONE")
