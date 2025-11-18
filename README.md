# OBSID Decant Manager

Platformă web profesională pentru procesarea comenzilor de decanturi parfumuri.

![OBSID Logo](https://gomagcdn.ro/domains3/obsid.ro/files/company/parfumuri-arabesti8220.svg)

## 🌟 Caracteristici

- ✅ **Upload Excel** - Încarcă fișiere cu comenzi direct din browser
- ✅ **Procesare Automată** - Exclude automat comenzile anulate
- ✅ **Raport Producție** - Vizualizare clară câte decanturi trebuie făcute
- ✅ **Grupare Inteligentă** - Organizat pe parfum și cantitate (3ml, 5ml, 10ml)
- ✅ **Export Excel** - Descarcă raportul pentru arhivare
- ✅ **Design Profesional** - Temă gri/negru/alb cu logo OBSID
- ✅ **Responsive** - Funcționează pe desktop, tabletă și mobile
- ✅ **HTTPS Securizat** - SSL automat prin Coolify

## 🚀 Demo

**Live:** [https://decant.obsid.ro](https://decant.obsid.ro)

## 📋 Tehnologii

- **Backend:** Python 3.11, Flask, Pandas
- **Frontend:** HTML5, CSS3, JavaScript (Vanilla)
- **Deployment:** Docker, Coolify
- **Server:** Ubuntu 20.04+

## 🏗️ Structura Proiect

```
obsid-decant-manager/
├── Dockerfile              # Container configuration
├── requirements.txt        # Python dependencies
├── app.py                  # Flask application
├── templates/
│   └── index.html         # Frontend template
├── static/
│   ├── css/
│   │   └── style.css      # Styling
│   └── js/
│       └── main.js        # Frontend logic
└── .dockerignore          # Docker ignore rules
```

## 🎯 Cum Funcționează

1. **Upload** - Utilizatorul încarcă fișier Excel cu comenzi
2. **Procesare** - Sistemul filtrează comenzile finalizate
3. **Analiză** - Extrage și grupează produsele pe parfum și cantitate
4. **Raport** - Afișează raportul de producție în browser
5. **Export** - Opțional, descarcă raportul în Excel

### Exemplu Raport:

| Parfum | Cantitate | Bucăți | Total Parfum |
|--------|-----------|--------|--------------|
| **Yum Yum Armaf** | 3 ml | 5 | **10** |
| | 5 ml | 2 | |
| | 10 ml | 3 | |

## 🔧 Deployment

### Coolify (Recomandat)

1. **New Resource** → **Git Repository**
2. **URL:** `https://github.com/YOUR-USERNAME/obsid-decant-manager`
3. **Build Pack:** Dockerfile
4. **Domain:** decant.obsid.ro
5. **Deploy**

### Docker Manual

```bash
git clone https://github.com/YOUR-USERNAME/obsid-decant-manager.git
cd obsid-decant-manager
docker build -t obsid-decant .
docker run -d -p 5000:5000 \
  -v $(pwd)/uploads:/app/uploads \
  -v $(pwd)/exports:/app/exports \
  obsid-decant
```

## 🔒 Securitate

- ✅ File type validation (doar .xlsx/.xls)
- ✅ Max upload size: 16MB
- ✅ HTTPS encryption
- ✅ Security headers
- ✅ Input sanitization

## 📞 Link-uri

- **Site Principal:** [https://www.obsid.ro](https://www.obsid.ro)
- **Dashboard:** [https://www.obsid.ro/gomag](https://www.obsid.ro/gomag)

## 📄 Licență

© 2025 OBSID - Parfumuri Arabești Premium. Toate drepturile rezervate.

---

**Dezvoltat cu ❤️ pentru OBSID**
