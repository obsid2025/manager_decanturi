# 🚀 Ghid Utilizare Selenium Automation

## 📋 Mod de Funcționare

Aplicația folosește **2 metode diferite** în funcție de unde rulează:

### 🪟 Windows (Local Development) - Browser Reuse
- Selenium se **conectează la Chrome-ul tău deja deschis**
- Vezi **LIVE** în browser cum se creează bonurile
- Perfect pentru **debugging**
- Folosește sesiunea ta activă din Chrome (nu e nevoie de login)

### 🐧 Linux Server (Coolify) - Cookies
- Selenium rulează în **headless mode** (fără GUI)
- Folosește **cookies trimise din frontend** pentru autentificare
- Automat, fără intervenție

---

## 🪟 Instrucțiuni Windows (Debugging Live)

### Pasul 1: Pornește Chrome cu Remote Debugging

Închide toate instanțele Chrome deschise, apoi pornește Chrome cu comanda:

```powershell
& "C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 --user-data-dir="C:\Users\$env:USERNAME\AppData\Local\Google\Chrome\User Data"
```

**SAU** creează un shortcut:
1. Click dreapta pe Desktop → New → Shortcut
2. Location: 
   ```
   "C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 --user-data-dir="C:\Users\YOUR_USERNAME\AppData\Local\Google\Chrome\User Data"
   ```
3. Name: `Chrome Debug Mode`
4. Pornește Chrome din acest shortcut

### Pasul 2: Loghează-te în Oblio

1. În Chrome-ul pornit, accesează https://www.oblio.eu
2. Autentifică-te cu email + parolă + 2FA
3. Asigură-te că ești pe pagina principală Oblio

### Pasul 3: Pornește Aplicația

```powershell
python app.py
```

### Pasul 4: Folosește Aplicația

1. Accesează http://localhost:5000
2. Încarcă fișierul Excel
3. Click pe "🤖 Pornește Automatizare Selenium"
4. **Vezi LIVE în Chrome** cum se creează bonurile!

### ✅ Avantaje Windows (Browser Reuse):
- ✅ Vezi **LIVE** ce se întâmplă
- ✅ Debugging ușor
- ✅ Nu e nevoie să trimiți cookies
- ✅ Folosește sesiunea ta activă (2FA deja trecut)
- ✅ Poți interveni manual dacă e necesar

---

## 🐧 Instrucțiuni Linux Server (Coolify)

### Configurare Environment Variables

În Coolify, setează variabilele (opțional, pentru fallback):

```env
OBLIO_EMAIL=obsidparfume@gmail.com
OBLIO_PASSWORD=M@83LFdkc.Mgcx3
```

### Mod de Funcționare

1. Te loghezi în Oblio în browser-ul tău normal
2. Aplicația **extrage automat cookies** din browser
3. Trimite cookies la backend
4. Backend injectează cookies în Selenium
5. Selenium rulează automat cu sesiunea ta

### ✅ Avantaje Linux (Cookies):
- ✅ Funcționează automat fără intervenție
- ✅ Nu e nevoie de GUI
- ✅ Folosește sesiunea activă (2FA deja trecut)
- ✅ Perfect pentru server

---

## 🔧 Troubleshooting

### Windows: "Nu se poate conecta la Chrome"

**Cauză:** Chrome nu rulează cu remote debugging activat

**Soluție:**
1. Închide toate instanțele Chrome (Task Manager → End Chrome)
2. Pornește Chrome cu comanda de mai sus
3. Verifică că Chrome rulează:
   ```powershell
   curl http://localhost:9222/json
   ```
   Ar trebui să vezi JSON cu tabs deschise

### Linux: "Element #pp_name nu a fost găsit"

**Cauză:** Nu ești autentificat (cookies invalide sau expirate)

**Soluție:**
1. Asigură-te că ești logat în Oblio în browser-ul tău
2. Reîncarcă pagina aplicației (pentru cookies fresh)
3. Încearcă din nou automatizarea

### "Cookies Oblio lipsă"

**Cauză:** Browser-ul blochează accesul la cookies cross-origin

**Soluție:**
1. Asigură-te că aplicația rulează pe `localhost` (nu IP)
2. Dacă folosești HTTPS, verifică certificatele
3. Verifică Console-ul browser-ului pentru erori JavaScript

---

## 📊 Fluxul Automatizării

### Windows (Browser Reuse):
```
1. Tu pornești Chrome cu remote debugging
2. Te loghezi manual în Oblio
3. Selenium se conectează la Chrome-ul tău
4. Vezi LIVE cum se creează bonurile
```

### Linux (Cookies):
```
1. Te loghezi în Oblio în browser-ul tău
2. Frontend extrage cookies
3. Backend primește cookies
4. Selenium injectează cookies
5. Selenium creează bonuri automat (headless)
```

---

## 🎯 Recomandări

- **Pentru debugging/testare:** Folosește Windows cu browser reuse
- **Pentru producție/server:** Folosește Linux cu cookies
- **Întotdeauna:** Asigură-te că ești logat în Oblio înainte să pornești automatizarea
- **Cookies expirare:** Dacă primești erori de autentificare, re-loghează-te în Oblio

---

## 📝 Note Importante

1. **2FA:** Metodele folosite (browser reuse + cookies) NU necesită 2FA repetat
   - Te loghezi o dată manual cu 2FA
   - Sesiunea rămâne activă

2. **Securitate:** 
   - Cookies nu sunt salvate permanent
   - Se trimit doar la backend pentru sesiunea curentă
   - Environment variables pentru fallback (doar dacă cookies nu funcționează)

3. **Performance:**
   - Windows: Mai lent (GUI visible)
   - Linux: Mai rapid (headless)

4. **Debugging:**
   - Windows: Vezi tot live, poți interveni
   - Linux: Vezi doar logs, screenshots la eroare
