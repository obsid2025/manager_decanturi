INSTRUCTIUNI DEPLOYMENT FIX (23 Nov 2025)

1. Actualizare cod pe server:
   cd /cale/catre/manager_decanturi
   git pull

2. Verificare existență fișier produse:
   ls -l produse.xlsx
   (Trebuie să existe și să aibă o dimensiune > 0)

3. Verificare mediu (Opțional):
   python3 generate_test_export.py
   (Acest script va genera un test_export_50.xlsx folosind logica corectă. Dacă acesta e corect, mediul e ok.)

4. RESTART APLICAȚIE (CRITIC):
   Deoarece baza de date se încarcă la pornire, trebuie restartat serviciul.
   Exemplu (dacă folosiți systemd):
   sudo systemctl restart decant-manager
   
   Sau dacă rulați manual/docker:
   docker-compose restart
   # sau
   kill -9 <pid_python> && python3 app.py &

MODIFICĂRI ADUSE:
- S-a eliminat complet logica de "fallback" care ghicea SKU-ul din atribute.
- Acum se folosește STRICT fișierul produse.xlsx.
- Dacă un produs nu e în produse.xlsx, va apărea cu SKU "N/A" în loc să fie greșit.
- S-a adăugat o verificare la fiecare procesare: dacă baza de date e goală, încearcă să o reîncarce.
