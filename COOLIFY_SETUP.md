# 🚀 Setup OBSID Decant Manager în Coolify

## 📋 Fișiere necesare (TOATE sunt în acest folder)

```
C:\OBSID SRL\Script-uri Obsid\pregatire_decanturi\
├── Dockerfile              ✅ Creat
├── docker-compose.yml      ✅ Creat
├── requirements.txt        ✅ Creat
├── app.py                  ✅ Creat
├── .dockerignore          ✅ Creat
├── templates/
│   └── index.html         ✅ Creat
└── static/
    ├── css/
    │   └── style.css      ✅ Creat
    └── js/
        └── main.js        ✅ Creat
```

---

## 🎯 Pas cu Pas în Coolify

### Opțiunea 1: Deploy prin Git (RECOMANDAT)

#### 1. Creează un repository Git

**Pe GitHub/GitLab:**
1. Creează un repository nou: `obsid-decant-manager`
2. Inițializează Git local:

```bash
cd "C:\OBSID SRL\Script-uri Obsid\pregatire_decanturi"
git init
git add Dockerfile docker-compose.yml requirements.txt app.py .dockerignore
git add templates/ static/
git commit -m "Initial commit - OBSID Decant Manager"
git remote add origin https://github.com/TAU-USERNAME/obsid-decant-manager.git
git push -u origin main
```

#### 2. În Coolify Dashboard

1. **Login** la Coolify (de obicei la IP server:8000 sau coolify.obsid.ro)

2. **New Project**
   - Nume: `OBSID Decant Manager`

3. **Add New Resource** → **Public Repository**

4. **Repository Details:**
   - **URL:** `https://github.com/TAU-USERNAME/obsid-decant-manager.git`
   - **Branch:** `main`
   - **Build Pack:** `Dockerfile`

5. **Domain Settings:**
   - **Domain:** `decant.obsid.ro`
   - **Enable HTTPS:** ✅ (Coolify va genera automat SSL)

6. **Environment Variables** (opțional):
   ```
   FLASK_ENV=production
   TZ=Europe/Bucharest
   ```

7. **Port:**
   - **Exposed Port:** `5000`

8. Click **Deploy**

---

### Opțiunea 2: Deploy Direct (fără Git)

#### 1. Arhivează fișierele

```powershell
# PowerShell
cd "C:\OBSID SRL\Script-uri Obsid\pregatire_decanturi"
Compress-Archive -Path Dockerfile,docker-compose.yml,requirements.txt,app.py,.dockerignore,templates,static -DestinationPath obsid-decant.zip
```

#### 2. Upload pe server

```bash
# Transfer pe server
scp obsid-decant.zip ubuntu@130.61.223.102:/tmp/
```

#### 3. În Coolify Dashboard

1. **New Project** → **Docker Compose**

2. **Paste docker-compose.yml:**

```yaml
version: '3.8'

services:
  web:
    build: .
    container_name: obsid-decant-manager
    restart: unless-stopped
    ports:
      - "5000:5000"
    volumes:
      - ./uploads:/app/uploads
      - ./exports:/app/exports
    environment:
      - FLASK_ENV=production
      - TZ=Europe/Bucharest
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:5000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
```

3. **Domain:** `decant.obsid.ro`
4. **Enable HTTPS:** ✅
5. **Deploy**

---

### Opțiunea 3: Docker Manual (pe server, fără Coolify)

```bash
# 1. Conectare la server
ssh ubuntu@130.61.223.102

# 2. Creează director
sudo mkdir -p /opt/obsid-decant
cd /opt/obsid-decant

# 3. Transfer fișiere (de pe Windows)
# Rulează pe Windows PowerShell:
scp -r "C:\OBSID SRL\Script-uri Obsid\pregatire_decanturi\*" ubuntu@130.61.223.102:/opt/obsid-decant/

# 4. Build și run (pe server)
cd /opt/obsid-decant
sudo docker-compose up -d --build

# 5. Verificare
sudo docker-compose ps
sudo docker-compose logs -f
```

---

## 🔧 Configurare DNS

**Înainte sau după deploy, configurează:**

- **Domeniu:** `decant.obsid.ro`
- **Tip:** `A Record`
- **Valoare:** `130.61.223.102`
- **TTL:** `300` (5 minute)

**Verificare DNS:**
```bash
nslookup decant.obsid.ro
# Trebuie să returneze: 130.61.223.102
```

---

## ✅ Verificare După Deploy

1. **Health Check:**
   - http://decant.obsid.ro/health sau http://130.61.223.102:5000/health
   - Răspuns așteptat: `{"status":"healthy","service":"OBSID Decant Manager"}`

2. **Accesare aplicație:**
   - https://decant.obsid.ro (dacă SSL este configurat)
   - http://decant.obsid.ro sau http://130.61.223.102:5000 (temporar)

3. **Test funcționalitate:**
   - Upload fișier 45.xlsx
   - Verifică procesare
   - Testează export

---

## 🐛 Troubleshooting

### Aplicația nu pornește în Coolify

**Verifică logs în Coolify Dashboard:**
- Secțiunea "Logs" → Vezi ce eroare apare

**Cele mai comune probleme:**

1. **Port deja folosit:**
   ```bash
   # Verifică ce rulează pe port 5000
   sudo netstat -tulpn | grep :5000
   # Schimbă port-ul în docker-compose.yml la 5001:5000
   ```

2. **Build eșuează:**
   - Verifică că toate fișierele sunt prezente
   - Verifică logs de build în Coolify

3. **DNS nu funcționează:**
   - Așteaptă propagare (până la 24h)
   - Testează cu IP direct: http://130.61.223.102:5000

### SSL nu se activează

- Asigură-te că DNS-ul pointează corect
- În Coolify: **Force SSL Generation**
- Sau manual: În setări Coolify, regenerează certificatul

---

## 📞 Link-uri Rapide

- **Aplicație:** https://decant.obsid.ro
- **Health:** https://decant.obsid.ro/health
- **Site Principal:** https://www.obsid.ro
- **Dashboard:** https://www.obsid.ro/gomag

---

## 🎉 Gata!

După deployment, aplicația va fi disponibilă la **https://decant.obsid.ro**

**Test rapid:**
1. Deschide https://decant.obsid.ro
2. Upload fișier 45.xlsx
3. Vezi raportul generat
4. Exportă în Excel

**Enjoy! 🚀**
