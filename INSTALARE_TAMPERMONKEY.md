# 🤖 INSTALARE AUTOMATIZARE OBLIO - Ghid Complet

## 📋 Ce face automatizarea?

Sistemul **creează automat bonuri de producție în Oblio** din interfața web, deschizând **tab-uri multiple în paralel** pentru procesare rapidă:

- ✅ Deschide 5 tab-uri simultan (configurabil)
- ✅ Completează automat SKU și cantitate
- ✅ Salvează bonurile automat
- ✅ Închide tab-urile automat când e gata
- ✅ Procesează toate bonurile din Excel într-un singur click!

---

## 🚀 INSTALARE ÎN 3 PAȘI

### PASUL 1: Instalează Tampermonkey

Tampermonkey este o extensie de browser care permite rularea de scripturi personalizate.

#### Pentru Microsoft Edge (RECOMANDAT)

1. Deschide Microsoft Edge
2. Navighează la: **[Tampermonkey pe Edge Add-ons](https://microsoftedge.microsoft.com/addons/detail/tampermonkey/iikmkjmpaadaobahmlepeloendndfphd)**
3. Click pe **"Obține"** / **"Get"**
4. Click pe **"Adaugă extensie"** / **"Add extension"**
5. ✅ Instalare completă!

#### Pentru Google Chrome

1. Deschide Google Chrome
2. Navighează la: **[Tampermonkey pe Chrome Web Store](https://chrome.google.com/webstore/detail/tampermonkey/dhdgffkkebhmkfjojejmpbldmpobfkfo)**
3. Click pe **"Add to Chrome"**
4. Click pe **"Add extension"**
5. ✅ Instalare completă!

#### Pentru Firefox

1. Deschide Firefox
2. Navighează la: **[Tampermonkey pe Firefox Add-ons](https://addons.mozilla.org/en-US/firefox/addon/tampermonkey/)**
3. Click pe **"Add to Firefox"**
4. Click pe **"Add"**
5. ✅ Instalare completă!

---

### PASUL 2: Instalează Scriptul OBSID

1. **Deschide Tampermonkey Dashboard:**
   - Click pe iconița Tampermonkey din browser (în bara de sus, lângă adresă)
   - Selectează **"Dashboard"** / **"Panou de control"**

2. **Creează script nou:**
   - Click pe tab-ul **"Utilities"** (sau **"Utilități"**)
   - Găsește secțiunea **"Import from URL"** sau **"URL"**
   - **SAU** click direct pe **"+"** (butonul de creare script nou)

3. **Copiază codul scriptului:**
   - Deschide fișierul `tampermonkey_oblio_auto.js` din proiect
   - Selectează **TOT** conținutul (Ctrl+A)
   - Copiază (Ctrl+C)

4. **Lipește în editor:**
   - Șterge tot ce e în editorul Tampermonkey
   - Lipește codul copiat (Ctrl+V)

5. **Salvează:**
   - Click pe **File → Save** sau apasă **Ctrl+S**
   - Iconița Tampermonkey ar trebui să arate acum **"1"** (1 script activ)

6. **Verifică instalarea:**
   - Mergi înapoi la Dashboard
   - Ar trebui să vezi scriptul: **"OBSID - Automatizare Bonuri Producție Oblio"**
   - Status: **🟢 Enabled** (activat)

---

### PASUL 3: Loghează-te în Oblio

**IMPORTANT:** Trebuie să fii deja autentificat în Oblio înainte de automatizare!

1. Deschide o fereastră de browser
2. Navighează la: **https://www.oblio.eu**
3. **Loghează-te** cu credențialele tale Oblio
4. ✅ **NU închide această fereastră!** (sesiunea trebuie să rămână activă)

---

## 🎯 UTILIZARE

### Workflow Complet

```
┌─────────────────────────────────────────────────────────┐
│  1. Deschide https://decant.obsid.ro                    │
└──────────────────┬──────────────────────────────────────┘
                   ↓
┌─────────────────────────────────────────────────────────┐
│  2. Tab "Raport Producție Decanturi"                    │
│     → Încarcă fișierul Excel cu comenzi                 │
│     → Apasă "Procesează Comenzi"                        │
└──────────────────┬──────────────────────────────────────┘
                   ↓
┌─────────────────────────────────────────────────────────┐
│  3. Tab "Bonuri de Producție"                           │
│     → Tabelul se completează AUTOMAT                    │
│     → Apare butonul "🤖 START AUTOMATIZARE OBLIO"       │
└──────────────────┬──────────────────────────────────────┘
                   ↓
┌─────────────────────────────────────────────────────────┐
│  4. Click pe "🤖 START AUTOMATIZARE OBLIO"              │
│     → Confirmă în popup                                 │
└──────────────────┬──────────────────────────────────────┘
                   ↓
┌─────────────────────────────────────────────────────────┐
│  5. Sistemul deschide tab-uri în batch-uri:             │
│     → Batch 1: 5 tab-uri în paralel (0.5s delay)        │
│     → Așteptare 8 secunde                               │
│     → Batch 2: următoarele 5 tab-uri                    │
│     → ... și așa mai departe                            │
└──────────────────┬──────────────────────────────────────┘
                   ↓
┌─────────────────────────────────────────────────────────┐
│  6. În fiecare tab, scriptul Tampermonkey:              │
│     ✅ Completează SKU-ul                               │
│     ✅ Selectează produsul din autocomplete             │
│     ✅ Completează cantitatea                           │
│     ✅ Click "Salvare"                                  │
│     ✅ Închide tab-ul automat                           │
└──────────────────┬──────────────────────────────────────┘
                   ↓
┌─────────────────────────────────────────────────────────┐
│  7. GATA! Toate bonurile au fost create automat! 🎉     │
└─────────────────────────────────────────────────────────┘
```

### Pași Detaliat

1. **Încarcă datele:**
   - Mergi la https://decant.obsid.ro
   - Tab "Raport Producție Decanturi"
   - Încarcă fișierul Excel
   - Click "Procesează Comenzi"

2. **Verifică datele:**
   - Treci la tab "Bonuri de Producție"
   - Verifică că tabelul s-a completat corect cu SKU-uri și cantități

3. **Pornește automatizarea:**
   - Click pe butonul verde **"🤖 START AUTOMATIZARE OBLIO"**
   - Confirmă în fereastra popup

4. **Monitorizare:**
   - Vei vedea tab-uri care se deschid automat (5 odată)
   - În fiecare tab apare un indicator violet: **"🤖 OBSID Automation"**
   - Progresul se afișează în indicator: "Se procesează...", "Salvare bon...", etc.

5. **Finalizare:**
   - Tab-urile se închid automat după ce bonul e salvat
   - În tab-ul principal (decant.obsid.ro) vei vedea mesaj de succes

---

## ⚙️ CONFIGURARE AVANSATĂ

### Modifică numărul de tab-uri în paralel

Editează `static/js/main.js`, linia ~520:

```javascript
const BATCH_SIZE = 5; // Schimbă la 3, 10, etc.
```

**Recomandări:**
- **3 tab-uri** = procesare conservatoare (pentru calculatoare mai slabe)
- **5 tab-uri** = balansat (RECOMANDAT)
- **10 tab-uri** = rapid (necesită calculator puternic și internet rapid)

### Modifică delay-urile

```javascript
const DELAY_BETWEEN_TABS = 500; // ms între tab-uri (în același batch)
const DELAY_BETWEEN_BATCHES = 8000; // ms între batch-uri (8 secunde)
```

**Atenție:** Delay-uri prea mici pot suprasolicita browser-ul!

### Modifică timeout-urile în Tampermonkey script

Editează `tampermonkey_oblio_auto.js`:

```javascript
function waitForElement(selector, timeout = 10000) {
    // Schimbă 10000 la 15000 pentru timeout mai lung (15 secunde)
}
```

---

## 🐛 TROUBLESHOOTING

### 1. ❌ Scriptul nu pornește deloc

**Verifică:**
- ✅ Tampermonkey este instalat și activat?
  - Click pe iconița Tampermonkey → ar trebui să vezi scriptul verde
- ✅ Scriptul este activat în Dashboard?
  - Deschide Tampermonkey Dashboard → verifică status

**Soluție:**
- Reîmprospătează pagina (Ctrl+F5)
- Verifică Console-ul browser-ului (F12) pentru erori

---

### 2. ❌ Tab-urile se deschid, dar scriptul nu face nimic

**Verifică:**
- ✅ URL-ul tab-ului conține parametrii `?sku=...&qty=...`?
- ✅ Ești logat în Oblio în sesiunea browser-ului?

**Soluție:**
- Loghează-te manual în Oblio într-un tab
- Reîncearcă automatizarea

---

### 3. ❌ "Element not found" în console

**Cauză:** Oblio a schimbat structura paginii SAU pagina nu s-a încărcat complet.

**Soluție:**
- Mărește timeout-ul în `waitForElement()` (ex: 15000ms)
- Verifică că Oblio nu a făcut update la interfață

---

### 4. ❌ Autocomplete nu apare / Produsul nu se selectează

**Cauză:** SKU-ul nu există în baza de date Oblio SAU autocomplete-ul e prea lent.

**Soluție:**
- Verifică SKU-urile în Excel (sunt corecte?)
- Mărește delay-ul după introducerea SKU-ului:
  ```javascript
  await sleep(1500); // Schimbă la 2500 sau 3000
  ```

---

### 5. ❌ Bonurile nu se salvează

**Cauză:** Butonul de salvare nu e găsit SAU există erori de validare în formular.

**Verifică:**
- Console-ul browser-ului (F12) pentru erori
- Toate câmpurile obligatorii sunt completate?

**Soluție:**
- Rulează scriptul manual pentru UN bon să vezi exact unde eșuează
- Verifică în Oblio ce erori apar

---

### 6. ❌ Browser-ul se blochează / devine lent

**Cauză:** Prea multe tab-uri deschise simultan.

**Soluție:**
- Micșorează `BATCH_SIZE` la 3
- Mărește `DELAY_BETWEEN_BATCHES` la 10000 (10 secunde)

---

### 7. ⚠️ Tab-urile nu se închid automat

**Cauză:** Browser-ul blochează `window.close()` pentru tab-uri deschise cu `window.open()`.

**Soluție:**
- Este normal pentru unele browsere
- Închide manual tab-urile rămase
- **SAU** verifică setările browser-ului pentru permisiuni JavaScript

---

### 8. 🔍 Cum verific dacă scriptul rulează?

**Metoda 1: Console Log**
- Deschide Console (F12)
- Când accesezi `https://www.oblio.eu/stock/production/?sku=...`
- Ar trebui să vezi: `🤖 OBSID Automation Script - LOADED`

**Metoda 2: Indicator Vizual**
- În colțul dreapta sus al paginii Oblio
- Ar trebui să apară un dreptunghi violet cu text: "🤖 OBSID Automation"

---

## 🔒 SECURITATE

### ⚠️ IMPORTANT - Citește cu atenție!

1. **NU partaja scriptul Tampermonkey cu persoane necunoscute**
   - Scriptul are acces la pagina Oblio
   - Poate completa formulare automat

2. **NU modifica scriptul dacă nu știi ce faci**
   - Cod incorect poate cauza erori în Oblio
   - Poți crea bonuri greșite

3. **Verifică întotdeauna rezultatele**
   - După automatizare, verifică în Oblio că bonurile sunt corecte
   - Primele rulări: monitorizează fiecare bon

4. **Păstrează-ți credențialele în siguranță**
   - Scriptul **NU** cere parola
   - Folosește sesiunea browser-ului existent

5. **Backup înainte de rulări mari**
   - Pentru 50+ bonuri, verifică prima dată cu 5 bonuri test
   - Asigură-te că totul funcționează corect

---

## 📊 STATISTICI ȘI PERFORMANȚĂ

### Timpi estimați

| Bonuri | Batch-uri | Timp total estimat |
|--------|-----------|-------------------|
| 5      | 1         | ~10 secunde       |
| 10     | 2         | ~25 secunde       |
| 25     | 5         | ~1 minut          |
| 50     | 10        | ~2.5 minute       |
| 100    | 20        | ~5 minute         |

**Formula:**
```
Timp = (Număr batch-uri × 8s) + (Număr bonuri × 2s)
```

### Optimizare

Pentru **performanță maximă:**
- BATCH_SIZE = 10
- DELAY_BETWEEN_BATCHES = 5000

Pentru **stabilitate maximă:**
- BATCH_SIZE = 3
- DELAY_BETWEEN_BATCHES = 10000

---

## 📞 SUPORT

### Probleme tehnice?

1. **Verifică acest ghid** - majoritatea problemelor sunt rezolvate aici
2. **Console-ul browser-ului** (F12) - citește erorile
3. **Testează manual** - creează 1 bon manual să vezi că Oblio funcționează
4. **Contactează echipa OBSID** - pentru probleme nerezolvate

### Raportare bug-uri

Când raportezi o problemă, include:
- ✅ Browser și versiune (Edge 120, Chrome 119, etc.)
- ✅ Tampermonkey versiune
- ✅ Erori din Console (F12)
- ✅ Screenshot-uri dacă e posibil
- ✅ Pașii pentru reproducerea problemei

---

## 🎉 SUCCES!

Scriptul este gata de folosit! Vei economisi **ore de muncă** creând bonurile automat!

**Înainte de prima utilizare:**
1. ✅ Testează cu 2-3 bonuri
2. ✅ Verifică rezultatele în Oblio
3. ✅ Apoi rulează pentru toate bonurile

**Enjoy automation! 🚀**
