# 🤖 OBSID Decant Manager + Automatizare Oblio

Platformă web profesională pentru procesarea comenzilor de decanturi parfumuri **cu automatizare completă pentru crearea bonurilor de producție în Oblio**.

![OBSID Logo](https://gomagcdn.ro/domains3/obsid.ro/files/company/parfumuri-arabesti8220.svg)

---

## ⚡ FUNCȚIONALITATE PRINCIPALĂ: AUTOMATIZARE OBLIO

### 🎯 Ce face?

Aplicația **creează automat bonuri de producție în Oblio**, deschizând **tab-uri multiple în paralel** pentru procesare rapidă:

1. ✅ **Upload ONE-TIME**: Încarcă Excel o singură dată
2. ✅ **Procesare Automată**: Extrage SKU-uri și cantități
3. ✅ **Paralel Processing**: Deschide 5 tab-uri simultan (configurabil)
4. ✅ **Zero Input Manual**: Tampermonkey completează totul automat
5. ✅ **Auto-Close**: Tab-urile se închid singure când e gata

### 🚀 Rezultat

**Economie de timp:** De la 2-3 ore de muncă manuală → **sub 2 minute automat**!

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
- ✅ **🤖 AUTOMATIZARE OBLIO** - Buton pentru procesare automată în batch-uri

### Sistem Automatizare (COMPLET)
- ✅ **Tampermonkey Integration** - Script pentru automatizare browser
- ✅ **Batch Processing** - 5 tab-uri paralele cu delay-uri configurabile
- ✅ **Progress Indicator** - Vizualizare în timp real a procesării
- ✅ **Session Persistence** - Folosește sesiunea Oblio existentă (fără re-login)
- ✅ **Auto-Fill Forms** - Completează SKU, selectează din autocomplete, introduce cantitate
- ✅ **Auto-Save & Close** - Salvează bonuri și închide tab-uri automat

### Help System Integrat
- ✅ **Modal Instrucțiuni** - Buton "❓ Cum funcționează?" în interfață
- ✅ **Ghid Instalare** - Link-uri directe către Tampermonkey pentru Edge/Chrome
- ✅ **Troubleshooting** - Rezolvări pentru probleme comune
- ✅ **Documentație Completă** - Markdown files pentru referință offline

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
| **QUICK_START.md** | Începe în 3 minute - ghid rapid |
| **INSTALARE_TAMPERMONKEY.md** | Ghid complet de instalare și utilizare (120+ linii) |
| **DEPLOYMENT.md** | Ghid deployment Coolify cu troubleshooting |
| **README_AUTOMATIZARE.md** | Documentație tehnică despre automatizare |

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
│  3. Click "🤖 START AUTOMATIZARE OBLIO"     │
│     → Confirmă în popup                     │
└──────────────┬──────────────────────────────┘
               ↓
┌─────────────────────────────────────────────┐
│  4. Browser deschide tab-uri în batch-uri:  │
│     → Batch 1: 5 tab-uri (paralel)          │
│     → Așteptare 8 secunde                   │
│     → Batch 2: următoarele 5 tab-uri       │
│     → ... continuă până la final            │
└──────────────┬──────────────────────────────┘
               ↓
┌─────────────────────────────────────────────┐
│  5. Tampermonkey în fiecare tab:            │
│     ✅ Completează SKU                      │
│     ✅ Selectează din autocomplete          │
│     ✅ Introduce cantitate                  │
│     ✅ Salvează bonul                       │
│     ✅ Închide tab-ul                       │
└──────────────┬──────────────────────────────┘
               ↓
┌─────────────────────────────────────────────┐
│  6. GATA! Toate bonurile create! 🎉         │
└─────────────────────────────────────────────┘
```

---

## 📋 Tehnologii

### Backend
- **Python 3.11** - Runtime
- **Flask 3.0+** - Web framework
- **Pandas 2.0+** - Excel processing
- **OpenPyXL** - Excel read/write

### Frontend
- **HTML5** - Structure
- **CSS3** - Styling (custom, no frameworks)
- **JavaScript (Vanilla)** - Logic și interactivitate
- **Tampermonkey** - Browser automation

### Deployment
- **Docker** - Containerization
- **Coolify** - PaaS deployment
- **Nginx** - Reverse proxy (via Coolify)
- **Ubuntu 20.04+** - Server OS

---

## 🏗️ Structura Proiect

```
pregatire_decanturi/
├── 📄 Dockerfile                      # Container configuration
├── 📄 requirements.txt                # Python dependencies
├── 📄 app.py                          # Flask application (backend)
│
├── 📁 templates/
│   └── index.html                     # Frontend UI (2 tabs + modal)
│
├── 📁 static/
│   ├── css/
│   │   └── style.css                  # Styling
│   └── js/
│       └── main.js                    # Frontend logic + automation
│
├── 📄 tampermonkey_oblio_auto.js      # Tampermonkey script pentru Oblio
│
├── 📁 Documentație/
│   ├── README.md                      # Acest fișier
│   ├── QUICK_START.md                 # Ghid rapid 3 minute
│   ├── INSTALARE_TAMPERMONKEY.md      # Ghid complet instalare
│   ├── DEPLOYMENT.md                  # Ghid deployment Coolify
│   └── README_AUTOMATIZARE.md         # Documentație tehnică
│
├── 📁 uploads/                        # Excel-uri încărcate (temporar)
└── 📁 exports/                        # Excel-uri exportate (temporar)
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

### 2️⃣ Instalare Tampermonkey (O DATĂ)

**Microsoft Edge:**
1. https://microsoftedge.microsoft.com/addons/detail/tampermonkey/iikmkjmpaadaobahmlepeloendndfphd
2. Click "Obține" → "Adaugă extensie"

**Google Chrome:**
1. https://chrome.google.com/webstore/detail/tampermonkey/dhdgffkkebhmkfjojejmpbldmpobfkfo
2. Click "Add to Chrome"

### 3️⃣ Instalare Script OBSID (O DATĂ)

1. Click pe iconița Tampermonkey → "Dashboard"
2. Click pe "+" (script nou)
3. Copiază conținutul din `tampermonkey_oblio_auto.js`
4. Lipește în editor și Salvează (Ctrl+S)

### 4️⃣ Utilizare Zilnică

1. Loghează-te în Oblio (o dată pe sesiune)
2. Deschide https://decant.obsid.ro
3. Încarcă Excel în Tab 1 → Procesează
4. Tab 2 se completează automat
5. Click "🤖 START AUTOMATIZARE OBLIO"
6. ☕ Relaxează-te - bonurile se creează singure!

**Citește:** `QUICK_START.md` pentru ghid detaliat

---

## 🔧 Configurare Avansată

### Ajustare Performanță

Editează `static/js/main.js` (linia ~520):

```javascript
const BATCH_SIZE = 5;              // 3-10 (număr tab-uri paralele)
const DELAY_BETWEEN_TABS = 500;    // ms (între tab-uri în același batch)
const DELAY_BETWEEN_BATCHES = 8000; // ms (între batch-uri)
```

**Recomandări:**
- **Calculator rapid + internet bun:** BATCH_SIZE = 10, DELAY = 5000
- **Balansat (RECOMANDAT):** BATCH_SIZE = 5, DELAY = 8000
- **Conservator:** BATCH_SIZE = 3, DELAY = 10000

### Ajustare Timeout Tampermonkey

Editează `tampermonkey_oblio_auto.js`:

```javascript
function waitForElement(selector, timeout = 10000) {
    // Schimbă 10000 la 15000 pentru timeout mai lung
}
```

---

## 🔒 Securitate

### Aplicație Web
- ✅ File type validation (doar .xlsx/.xls)
- ✅ Max upload size: 16MB
- ✅ HTTPS encryption
- ✅ Security headers (CSP, HSTS)
- ✅ Input sanitization
- ✅ Temporary file cleanup

### Tampermonkey Script
- ✅ Rulează doar pe domeniul Oblio (`@match https://www.oblio.eu/stock/production/*`)
- ✅ Nu cere/trimite parole (folosește sesiunea browser existentă)
- ✅ Nu accesează alte site-uri
- ✅ Open source - cod vizibil și auditabil

---

## 🐛 Troubleshooting

### ❌ Tab-urile se deschid dar nu fac nimic

**Soluție:** Verifică că ești logat în Oblio și că Tampermonkey script este activ (icon verde).

### ❌ "Element not found" în console

**Soluție:** Reîmprospătează pagina (Ctrl+F5) sau verifică că Oblio nu a schimbat interfața.

### ❌ Browser-ul se blochează

**Soluție:** Micșorează `BATCH_SIZE` la 3 în `main.js`.

### ❌ SKU nu apare în Tab 1

**Soluție:** Hard refresh (Ctrl+Shift+R) sau clear cache.

**Documentație completă:** Vezi `INSTALARE_TAMPERMONKEY.md` → secțiunea "Troubleshooting"

---

## 📊 Performanță

### Timpi Estimați

| Bonuri | Mod Manual | Mod Automat | Economie |
|--------|-----------|-------------|----------|
| 10     | ~30 min   | ~25 sec     | **98%** ⚡ |
| 25     | ~1.5 ore  | ~1 min      | **98%** ⚡ |
| 50     | ~3 ore    | ~2.5 min    | **98%** ⚡ |
| 100    | ~6 ore    | ~5 min      | **98%** ⚡ |

**Formula:**
```
Timp automat = (Număr batch-uri × 8s) + (Număr bonuri × 2s)
```

---

## 📞 Link-uri Utile

### OBSID
- **Site Principal:** https://www.obsid.ro
- **Dashboard:** https://www.obsid.ro/gomag
- **Aplicație Decanturi:** https://decant.obsid.ro

### External
- **Oblio (sistem producție):** https://www.oblio.eu
- **Tampermonkey Edge:** https://microsoftedge.microsoft.com/addons/detail/tampermonkey/iikmkjmpaadaobahmlepeloendndfphd
- **Tampermonkey Chrome:** https://chrome.google.com/webstore/detail/tampermonkey/dhdgffkkebhmkfjojejmpbldmpobfkfo

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

- [ ] Suport pentru multiple formate Excel (CSV, XLSX variations)
- [ ] Dashboard statistici procesări (câte bonuri create, timp economisit)
- [ ] Integrare directă API Oblio (fără Tampermonkey)
- [ ] Export PDF cu rapoarte
- [ ] Autentificare utilizatori (multi-tenant)
- [ ] Istoric procesări cu undo/redo
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
1. Citește documentația relevantă (`INSTALARE_TAMPERMONKEY.md`, `DEPLOYMENT.md`)
2. Verifică Console browser (F12) pentru erori
3. Testează local pentru izolarea problemei
4. Contactează echipa OBSID pentru suport suplimentar

**Happy automating! 🤖✨**
