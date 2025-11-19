# 🚀 QUICK START - Automatizare Oblio cu Selenium

## ⚡ Începe în 5 minute!

### 1️⃣ Instalează ChromeDriver (O DATĂ)

**Metoda Automată (Recomandată):**
```bash
pip install webdriver-manager
```

**Metoda Manuală:**
1. Verifică versiunea Chrome: `chrome://settings/help`
2. Descarcă ChromeDriver: https://googlechromelabs.github.io/chrome-for-testing/
3. Adaugă în PATH sau copiază în `C:\Windows\System32\`

**Verificare:**
```bash
chromedriver --version
```

---

### 2️⃣ Instalează Selenium (O DATĂ)

```bash
pip install selenium
```

---

### 3️⃣ Loghează-te în Oblio (O DATĂ pe sesiune)

1. Deschide https://www.oblio.eu
2. Loghează-te cu credențialele tale
3. **Lasă tab-ul deschis!**

---

### 4️⃣ Utilizare Zilnică

```
1. Deschide decant.obsid.ro
         ↓
2. Tab "Raport Producție Decanturi"
   → Încarcă Excel
   → Click "Procesează Comenzi"
         ↓
3. Tab "Bonuri de Producție"
   → Verifică datele
   → Click "🤖 START AUTOMATIZARE (SELENIUM)"
         ↓
4. Confirmă în popup
         ↓
5. Chrome se deschide automat și creează bonurile! 🎉
         ↓
6. Verifică raportul final + log-ul (automatizare_oblio.log)
```

---

## ✅ Verificare Rapidă

După instalare, testează cu **2-3 bonuri**:
1. Încarcă un Excel mic (2-3 comenzi)
2. Pornește automatizarea
3. Urmărește Chrome cum completează formularele
4. Verifică în Oblio că bonurile sunt corecte
5. Verifică `automatizare_oblio.log` pentru detalii

---

## 🐛 Probleme?

| Problemă | Soluție |
|----------|---------|
| "ChromeDriver not found" | `pip install webdriver-manager` |
| "Chrome failed to start" | Verifică path-ul profilului Chrome (vezi `SELENIUM_SETUP.md`) |
| "Element #pp_name not found" | Verifică că ești logat în Oblio, crește timeout |
| SKU nu apare în Tab 1 | Hard refresh (Ctrl+Shift+R) sau clear cache |

**Detalii complete:** Citește `SELENIUM_SETUP.md` (documentație de 400+ linii!)

---

## 📞 Suport

- Verifică `automatizare_oblio.log` pentru erori
- Console browser (F12) pentru erori frontend
- Screenshot-uri automate la erori (error_screenshot_*.png)
- Testează manual 1 bon în Oblio pentru a verifica SKU-urile

**Economisește timp! Creează bonuri automat cu Selenium! 🚀**
