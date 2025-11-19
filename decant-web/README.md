# OBSID Decant Manager

Platformă web profesională pentru procesarea comenzilor de decanturi parfumuri.

## 🌟 Caracteristici

- ✅ Upload fișiere Excel cu comenzi
- ✅ Procesare automată și excludere comenzi anulate
- ✅ Vizualizare raport de producție în browser
- ✅ Export Excel pentru arhivare
- ✅ Design profesional gri/negru/alb
- ✅ Responsive design
- ✅ HTTPS securizat
- ✅ Docker deployment

## 🚀 Deployment pe Server Ubuntu

### Prerequisite

- Server Ubuntu 20.04+ (IP: 130.61.223.102)
- Acces SSH cu cheie
- Domeniu configurat: decant.obsid.ro

### Pasul 1: Conectare la server

```bash
ssh -i "C:\Users\ukfdb\.ssh\coolify_key_obsid.pub" ubuntu@130.61.223.102
```

### Pasul 2: Transfer fișiere pe server

**De pe Windows (PowerShell):**

```powershell
# Navigare la director
cd "C:\OBSID SRL\Script-uri Obsid\pregatire_decanturi\decant-web"

# Transfer cu SCP
scp -i "C:\Users\ukfdb\.ssh\coolify_key_obsid.pub" -r . ubuntu@130.61.223.102:/tmp/decant-web
```

**Pe server (după transfer):**

```bash
sudo mv /tmp/decant-web /opt/obsid-decant
cd /opt/obsid-decant
```

### Pasul 3: Instalare Docker și setup

```bash
cd /opt/obsid-decant
sudo chmod +x deploy.sh setup-ssl.sh
sudo ./deploy.sh
```

### Pasul 4: Configurare DNS

Configurează DNS-ul pentru domeniu:
- **Domeniu:** decant.obsid.ro
- **Tip:** A Record
- **Valoare:** 130.61.223.102
- **TTL:** 300

Verifică propagare DNS:
```bash
nslookup decant.obsid.ro
```

### Pasul 5: Pornire aplicație

```bash
cd /opt/obsid-decant
sudo docker-compose up -d
```

Verifică status:
```bash
sudo docker-compose ps
sudo docker-compose logs -f
```

### Pasul 6: Configurare SSL (HTTPS)

**Înainte de a rula acest pas, asigură-te că:**
- DNS-ul este configurat și propagat
- Aplicația rulează (pasul 5)

```bash
cd /opt/obsid-decant
sudo ./setup-ssl.sh
```

### Pasul 7: Verificare

Accesează aplicația:
- **URL:** https://decant.obsid.ro
- **Health check:** https://decant.obsid.ro/health

## 🔧 Comenzi Utile

### Management containere

```bash
# Status
sudo docker-compose ps

# Logs
sudo docker-compose logs -f

# Restart
sudo docker-compose restart

# Stop
sudo docker-compose down

# Rebuild
sudo docker-compose up -d --build
```

### Actualizare aplicație

```bash
cd /opt/obsid-decant
sudo docker-compose down
# Transfer fișiere noi
sudo docker-compose up -d --build
```

### Backup date

```bash
# Backup uploads și exports
sudo tar -czf backup-$(date +%Y%m%d).tar.gz app/uploads app/exports
```

## 📊 Structura Proiectului

```
decant-web/
├── app/
│   ├── app.py                 # Aplicația Flask
│   ├── templates/
│   │   └── index.html         # Template HTML
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css      # Stiluri CSS
│   │   └── js/
│   │       └── main.js        # JavaScript
│   ├── uploads/               # Fișiere încărcate
│   └── exports/               # Rapoarte exportate
├── nginx/
│   ├── nginx.conf             # Config Nginx principal
│   └── conf.d/
│       └── decant.obsid.ro.conf  # Config domeniu
├── Dockerfile                 # Container Python/Flask
├── docker-compose.yml         # Orchestrare containere
├── requirements.txt           # Dependințe Python
├── deploy.sh                  # Script deployment
└── setup-ssl.sh              # Script configurare SSL
```

## 🎨 Design

- **Culori principale:**
  - Gri: #cfcfcf
  - Negru: #2c2c2c, #1a1a1a
  - Alb: #ffffff
  - Background: #f5f5f5

- **Logo:** Integrat din CDN OBSID
- **Font:** System fonts (SF Pro, Segoe UI, etc.)
- **Responsive:** Mobile-first design

## 🔒 Securitate

- ✅ HTTPS obligatoriu (redirect HTTP → HTTPS)
- ✅ SSL/TLS 1.2+
- ✅ Security headers (HSTS, X-Frame-Options, etc.)
- ✅ Max upload size: 20MB
- ✅ File type validation (doar .xlsx, .xls)

## 🐛 Troubleshooting

### Aplicația nu pornește

```bash
# Verifică logs
sudo docker-compose logs decant-web

# Verifică port-uri
sudo netstat -tulpn | grep :5000
```

### Certificat SSL nu se generează

```bash
# Verifică DNS
nslookup decant.obsid.ro

# Verifică logs certbot
sudo docker-compose logs certbot

# Verifică dacă nginx răspunde pe port 80
curl http://decant.obsid.ro/.well-known/acme-challenge/test
```

### Erori la procesare Excel

- Verifică formatul fișierului (.xlsx sau .xls)
- Verifică că există coloana "Status Comanda"
- Verifică că există coloana "Produse comandate"

## 📞 Support

Pentru probleme sau întrebări:
- **Website:** https://www.obsid.ro
- **Dashboard:** https://www.obsid.ro/gomag

## 📝 Licență

© 2025 OBSID - Parfumuri Arabești Premium. Toate drepturile rezervate.
