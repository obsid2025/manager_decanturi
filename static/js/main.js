// Variabile globale
let currentFilename = null;

// Elemente DOM
const fileInput = document.getElementById('fileInput');
const fileName = document.getElementById('fileName');
const processBtn = document.getElementById('processBtn');
const loading = document.getElementById('loading');
const resultsSection = document.getElementById('resultsSection');
const errorAlert = document.getElementById('errorAlert');
const errorMessage = document.getElementById('errorMessage');
const exportBtn = document.getElementById('exportBtn');

// Event listeners
fileInput.addEventListener('change', handleFileSelect);
processBtn.addEventListener('click', handleFileUpload);
exportBtn.addEventListener('click', handleExport);

// Drag & drop pentru upload zone
const uploadZone = document.getElementById('uploadZone');
uploadZone.addEventListener('dragover', (e) => {
    e.preventDefault();
    uploadZone.style.background = '#e8e8e8';
});

uploadZone.addEventListener('dragleave', () => {
    uploadZone.style.background = '';
});

uploadZone.addEventListener('drop', (e) => {
    e.preventDefault();
    uploadZone.style.background = '';
    const files = e.dataTransfer.files;
    if (files.length > 0) {
        fileInput.files = files;
        handleFileSelect();
    }
});

/**
 * Gestionare selectare fișier
 */
function handleFileSelect() {
    const file = fileInput.files[0];
    if (file) {
        // Verificare extensie
        const ext = file.name.split('.').pop().toLowerCase();
        if (ext !== 'xlsx' && ext !== 'xls') {
            showError('Vă rugăm selectați un fișier Excel (.xlsx sau .xls)');
            return;
        }

        fileName.textContent = file.name;
        fileName.style.display = 'inline-block';
        processBtn.style.display = 'inline-block';
        hideError();
    }
}

/**
 * Gestionare upload și procesare fișier
 */
async function handleFileUpload() {
    const file = fileInput.files[0];
    if (!file) {
        showError('Vă rugăm selectați un fișier');
        return;
    }

    // Ascunde rezultatele anterioare
    resultsSection.style.display = 'none';
    processBtn.style.display = 'none';
    loading.style.display = 'block';
    hideError();

    // Creare FormData
    const formData = new FormData();
    formData.append('file', file);

    try {
        const response = await fetch('/upload', {
            method: 'POST',
            body: formData
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || 'Eroare la procesare');
        }

        // Salvare filename pentru export
        currentFilename = data.filename;

        // Afișare rezultate
        displayResults(data);

    } catch (error) {
        showError(error.message);
        processBtn.style.display = 'inline-block';
    } finally {
        loading.style.display = 'none';
    }
}

/**
 * Afișare rezultate
 */
function displayResults(data) {
    // Afișare statistici
    document.getElementById('comenziFinalizate').textContent = data.comenzi_finalizate;
    document.getElementById('comenziAnulate').textContent = data.comenzi_anulate;
    document.getElementById('totalComenzi').textContent = data.total_comenzi;

    // Construire tabel
    const tableBody = document.getElementById('tableBody');
    tableBody.innerHTML = '';

    data.randuri.forEach(rand => {
        const tr = document.createElement('tr');

        // Adaugă clasa pentru primul rând din grup
        if (rand.este_prim) {
            tr.classList.add('parfum-group-start');
        }

        // Coloana parfum (goală dacă nu e primul rând)
        const tdParfum = document.createElement('td');
        tdParfum.textContent = rand.parfum;
        if (rand.parfum) {
            tdParfum.classList.add('parfum-name');
        }
        tr.appendChild(tdParfum);

        // Coloana cantitate
        const tdCantitate = document.createElement('td');
        tdCantitate.textContent = `${rand.cantitate_ml} ml`;
        tr.appendChild(tdCantitate);

        // Coloana bucăți
        const tdBucati = document.createElement('td');
        tdBucati.textContent = rand.bucati;
        tr.appendChild(tdBucati);

        // Coloana total (doar pe primul rând)
        const tdTotal = document.createElement('td');
        tdTotal.textContent = rand.total;
        if (rand.total) {
            tdTotal.classList.add('total-cell');
        }
        tr.appendChild(tdTotal);

        tableBody.appendChild(tr);
    });

    // Construire sumar
    const summaryGrid = document.getElementById('summaryGrid');
    summaryGrid.innerHTML = '';

    Object.entries(data.sumar.cantitati).forEach(([ml, bucati]) => {
        const div = document.createElement('div');
        div.className = 'summary-item';
        div.innerHTML = `
            <strong>${bucati}</strong>
            <span>${ml} ml</span>
        `;
        summaryGrid.appendChild(div);
    });

    document.getElementById('totalGeneral').textContent = data.sumar.total;

    // Afișare secțiune rezultate
    resultsSection.style.display = 'block';

    // Scroll la rezultate
    resultsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

/**
 * Gestionare export Excel
 */
async function handleExport() {
    if (!currentFilename) {
        showError('Nu există date pentru export');
        return;
    }

    try {
        // Download fișier
        window.location.href = `/export/${currentFilename}`;

        // Mesaj de succes (opțional)
        showSuccess('Fișierul se descarcă...');

    } catch (error) {
        showError('Eroare la export: ' + error.message);
    }
}

/**
 * Afișare eroare
 */
function showError(message) {
    errorMessage.textContent = message;
    errorAlert.style.display = 'flex';
    errorAlert.scrollIntoView({ behavior: 'smooth', block: 'center' });
}

/**
 * Ascundere eroare
 */
function hideError() {
    errorAlert.style.display = 'none';
}

/**
 * Afișare mesaj de succes (opțional)
 */
function showSuccess(message) {
    // Poate fi implementat cu un toast notification
    console.log('Success:', message);
}

/**
 * Format număr cu separator de mii
 */
function formatNumber(num) {
    return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ".");
}

/**
 * Inițializare la încărcare pagină
 */
document.addEventListener('DOMContentLoaded', () => {
    console.log('OBSID Decant Manager - Inițializat');
});
