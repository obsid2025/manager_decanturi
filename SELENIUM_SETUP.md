# Ghid Instalare și Utilizare - Automatizare Oblio cu Selenium

## 📋 Prezentare Generală

Acest sistem automatizează crearea bonurilor de producție în Oblio folosind **Python Selenium WebDriver**.
Browser-ul Chrome va fi controlat automat pentru a completa formularele și crea bonurile.

---

## 🔧 Instalare

### 1. Instalare ChromeDriver

ChromeDriver este necesar pentru ca Selenium să controleze Chrome.

**Metoda 1: Instalare automată (Recomandată)**

```bash
pip install webdriver-manager
```

Apoi modifică `automatizare_oblio_selenium.py` la linia 88:

```python
from webdriver_manager.chrome import ChromeDriverManager

# Înlocuiește:
self.driver = webdriver.Chrome(options=chrome_options)

# Cu:
self.driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=chrome_options
)
```

**Metoda 2: Instalare manuală**

1. Verifică versiunea Chrome:
   - Deschide Chrome
   - Accesează `chrome://settings/help`
   - Notează versiunea (ex: 120.0.6099.109)

2. Descarcă ChromeDriver:
   - Accesează https://googlechromelabs.github.io/chrome-for-testing/
   - Descarcă versiunea corespunzătoare pentru Windows
   - Extrage `chromedriver.exe`

3. Adaugă ChromeDriver în PATH:
   - Copiază `chromedriver.exe` în `C:\Windows\System32\`
   - SAU adaugă directorul în PATH

4. Verifică instalarea:
   ```bash
   chromedriver --version
   ```

### 2. Instalare Dependințe Python

```bash
pip install selenium
```

### 3. Verificare Instalare

Rulează testul:

```bash
python automatizare_oblio_selenium.py
```

Dacă Chrome se deschide, instalarea e reușită!

---

## 🚀 Utilizare

### 1. Pornire Aplicație

```bash
python app.py
```

Aplicația va porni pe `http://localhost:5000`

### 2. Procesare Fișier Excel

1. Accesează `http://localhost:5000` în browser
2. Click pe **"Alege fișier Excel"**
3. Selectează fișierul cu comenzi (trebuie să conțină coloana SKU)
4. Click **"PROCESEAZĂ EXCEL"**
5. Verifică previzualizarea bonurilor

### 3. Pornire Automatizare

1. **IMPORTANT**: Asigură-te că ești logat în Oblio în Chrome!
   - Deschide Chrome
   - Accesează https://www.oblio.eu
   - Loghează-te în contul Oblio
   - Lasă tab-ul deschis

2. Click pe butonul **"START AUTOMATIZARE (SELENIUM)"**

3. Confirmă în dialog:
   - Verifică că numărul de bonuri e corect
   - Confirmă că ești logat în Oblio
   - Click **OK**

4. **NU închide browser-ul Chrome** în timpul procesării!

5. Așteaptă finalizarea:
   - Chrome se va deschide automat
   - Vei vedea procesarea în timp real
   - Pentru fiecare bon:
     - Se accesează pagina de producție
     - Se completează SKU-ul
     - Se selectează din autocomplete
     - Se completează cantitatea
     - Se salvează bonul

6. La final, vei vedea un raport cu:
   - Număr total bonuri
   - Bonuri create cu succes
   - Bonuri eșuate (dacă există)

---

## 📊 Log-uri și Debugging

### Log-uri Aplicație

Toate acțiunile sunt înregistrate în:

```
automatizare_oblio.log
```

Conținut log:
- Timestamp pentru fiecare acțiune
- Progres procesare (Bon X/Y)
- SKU-uri procesate
- Cantități introduse
- Erori (dacă există)

### Screenshot-uri Erori

Dacă apare o eroare, se salvează automat un screenshot:

```
error_screenshot_<SKU>_<timestamp>.png
```

Folosește acest screenshot pentru a identifica problema.

---

## ⚠️ Troubleshooting

### Eroare: "ChromeDriver nu a fost găsit"

**Cauză**: ChromeDriver nu e instalat sau nu e în PATH.

**Soluție**:
1. Verifică instalarea: `chromedriver --version`
2. Dacă lipsește, reinstalează (vezi secțiunea Instalare)
3. SAU folosește `webdriver-manager` (Metoda 1)

---

### Eroare: "Chrome failed to start"

**Cauză**: Path-ul către profilul Chrome e incorect.

**Soluție**: Modifică linia 68 în `automatizare_oblio_selenium.py`:

```python
# Înlocuiește %USERNAME% cu username-ul tău real:
user_data_dir = r"C:\Users\TauUsername\AppData\Local\Google\Chrome\User Data"
```

Pentru a găsi username-ul:
```bash
echo %USERNAME%
```

---

### Eroare: "Nu s-a putut găsi elementul #pp_name"

**Cauză**: Pagina Oblio nu s-a încărcat complet SAU nu ești logat.

**Soluție**:
1. Verifică că ești logat în Oblio în Chrome
2. Accesează manual https://www.oblio.eu/stock/production/ pentru a verifica
3. Crește timeout-ul în cod (linia 177):
   ```python
   pp_name_input = self.wait_for_element(By.ID, "pp_name", timeout=30)
   ```

---

### Eroare: "Produsul cu SKU 'XXX' nu a fost selectat"

**Cauză**: SKU-ul nu există în baza de date Oblio SAU autocomplete-ul nu a funcționat.

**Soluție**:
1. Verifică în Oblio că produsul cu acel SKU există
2. Verifică că SKU-ul e scris corect (case-sensitive)
3. Încearcă să crești delay-ul la tastare (linia 186):
   ```python
   self.type_slowly(pp_name_input, sku, delay=0.15)  # Mai lent
   ```

---

### Bonuri create parțial

**Cauză**: Unele SKU-uri sunt invalide sau lipsesc din Oblio.

**Soluție**:
1. Verifică raportul final în consolă:
   ```
   ✅ Succese: X
   ❌ Eșecuri: Y
   ```

2. Verifică `automatizare_oblio.log` pentru detalii:
   ```
   ❌ EROARE la crearea bonului: Produsul cu SKU 'XXX' nu a fost selectat
   ```

3. Adaugă SKU-urile lipsă în Oblio

4. Reluează procesarea doar pentru bonurile eșuate

---

### Browser-ul nu se închide la final

**Cauză**: Eroare în procesare care a prevenit închiderea corectă.

**Soluție**:
1. Închide manual Chrome
2. Verifică log-urile pentru erori
3. Adaugă în cod (după procesare):
   ```python
   automation.close()
   ```

---

## 🎯 Best Practices

### 1. Verificare înaintea Automatizării

✅ Ești logat în Oblio în Chrome
✅ Toate SKU-urile există în baza de date Oblio
✅ Conexiunea internet e stabilă
✅ Nu ai alte automatizări Chrome în desfășurare

### 2. Procesare în Loturi

Pentru comenzi mari (>50 bonuri):
- Împarte în loturi de câte 20-30
- Procesează fiecare lot separat
- Verifică succesul între loturi

### 3. Backup Date

Înainte de automatizare:
- Salvează o copie a fișierului Excel original
- Exportă bonurile existente din Oblio (pentru verificare)

### 4. Monitorizare

- Nu părăsi calculatorul în timpul procesării
- Verifică vizual că bonurile se creează corect
- La prima eroare, oprește procesarea (Ctrl+C în terminal)

---

## 🔒 Securitate

### Protecție Date Sesiune

Script-ul folosește profilul Chrome existent pentru a păstra sesiunea Oblio.
**NU** sunt salvate parole sau token-uri în fișiere.

### Rulare în Headless Mode

Pentru server fără GUI, modifică la inițializare:

```python
automation = OblioAutomation(
    use_existing_profile=True,
    headless=True  # Rulează fără GUI
)
```

**ATENȚIE**: În headless mode nu poți verifica vizual procesarea!

---

## 📈 Performance

### Viteza Procesării

- **~15-20 secunde** per bon (cu verificări complete)
- **~30 bonuri** în 10 minute
- **~180 bonuri** pe oră

### Optimizare

Pentru procesare mai rapidă, modifică delay-urile:

```python
# Linia 186 - delay tastare
self.type_slowly(pp_name_input, sku, delay=0.03)  # Mai rapid

# Linia 191 - așteptare autocomplete
time.sleep(1.5)  # Redus de la 2s

# Linia 359 - pauză între bonuri
time.sleep(1)  # Redus de la 2s
```

⚠️ **RISC**: Delay-uri prea mici pot cauza eșecuri!

---

## 🆘 Suport

### Log-uri Complete

Pentru debugging avansat, activează log-uri detaliate:

```python
# Linia 27
logging.basicConfig(
    level=logging.DEBUG,  # Schimbat de la INFO
    ...
)
```

### Informații pentru Suport

La raportarea unei probleme, include:
1. Fișierul `automatizare_oblio.log`
2. Screenshot-urile de eroare (dacă există)
3. Versiunea Chrome: `chrome://settings/help`
4. Versiunea ChromeDriver: `chromedriver --version`
5. Mesajul exact de eroare din consolă

---

## 📝 Întrebări Frecvente

### Pot rula automatizarea pe server?

Da, dar necesită:
1. Server cu GUI (Desktop Windows/Linux) SAU
2. Headless Chrome cu Xvfb (Linux)
3. ChromeDriver instalat
4. Sesiune Oblio activă (cookies salvate)

### Pot schimba browser-ul?

Da, Selenium suportă:
- Firefox (geckodriver)
- Edge (msedgedriver)

Modifică la linia 88:
```python
self.driver = webdriver.Firefox(options=firefox_options)
```

### Cât timp rămâne sesiunea Oblio activă?

Depinde de setările Oblio. Recomandare:
- Loghează-te în Oblio înainte de fiecare rulare
- Bifează "Ține-mă minte" la login

### Pot procesa bonuri din multiple fișiere Excel?

Da:
1. Procesează primul fișier
2. Click **RESETARE**
3. Încarcă următorul fișier
4. Repetă

SAU concatenează fișierele Excel înainte de încărcare.

---

## 🎉 Succes!

Acum ai un sistem complet automatizat pentru crearea bonurilor de producție în Oblio!

Pentru întrebări sau probleme: verifică log-urile și secțiunea Troubleshooting.
