# Autentificare și Securitate pentru Aplicația Decanturi

## Situația Curentă
În prezent, aplicația este accesibilă oricui are acces la URL-ul serverului. Nu există un mecanism de login pentru a proteja interfața de administrare.

## Recomandare: Supabase
Da, **Supabase** este o alegere excelentă pentru a adăuga autentificare și o bază de date persistentă.

### Avantaje Supabase:
1.  **Autentificare Gata Făcută:** Oferă login cu Email/Parolă, Google, GitHub etc. fără a scrie mult cod de backend.
2.  **Bază de Date PostgreSQL:** O bază de date robustă pentru a stoca istoricul bonurilor, utilizatorii și setările.
3.  **Row Level Security (RLS):** Poți controla exact cine ce date vede.
4.  **Ușor de integrat:** Există biblioteci Python (`supabase-py`) și JavaScript (`@supabase/supabase-js`) foarte bune.

### Cum ar arăta implementarea:
1.  **Frontend:** Pagina de login (HTML/JS) care folosește clientul Supabase JS pentru a autentifica utilizatorul.
2.  **Backend (Flask):**
    *   Verifică token-ul JWT primit de la frontend la fiecare request protejat.
    *   Stochează sesiunea utilizatorului.
3.  **Baza de Date:**
    *   Tabel `users` (gestionat de Supabase Auth).
    *   Tabel `bonuri_history` pentru a păstra istoricul procesărilor.

## Alternativă Rapidă (Temporară)
Dacă dorești o protecție imediată fără a configura o bază de date externă, putem implementa:
1.  **HTTP Basic Auth:** O fereastră simplă de browser care cere user și parolă (hardcodate în `.env`).
2.  **Login Simplu în Flask:** O pagină HTML simplă care verifică o parolă setată în variabilele de mediu.

## Concluzie
Pentru un proiect pe termen lung și scalabil, **recomand Supabase**. Dacă dorești să începi implementarea, pot genera structura necesară.
