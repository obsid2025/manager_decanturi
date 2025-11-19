# 🚀 Quick Start - Deployment în 5 Minute

## Pre-requisite

✅ Cheie SSH: `C:\Users\ukfdb\.ssh\coolify_key_obsid.pub`
✅ Server: `130.61.223.102`
✅ Domeniu: `decant.obsid.ro` (trebuie configurat să pointeze la IP-ul serverului)

---

## Opțiunea 1: Deployment Automat (Windows)

### Un singur click! 🎯

1. **Deschide PowerShell ca Administrator** în directorul `decant-web`:
   ```powershell
   cd "C:\OBSID SRL\Script-uri Obsid\pregatire_decanturi\decant-web"
   ```

2. **Rulează scriptul de deployment:**
   ```powershell
   .\deploy-from-windows.ps1
   ```

3. **Așteaptă finalizarea** (2-5 minute)

4. **Configurează SSL:**
   ```powershell
   ssh -i "C:\Users\ukfdb\.ssh\coolify_key_obsid.pub" ubuntu@130.61.223.102
   cd /opt/obsid-decant
   sudo ./setup-ssl.sh
   ```

5. **Gata!** Accesează: **https://decant.obsid.ro**

---

## Opțiunea 2: Deployment Manual (Step by Step)

### Pasul 1: Transfer fișiere

```powershell
# PowerShell
cd "C:\OBSID SRL\Script-uri Obsid\pregatire_decanturi\decant-web"
scp -i "C:\Users\ukfdb\.ssh\coolify_key_obsid.pub" -r . ubuntu@130.61.223.102:/tmp/decant-web
```

### Pasul 2: Conectare server

```powershell
ssh -i "C:\Users\ukfdb\.ssh\coolify_key_obsid.pub" ubuntu@130.61.223.102
```

### Pasul 3: Setup pe server

```bash
# Pe server
sudo mv /tmp/decant-web /opt/obsid-decant
cd /opt/obsid-decant
sudo chmod +x deploy.sh setup-ssl.sh
sudo ./deploy.sh
```

### Pasul 4: Pornire aplicație

```bash
sudo docker-compose up -d --build
```

### Pasul 5: Verificare

```bash
sudo docker-compose ps
sudo docker-compose logs -f
```

### Pasul 6: SSL (după ce DNS-ul este configurat)

```bash
sudo ./setup-ssl.sh
```

---

## ⚡ Comenzi Rapide

### Verificare status
```bash
ssh -i "C:\Users\ukfdb\.ssh\coolify_key_obsid.pub" ubuntu@130.61.223.102 "cd /opt/obsid-decant && sudo docker-compose ps"
```

### Logs
```bash
ssh -i "C:\Users\ukfdb\.ssh\coolify_key_obsid.pub" ubuntu@130.61.223.102 "cd /opt/obsid-decant && sudo docker-compose logs -f"
```

### Restart
```bash
ssh -i "C:\Users\ukfdb\.ssh\coolify_key_obsid.pub" ubuntu@130.61.223.102 "cd /opt/obsid-decant && sudo docker-compose restart"
```

---

## 📋 Checklist Deployment

- [ ] Cheia SSH există la `C:\Users\ukfdb\.ssh\coolify_key_obsid.pub`
- [ ] Server accesibil la `130.61.223.102`
- [ ] DNS configurat pentru `decant.obsid.ro` → `130.61.223.102`
- [ ] DNS propagat (verifică: `nslookup decant.obsid.ro`)
- [ ] Deployment rulat cu succes
- [ ] Containere pornite (verifică cu `docker-compose ps`)
- [ ] SSL configurat (după propagare DNS)
- [ ] Site accesibil la `https://decant.obsid.ro`

---

## 🔧 Troubleshooting Rapid

### Problema: Conexiune SSH refuzată
```powershell
# Verifică dacă cheia este corectă
ssh -i "C:\Users\ukfdb\.ssh\coolify_key_obsid.pub" ubuntu@130.61.223.102 "whoami"
```

### Problema: DNS nu se propagă
```bash
# Verifică DNS
nslookup decant.obsid.ro
# Sau ping
ping decant.obsid.ro
```

### Problema: Containere nu pornesc
```bash
# Logs detaliate
sudo docker-compose logs decant-web
sudo docker-compose logs nginx
```

### Problema: SSL eșuează
```bash
# Verifică că DNS-ul pointează corect și aplicația răspunde pe port 80
curl http://decant.obsid.ro
```

---

## 📞 Link-uri Utile

- **Aplicație:** https://decant.obsid.ro
- **Health Check:** https://decant.obsid.ro/health
- **Site Principal:** https://www.obsid.ro
- **Dashboard:** https://www.obsid.ro/gomag

---

## 🎯 După Deployment

1. Testează upload-ul unui fișier Excel
2. Verifică procesarea comenzilor
3. Testează export-ul în Excel
4. Verifică responsive design pe mobile
5. Bookmark-uiește în browser pentru acces rapid

---

**Succes! 🎉**
