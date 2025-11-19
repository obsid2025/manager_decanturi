# 🤖 AUTOMATIZARE BONURI DE PRODUCȚIE OBLIO

## 📋 Ce face?

Acest script **creează automat bonurile de producție** în Oblio folosind datele din Excel.

## 🚀 Cum funcționează?

1. **Încarcă fișierul Excel** în Tab "Bonuri de Producție"
2. **Apasă butonul "🤖 START AUTOMATIZARE OBLIO"**
3. **Browser-ul se deschide automat** și creează fiecare bon
4. **Te loghezi manual** în Oblio (pentru securitate)
5. **Scriptul completează automat** fiecare bon cu:
   - SKU-ul produsului
   - Cantitatea necesară
   - Salvare automată

## 📦 Cerințe

### 1. Microsoft Edge WebDriver

Scriptul folosește Microsoft Edge (deja instalat pe Windows).

**Instalare WebDriver:**
```bash
# Descarcă Edge WebDriver de la:
https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/

# Sau instalează automat cu Python:
pip install webdriver-manager
```

### 2. Pachete Python

```bash
pip install selenium==4.15.2
```

## 🎯 Utilizare

### Metoda 1: Din Interfața Web (RECOMANDAT)

1. Deschide aplicația web: `http://decant.obsid.ro`
2. Tab "Bonuri de Producție"
3. Încarcă Excel-ul cu comenzi
4. Click pe **"🤖 START AUTOMATIZARE OBLIO"**
5. Loghează-te manual în Oblio când se deschide browser-ul
6. Apasă ENTER în terminal pentru a continua
7. Scriptul creează toate bonurile automat!

### Metoda 2: Rulare Manuală (CLI)

```bash
cd "C:\OBSID SRL\Script-uri Obsid\pregatire_decanturi"
python automatizare_oblio.py
```

## ⚙️ Configurare

### Login Manual (Recomandat)

```python
automation.login_oblio()  # Așteaptă login manual
```

### Login Automat (NU RECOMANDAT - nesigur!)

```python
automation.login_oblio(email="email@exemplu.ro", password="parola")
```

## 🔧 Personalizare

### Modifică timpul de așteptare:

```python
# În automatizare_oblio.py, linia ~35:
self.wait = WebDriverWait(self.driver, 15)  # 15 secunde timeout
```

### Modifică pauzele între bonuri:

```python
# În proceseaza_lista_bonuri(), la final:
time.sleep(1)  # Modifică pentru pauză mai lungă/scurtă
```

## 📊 Workflow Complet

```
┌─────────────────────────────────────────────────────┐
│  1. Încarcă Excel cu comenzi finalizate             │
└──────────────────┬──────────────────────────────────┘
                   ↓
┌─────────────────────────────────────────────────────┐
│  2. App procesează și extrage bonurile (SKU+Cant)   │
└──────────────────┬──────────────────────────────────┘
                   ↓
┌─────────────────────────────────────────────────────┐
│  3. Apasă "START AUTOMATIZARE OBLIO"                │
└──────────────────┬──────────────────────────────────┘
                   ↓
┌─────────────────────────────────────────────────────┐
│  4. Browser Edge se deschide automat                │
└──────────────────┬──────────────────────────────────┘
                   ↓
┌─────────────────────────────────────────────────────┐
│  5. Navigare la oblio.eu/stock/production/          │
└──────────────────┬──────────────────────────────────┘
                   ↓
┌─────────────────────────────────────────────────────┐
│  6. Login manual (email + parolă)                   │
└──────────────────┬──────────────────────────────────┘
                   ↓
┌─────────────────────────────────────────────────────┐
│  Pentru fiecare bon din listă:                      │
│  ┌──────────────────────────────────────────────┐  │
│  │ a) Completează câmpul SKU (pp_name)          │  │
│  │ b) Așteaptă autocomplete                     │  │
│  │ c) Selectează produsul                       │  │
│  │ d) Completează cantitatea (pp_quantity)      │  │
│  │ e) Click "Salvare"                           │  │
│  │ f) Așteaptă confirmare                       │  │
│  │ g) Repetă pentru următorul bon               │  │
│  └──────────────────────────────────────────────┘  │
└──────────────────┬──────────────────────────────────┘
                   ↓
┌─────────────────────────────────────────────────────┐
│  7. Raport final: X bonuri create cu succes         │
└─────────────────────────────────────────────────────┘
```

## 🐛 Troubleshooting

### 1. "WebDriver not found"

Instalează Edge WebDriver:
```bash
pip install webdriver-manager
```

Sau descarcă manual de pe site-ul Microsoft Edge.

### 2. "Element not found"

- Verifică că ești pe pagina corectă (`/stock/production/`)
- Așteaptă mai mult timp (mărește timeout-ul)
- Verifică că Oblio nu a schimbat structura paginii

### 3. Autocomplete nu funcționează

- Mărește timpul de așteptare după introducerea SKU-ului
- Verifică că SKU-ul este corect și există în baza de date Oblio

### 4. Bonurile nu se salvează

- Verifică dacă toate câmpurile obligatorii sunt completate
- Uită-te în console pentru mesaje de eroare
- Rulează scriptul în modul non-headless pentru a vedea ce se întâmplă

## 📝 Exemple

### Exemplu 1: Test cu 3 bonuri

```python
bonuri = [
    {'sku': '6291106063742-3', 'nume': 'Decant 3ml Yum Yum', 'cantitate': 5},
    {'sku': '6291106063717-3', 'nume': 'Decant 3ml Yara Lattafa', 'cantitate': 4},
    {'sku': '6291106063721-10', 'nume': 'Decant 10ml Fakhar Rose', 'cantitate': 3},
]

automation = OblioAutomation()
automation.setup_driver()
automation.login_oblio()
automation.proceseaza_lista_bonuri(bonuri)
automation.close()
```

### Exemplu 2: Citire din Excel

```python
bonuri = citeste_bonuri_din_excel('raport_productie_20251119.xlsx')
automation.proceseaza_lista_bonuri(bonuri)
```

## 🔒 Securitate

**⚠️ IMPORTANT:**
- **NU salva parola în cod!**
- Folosește **login manual** pentru securitate maximă
- Nu commit-a fișierele cu credențiale pe GitHub
- Rulează scriptul doar pe computere de încredere

## 📞 Suport

Pentru probleme sau întrebări:
- Verifică acest README
- Verifică console-ul pentru mesaje de eroare
- Contactează suportul tehnic OBSID

## 🎉 Succes!

Scriptul este gata de folosit! Economisește timp și creează bonurile automat! 🚀
