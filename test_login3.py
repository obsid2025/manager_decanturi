from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

print("=" * 60)
print("TEST LOGIN OBLIO + 2FA (v3 - cu cookie consent)")
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

    # Dismiss cookie consent popup first
    print("\n3. Aștept popup cookie consent...")
    try:
        cookie_button = wait.until(EC.element_to_be_clickable((By.ID, 'CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll')))
        cookie_button.click()
        print("✅ Cookie consent acceptat!")
        time.sleep(1)  # Small delay after dismissing
    except Exception as e:
        print(f"⚠️  Cookie popup nu a apărut sau deja acceptat: {e}")

    print("\n4. Aștept câmp email să fie clickable...")
    email_input = wait.until(EC.element_to_be_clickable((By.ID, 'username')))
    email_input.clear()
    email_input.send_keys(email)
    print(f"✅ Email: {email}")

    print("\n5. Aștept câmp password să fie clickable...")
    password_input = wait.until(EC.element_to_be_clickable((By.ID, 'password')))
    password_input.clear()
    password_input.send_keys(password)
    print("✅ Password: ********")

    print("\n6. Click login...")
    login_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[type="submit"]')))
    login_button.click()
    print("✅ Buton login apăsat!")

    print("\n7. Aștept 10 secunde pentru popup 2FA...")
    time.sleep(10)

    print("\n8. Verific dacă există popup 2FA...")
    try:
        sms_input = driver.find_element(By.ID, 'sms_code')
        if sms_input.is_displayed():
            print("\n" + "=" * 60)
            print("🎉 SUCCES! POPUP 2FA GĂSIT!")
            print("📱 VERIFICĂ TELEFONUL PENTRU SMS!")
            print("=" * 60)
        else:
            print("⚠️  Element #sms_code există dar nu este vizibil")
    except Exception as e:
        print(f"❌ Popup 2FA nu a fost găsit: {e}")

        # Debug: print page source to see what's there
        print("\n🔍 DEBUG - Verificare pagină:")
        if 'login' in driver.current_url:
            print("❌ Încă pe pagina de login - probabil credențiale greșite")
        else:
            print(f"📍 URL curent: {driver.current_url}")

except Exception as e:
    print(f"\n❌ EROARE: {e}")

finally:
    print("\n9. Închidere...")
    driver.quit()
    print("DONE")
