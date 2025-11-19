# 🤖 OBSID Decant Manager + Automatizare Oblio

Platformă web profesională pentru procesarea comenzilor de decanturi parfumuri **cu automatizare completă pentru crearea bonurilor de producție în Oblio**.

![OBSID Logo](https://gomagcdn.ro/domains3/obsid.ro/files/company/parfumuri-arabesti8220.svg)

---

## ⚡ FUNCȚIONALITATE PRINCIPALĂ: AUTOMATIZARE OBLIO

### 🎯 Ce face?

Aplicația **creează automat bonuri de producție în Oblio** folosind **Python Selenium WebDriver** pentru control complet al browser-ului:

1. ✅ **Upload ONE-TIME**: Încarcă Excel o singură dată
2. ✅ **Procesare Automată**: Extrage SKU-uri și cantități
3. ✅ **Selenium Automation**: Control complet browser Chrome
4. ✅ **Zero Input Manual**: Toate câmpurile completate automat
5. ✅ **Session Persistence**: Folosește sesiunea Oblio existentă

### 🚀 Rezultat

**Economie de timp:** De la 2-3 ore de muncă manuală → **sub 5 minute automat**!

### 🔄 Tehnologie Folosită

**Selenium WebDriver + Chrome** (Metoda Nouă - RECOMANDATĂ)
- ✅ Control complet al browser-ului
- ✅ Fără limitări de securitate browser
- ✅ Logging detaliat și error handling
- ✅ Screenshots automate la erori
- ✅ Reutilizare sesiune Chrome existentă

---

## 🌟 Caracteristici Complete

### Tab 1: Raport Producție Decanturi
- ✅ **Upload Excel** - Încarcă fișiere cu comenzi direct din browser
- ✅ **Procesare Automată** - Exclude automat comenzile anulate
- ✅ **Extragere SKU** - Detectează SKU-uri din coloana "Atribute"
- ✅ **Raport Producție** - Vizualizare clară cu SKU, cantități, bucăți
- ✅ **Grupare Inteligentă** - Organizat pe parfum și cantitate (3ml, 5ml, 10ml)
- ✅ **Export Excel** - Descarcă raportul pentru arhivare
- ✅ **Sumar Global** - Statistici complete per parfum

### Tab 2: Bonuri de Producție (AUTOMAT)
- ✅ **Auto-Populate** - Se completează automat din datele Tab 1 (un singur upload!)
- ✅ **Agregare SKU** - Grupare inteligentă pe SKU cu cantități totale
- ✅ **Sortare Prioritate** - Cele mai solicitate produse primele
- ✅ **Copiere Rapidă** - Buton pentru copiere toate SKU-urile
- ✅ **🤖 AUTOMATIZARE SELENIUM** - Buton pentru procesare automată completă

### Sistem Automatizare Selenium (COMPLET)
- ✅ **Chrome WebDriver Control** - Control complet al browser-ului Chrome
- ✅ **Sequential Processing** - Procesare stabilă și fiabilă bon-cu-bon
- ✅ **Real-Time Logging** - Log detaliat în `automatizare_oblio.log`
- ✅ **Session Persistence** - Folosește sesiunea Oblio existentă (fără re-login)
- ✅ **Auto-Fill Forms** - Completează SKU character-by-character pentru autocomplete
- ✅ **jQuery UI Handling** - Selectare automată din dropdown autocomplete
- ✅ **Error Screenshots** - Capturează screenshot-uri automat la erori
- ✅ **Statistics Tracking** - Raport detaliat: succese/eșecuri/erori

### Help System Integrat
- ✅ **Modal Instrucțiuni** - Buton "❓ Cum funcționează?" în interfață
- ✅ **Ghid Selenium** - Documentație completă instalare și utilizare
- ✅ **Troubleshooting** - Rezolvări pentru probleme comune
- ✅ **Documentație Completă** - `SELENIUM_SETUP.md` pentru referință offline

### Design & UX
- ✅ **Design Profesional** - Temă gri/negru/alb cu logo OBSID
- ✅ **Responsive** - Funcționează pe desktop, tabletă și mobile
- ✅ **Tab Interface** - Navigare simplă între funcționalități
- ✅ **Visual Feedback** - Loading spinners, alerts, progress indicators
- ✅ **HTTPS Securizat** - SSL automat prin Coolify

---

## 🚀 Demo

**Live:** [https://decant.obsid.ro](https://decant.obsid.ro)

---

## 📖 Documentație

### 📚 Ghiduri de Utilizare

| Fișier | Descriere |
|--------|-----------|
| **SELENIUM_SETUP.md** | Ghid complet instalare și utilizare Selenium (PRINCIPAL) |
| **QUICK_START.md** | Începe în 3 minute - ghid rapid |
| **DEPLOYMENT.md** | Ghid deployment Coolify cu troubleshooting |
| **README_AUTOMATIZARE.md** | Documentație tehnică despre automatizare (versiune veche Edge) |

### 🎯 Workflow Complet

```
┌─────────────────────────────────────────────┐
│  1. Încarcă Excel în Tab 1                  │
│     → Procesează comenzi                    │
└──────────────┬──────────────────────────────┘
               ↓
┌─────────────────────────────────────────────┐
│  2. Tab 2 se completează AUTOMAT            │
│     → Verifică SKU-uri și cantități         │
└──────────────┬──────────────────────────────┘
               ↓
┌─────────────────────────────────────────────┐
│  3. Click "🤖 START AUTOMATIZARE (SELENIUM)"│
│     → Confirmă în popup                     │
└──────────────┬──────────────────────────────┘
               ↓
┌─────────────────────────────────────────────┐
│  4. Backend Flask primește request          │
│     → Pornește script Selenium Python       │
│     → Chrome se deschide automat            │
└──────────────┬──────────────────────────────┘
               ↓
┌─────────────────────────────────────────────┐
│  5. Pentru fiecare bon (secvențial):        │
│     ✅ Accesează pagina de producție        │
│     ✅ Completează SKU (char-by-char)       │
│     ✅ Așteaptă autocomplete jQuery UI      │
│     ✅ Selectează primul rezultat           │
│     ✅ Introduce cantitate                  │
│     ✅ Salvează bonul                       │
│     ✅ Verifică succes                      │
│     📝 Log detaliat la fiecare pas          │
└──────────────┬──────────────────────────────┘
               ↓
┌─────────────────────────────────────────────┐
│  6. Raport final în browser + log file:     │
│     → X bonuri create cu succes ✅          │
│     → Y bonuri eșuate (cu detalii) ❌       │
│     → Screenshot-uri la erori 📸            │
└─────────────────────────────────────────────┘
```

---

## 📋 Tehnologii

### Backend
- **Python 3.11** - Runtime
- **Flask 3.0+** - Web framework
- **Pandas 2.0+** - Excel processing
- **OpenPyXL** - Excel read/write
- **Selenium 4.x** - Browser automation
- **ChromeDriver** - Chrome WebDriver pentru Selenium

### Frontend
- **HTML5** - Structure
- **CSS3** - Styling (custom, no frameworks)
- **JavaScript (Vanilla)** - Logic și interactivitate

### Deployment
- **Docker** - Containerization
- **Coolify** - PaaS deployment
- **Nginx** - Reverse proxy (via Coolify)
- **Ubuntu 20.04+** - Server OS

---

## 🏗️ Structura Proiect

```
pregatire_decanturi/
├── 📄 Dockerfile                           # Container configuration
├── 📄 requirements.txt                     # Python dependencies
├── 📄 app.py                               # Flask application (backend)
├── 📄 automatizare_oblio_selenium.py       # ⭐ Script Selenium (PRINCIPAL)
│
├── 📁 templates/
│   └── index.html                          # Frontend UI (2 tabs + modal)
│
├── 📁 static/
│   ├── css/
│   │   └── style.css                       # Styling
│   └── js/
│       └── main.js                         # Frontend logic + automation
│
├── 📁 Documentație/
│   ├── README.md                           # Acest fișier
│   ├── SELENIUM_SETUP.md                   # ⭐ Ghid complet Selenium
│   ├── QUICK_START.md                      # Ghid rapid 3 minute
│   ├── DEPLOYMENT.md                       # Ghid deployment Coolify
│   └── README_AUTOMATIZARE.md              # Documentație tehnică (veche)
│
├── 📁 uploads/                             # Excel-uri încărcate (temporar)
├── 📁 exports/                             # Excel-uri exportate (temporar)
└── 📄 automatizare_oblio.log               # Log-uri Selenium (generat)
```

---

## 🎯 Instalare și Utilizare

### 1️⃣ Instalare Aplicație (O DATĂ)

Aplicația este deja deployed la **https://decant.obsid.ro** via Coolify.

**Pentru development local:**
```bash
git clone <repo-url>
cd pregatire_decanturi
pip install -r requirements.txt
python app.py
# Accesează: http://localhost:5000
```

### 2️⃣ Instalare ChromeDriver (O DATĂ)

**Metoda Automată (Recomandată):**
```bash
pip install webdriver-manager
```

**Metoda Manuală:**
1. Verifică versiunea Chrome: `chrome://settings/help`
2. Descarcă ChromeDriver corespunzător: https://googlechromelabs.github.io/chrome-for-testing/
3. Adaugă în PATH sau copiază în `C:\Windows\System32\`

**Verificare:**
```bash
chromedriver --version
```

### 3️⃣ Utilizare Zilnică

1. **Loghează-te în Oblio** (o dată pe sesiune în Chrome)
2. Deschide **https://decant.obsid.ro**
3. Încarcă Excel în Tab 1 → Procesează
4. Tab 2 se completează automat
5. Click **"🤖 START AUTOMATIZARE (SELENIUM)"**
6. ☕ Relaxează-te - bonurile se creează singure!
7. Verifică log-ul în `automatizare_oblio.log`

**Citește:** `SELENIUM_SETUP.md` pentru ghid complet și troubleshooting

---

## 🔧 Configurare Avansată

### Ajustare Performanță Selenium

Editează `automatizare_oblio_selenium.py`:

**1. Viteza de tastare (linia 186):**
```python
self.type_slowly(pp_name_input, sku, delay=0.08)
# Mai rapid: delay=0.05
# Mai lent (pentru conexiuni slabe): delay=0.15
```

**2. Timeout-uri (liniile 96, 117, 177):**
```python
def wait_for_element(self, by, selector, timeout=15):
    # Crește pentru conexiuni slabe: timeout=20
    # Scade pentru procesare rapidă: timeout=10
```

**3. Pauză între bonuri (linia 359):**
```python
time.sleep(2)  # Recomandare: 1-3 secunde
```

### Mod Headless (fără GUI)

Pentru server sau background processing:

```python
automation = OblioAutomation(
    use_existing_profile=True,
    headless=True  # Rulează fără fereastră vizibilă
)
```

⚠️ **Atenție:** În headless mode nu poți vedea ce se întâmplă!

---

## 🔒 Securitate

### Aplicație Web
- ✅ File type validation (doar .xlsx/.xls)
- ✅ Max upload size: 16MB
- ✅ HTTPS encryption
- ✅ Security headers (CSP, HSTS)
- ✅ Input sanitization
- ✅ Temporary file cleanup

### Script Selenium
- ✅ Folosește sesiunea Chrome existentă (nu solicită parole)
- ✅ Nu salvează credențiale în cod
- ✅ Logging detaliat pentru audit
- ✅ Screenshot-uri la erori (pentru debugging)
- ✅ Rulează doar la cerere (nu automat)
- ✅ Open source - cod vizibil și auditabil

---

## 🐛 Troubleshooting

### ❌ "ChromeDriver nu a fost găsit"

**Soluție:**
```bash
pip install webdriver-manager
# SAU descarcă manual și adaugă în PATH
```

### ❌ "Chrome failed to start"

**Soluție:** Verifică path-ul către profilul Chrome (linia 68 în `automatizare_oblio_selenium.py`):
```python
user_data_dir = r"C:\Users\TauUsername\AppData\Local\Google\Chrome\User Data"
```

### ❌ "Element #pp_name nu a fost găsit"

**Soluție:**
1. Verifică că ești logat în Oblio
2. Verifică `automatizare_oblio.log` pentru detalii
3. Crește timeout-ul (linia 177)

### ❌ "Produsul cu SKU 'XXX' nu a fost selectat"

**Soluție:**
1. Verifică că SKU-ul există în Oblio
2. Crește delay-ul de tastare (linia 186): `delay=0.15`
3. Verifică autocomplete în browser manual

### ❌ SKU nu apare în Tab 1

**Soluție:** Hard refresh (Ctrl+Shift+R) sau clear cache.

**Documentație completă:** Vezi `SELENIUM_SETUP.md` → secțiunea "Troubleshooting" (30+ soluții)

---

## 📊 Performanță

### Timpi Estimați (Selenium)

| Bonuri | Mod Manual | Mod Automat Selenium | Economie |
|--------|-----------|----------------------|----------|
| 10     | ~30 min   | ~3 min               | **90%** ⚡ |
| 25     | ~1.5 ore  | ~7 min               | **92%** ⚡ |
| 50     | ~3 ore    | ~15 min              | **92%** ⚡ |
| 100    | ~6 ore    | ~30 min              | **92%** ⚡ |

**Formula:**
```
Timp automat = Număr bonuri × ~15-20 secunde per bon
```

**Factori de influență:**
- Viteza conexiunii internet
- Performanța calculatorului
- Delay-urile configurate în script
- Timp răspuns server Oblio

---

## 📞 Link-uri Utile

### OBSID
- **Site Principal:** https://www.obsid.ro
- **Dashboard:** https://www.obsid.ro/gomag
- **Aplicație Decanturi:** https://decant.obsid.ro

### External
- **Oblio (sistem producție):** https://www.oblio.eu
- **ChromeDriver Downloads:** https://googlechromelabs.github.io/chrome-for-testing/
- **Selenium Documentation:** https://www.selenium.dev/documentation/

---

## 🚀 Deployment

### Coolify (Recomandată)

Aplicația este configurată pentru auto-deploy din Git:

1. Push modificări în GitHub
2. Coolify detectează automat și face redeploy
3. Verifică logs pentru succes

**Detalii complete:** Vezi `DEPLOYMENT.md`

### Docker Manual

```bash
docker build -t obsid-decant .
docker run -d -p 5000:5000 \
  -v $(pwd)/uploads:/app/uploads \
  -v $(pwd)/exports:/app/exports \
  obsid-decant
```

---

## 🎯 Roadmap Viitor

Posibile îmbunătățiri:

- [x] ~~Integrare directă automatizare (fără Tampermonkey)~~ ✅ **COMPLETAT - Selenium**
- [ ] Suport pentru multiple formate Excel (CSV, XLSX variations)
- [ ] Dashboard statistici procesări (câte bonuri create, timp economisit)
- [ ] Integrare directă API Oblio (fără UI automation)
- [ ] Export PDF cu rapoarte
- [ ] Autentificare utilizatori (multi-tenant)
- [ ] Istoric procesări cu undo/redo
- [ ] Retry automat pentru bonurile eșuate
- [ ] Notificări email la finalizare
- [ ] Mobile app (React Native)

---

## 📄 Licență

© 2025 OBSID - Parfumuri Arabești Premium. Toate drepturile rezervate.

---

## 🙏 Mulțumiri

**Dezvoltat cu ❤️ și ☕ pentru OBSID**

Această aplicație economisește **sute de ore de muncă** pe an, permițând echipei OBSID să se concentreze pe ceea ce contează cu adevărat: **parfumuri de calitate premium**.

---

## 📞 Suport

Pentru probleme tehnice:
1. Citește documentația relevantă (`SELENIUM_SETUP.md`, `DEPLOYMENT.md`)
2. Verifică `automatizare_oblio.log` pentru erori
3. Verifică Console browser (F12) pentru erori frontend
4. Testează local pentru izolarea problemei
5. Contactează echipa OBSID pentru suport suplimentar

**Happy automating! 🤖✨**
