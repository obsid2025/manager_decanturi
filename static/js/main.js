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

/**
 * Extrage toate cookies pentru un domeniu specific
 * @param {string} domain - Domeniul pentru care să extragă cookies (ex: 'oblio.eu')
 * @returns {Array} Lista de cookies în format compatibil cu Selenium
 */
function getCookiesForDomain(domain) {
    const allCookies = document.cookie.split(';');
    const cookies = [];
    
    for (let cookie of allCookies) {
        const [name, value] = cookie.trim().split('=');
        if (name && value) {
            cookies.push({
                name: name,
                value: value,
                domain: '.' + domain,
                path: '/',
                secure: true,
                httpOnly: false,
                sameSite: 'Lax'
            });
        }
    }
    
    return cookies;
}

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
 * Afișare rezultate pentru Tab 1 (Raport Decanturi)
 */
function displayResults(data) {
    // Afișare statistici
    document.getElementById('comenziFinalizate').textContent = data.comenzi_finalizate;
    document.getElementById('comenziAnulate').textContent = data.comenzi_anulate;
    document.getElementById('totalComenzi').textContent = data.total_comenzi;

    // Construire tabel (cu coloana SKU)
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

        // Coloana SKU (nouă!)
        const tdSku = document.createElement('td');
        tdSku.textContent = rand.sku;
        tdSku.style.fontFamily = "'Courier New', monospace";
        tdSku.style.fontSize = '0.9rem';
        tdSku.style.color = 'var(--text-secondary)';
        tr.appendChild(tdSku);

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

    // Afișare secțiune rezultate Tab 1
    resultsSection.style.display = 'block';

    // Populare automată Tab 2 (Bonuri de Producție) cu aceleași date
    if (data.bonuri && data.bonuri.length > 0) {
        displayVoucherResultsFromUpload(data);
    }

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

// ========== TAB SWITCHING ==========

/**
 * Gestionare schimbare tab
 */
function switchTab(tabId) {
    // Remove active class from all tabs
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    document.querySelectorAll('.tab-content').forEach(content => {
        content.classList.remove('active');
    });

    // Add active class to selected tab
    const selectedBtn = document.querySelector(`[data-tab="${tabId}"]`);
    const selectedContent = document.getElementById(tabId);

    if (selectedBtn && selectedContent) {
        selectedBtn.classList.add('active');
        selectedContent.classList.add('active');
    }
}

// ========== VOUCHER FUNCTIONALITY ==========

let currentVoucherFilename = null;

// Elemente DOM pentru voucher
const fileInputVoucher = document.getElementById('fileInputVoucher');
const fileNameVoucher = document.getElementById('fileNameVoucher');
const processBtnVoucher = document.getElementById('processBtnVoucher');
const loadingVoucher = document.getElementById('loadingVoucher');
const resultsSectionVoucher = document.getElementById('resultsSectionVoucher');
const errorAlertVoucher = document.getElementById('errorAlertVoucher');
const errorMessageVoucher = document.getElementById('errorMessageVoucher');
const copyAllBtn = document.getElementById('copyAllBtn');

// Event listeners pentru voucher
if (fileInputVoucher) {
    fileInputVoucher.addEventListener('change', handleVoucherFileSelect);
}
if (processBtnVoucher) {
    processBtnVoucher.addEventListener('click', handleVoucherFileUpload);
}
if (copyAllBtn) {
    copyAllBtn.addEventListener('click', handleCopyAllSKUs);
}

// Drag & drop pentru voucher upload zone
const uploadZoneVoucher = document.getElementById('uploadZoneVoucher');
if (uploadZoneVoucher) {
    uploadZoneVoucher.addEventListener('dragover', (e) => {
        e.preventDefault();
        uploadZoneVoucher.style.background = '#e8e8e8';
    });

    uploadZoneVoucher.addEventListener('dragleave', () => {
        uploadZoneVoucher.style.background = '';
    });

    uploadZoneVoucher.addEventListener('drop', (e) => {
        e.preventDefault();
        uploadZoneVoucher.style.background = '';
        const files = e.dataTransfer.files;
        if (files.length > 0) {
            fileInputVoucher.files = files;
            handleVoucherFileSelect();
        }
    });
}

/**
 * Gestionare selectare fișier voucher
 */
function handleVoucherFileSelect() {
    const file = fileInputVoucher.files[0];
    if (file) {
        const ext = file.name.split('.').pop().toLowerCase();
        if (ext !== 'xlsx' && ext !== 'xls') {
            showVoucherError('Vă rugăm selectați un fișier Excel (.xlsx sau .xls)');
            return;
        }

        fileNameVoucher.textContent = file.name;
        fileNameVoucher.style.display = 'inline-block';
        processBtnVoucher.style.display = 'inline-block';
        hideVoucherError();
    }
}

/**
 * Gestionare upload și procesare fișier voucher
 */
async function handleVoucherFileUpload() {
    const file = fileInputVoucher.files[0];
    if (!file) {
        showVoucherError('Vă rugăm selectați un fișier');
        return;
    }

    resultsSectionVoucher.style.display = 'none';
    processBtnVoucher.style.display = 'none';
    loadingVoucher.style.display = 'block';
    hideVoucherError();

    const formData = new FormData();
    formData.append('file', file);

    try {
        const response = await fetch('/process-vouchers', {
            method: 'POST',
            body: formData
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || 'Eroare la procesare');
        }

        currentVoucherFilename = data.filename;
        displayVoucherResults(data);

    } catch (error) {
        showVoucherError(error.message);
        processBtnVoucher.style.display = 'inline-block';
    } finally {
        loadingVoucher.style.display = 'none';
    }
}

/**
 * Afișare rezultate voucher din upload Tab 1 (fără comenzi)
 */
function displayVoucherResultsFromUpload(data) {
    // Salvare date pentru automatizare
    currentBonuriData = data.bonuri;

    // Afișare statistici
    document.getElementById('totalBonuri').textContent = data.total_bonuri;
    document.getElementById('totalBucati').textContent = data.total_bucati;

    // Construire tabel
    const tableBody = document.getElementById('voucherTableBody');
    tableBody.innerHTML = '';

    data.bonuri.forEach((bon, index) => {
        const tr = document.createElement('tr');

        // SKU
        const tdSku = document.createElement('td');
        tdSku.textContent = bon.sku;
        tr.appendChild(tdSku);

        // Nume
        const tdNume = document.createElement('td');
        tdNume.textContent = bon.nume;
        tr.appendChild(tdNume);

        // Cantitate
        const tdCantitate = document.createElement('td');
        tdCantitate.innerHTML = `<strong style="font-size: 1.2rem; color: var(--success-color);">${bon.cantitate}</strong>`;
        tr.appendChild(tdCantitate);

        // Comenzi (gol pentru upload din Tab 1)
        const tdComenzi = document.createElement('td');
        tdComenzi.textContent = '-';
        tdComenzi.style.fontSize = '0.85rem';
        tdComenzi.style.color = 'var(--text-secondary)';
        tr.appendChild(tdComenzi);

        // Acțiuni
        const tdActiuni = document.createElement('td');
        const btnCopy = document.createElement('button');
        btnCopy.className = 'btn-copy-sku';
        btnCopy.innerHTML = `
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect>
                <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path>
            </svg>
            Copiază SKU
        `;
        btnCopy.addEventListener('click', () => copySKU(bon.sku, btnCopy));
        tdActiuni.appendChild(btnCopy);
        tr.appendChild(tdActiuni);

        tableBody.appendChild(tr);
    });

    // Afișare secțiune rezultate
    resultsSectionVoucher.style.display = 'block';
}

/**
 * Afișare rezultate voucher din upload Tab 2 (cu comenzi)
 */
function displayVoucherResults(data) {
    // Afișare statistici
    document.getElementById('totalBonuri').textContent = data.total_bonuri;
    document.getElementById('totalBucati').textContent = data.total_bucati;

    // Construire tabel
    const tableBody = document.getElementById('voucherTableBody');
    tableBody.innerHTML = '';

    data.bonuri.forEach((bon, index) => {
        const tr = document.createElement('tr');

        // SKU
        const tdSku = document.createElement('td');
        tdSku.textContent = bon.sku;
        tr.appendChild(tdSku);

        // Nume
        const tdNume = document.createElement('td');
        tdNume.textContent = bon.nume;
        tr.appendChild(tdNume);

        // Cantitate
        const tdCantitate = document.createElement('td');
        tdCantitate.innerHTML = `<strong style="font-size: 1.2rem; color: var(--success-color);">${bon.cantitate}</strong>`;
        tr.appendChild(tdCantitate);

        // Comenzi
        const tdComenzi = document.createElement('td');
        const comenziText = bon.comenzi ? bon.comenzi.join(', ') : '-';
        const suffix = bon.total_comenzi > 5 ? '...' : '';
        tdComenzi.textContent = comenziText + suffix;
        tdComenzi.style.fontSize = '0.85rem';
        tdComenzi.style.color = 'var(--text-secondary)';
        tr.appendChild(tdComenzi);

        // Acțiuni
        const tdActiuni = document.createElement('td');
        const btnCopy = document.createElement('button');
        btnCopy.className = 'btn-copy-sku';
        btnCopy.innerHTML = `
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect>
                <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path>
            </svg>
            Copiază SKU
        `;
        btnCopy.addEventListener('click', () => copySKU(bon.sku, btnCopy));
        tdActiuni.appendChild(btnCopy);
        tr.appendChild(tdActiuni);

        tableBody.appendChild(tr);
    });

    // Afișare secțiune rezultate
    resultsSectionVoucher.style.display = 'block';
    resultsSectionVoucher.scrollIntoView({ behavior: 'smooth', block: 'start' });

    // Afișare buton automatizare
    const startAutomationBtn = document.getElementById('startAutomationBtn');
    if (startAutomationBtn) {
        startAutomationBtn.style.display = 'inline-flex';
    }
}

// ========== AUTOMATION FUNCTIONALITY ==========

let currentBonuriData = null;

/**
 * Start automatizare Oblio - Folosind Selenium (backend)
 */
async function startOblioAutomation() {
    if (!currentBonuriData || currentBonuriData.length === 0) {
        showVoucherError('Nu există bonuri de procesat!');
        return;
    }

    const totalBonuri = currentBonuriData.length;
    const startAutomationBtn = document.getElementById('startAutomationBtn');
    const originalHTML = startAutomationBtn.innerHTML;

    try {
        // Confirmă acțiunea
        const confirmMsg = `🤖 AUTOMATIZARE OBLIO CU SELENIUM\n\n` +
            `Total bonuri: ${totalBonuri}\n\n` +
            `✅ Ești logat în Oblio în Chrome?\n` +
            `✅ Chrome va fi controlat automat de Selenium\n\n` +
            `ℹ️ Browser-ul Chrome se va deschide automat\n` +
            `ℹ️ NU închide browser-ul până la finalizare\n\n` +
            `Pornești automatizarea?`;

        if (!confirm(confirmMsg)) {
            return;
        }

        // Afișare loading
        startAutomationBtn.disabled = true;
        startAutomationBtn.innerHTML = `
            <div class="spinner" style="width: 20px; height: 20px; margin-right: 0.5rem;"></div>
            Pornire Selenium...
        `;

        console.log(`🚀 START SELENIUM AUTOMATION: ${totalBonuri} bonuri`);
        console.log('📊 Lista bonuri:', currentBonuriData);

        // Extrage cookies Oblio pentru sesiune (IMPORTANT pentru server Linux)
        console.log('🍪 Extragere cookies Oblio...');
        const oblioCookies = getCookiesForDomain('oblio.eu');
        console.log(`🍪 Cookies Oblio găsite: ${oblioCookies.length}`);

        // Trimite request la backend pentru a porni Selenium
        const response = await fetch('/start-automation-selenium', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                bonuri: currentBonuriData,
                oblio_cookies: oblioCookies  // Trimite cookies pentru autentificare
            })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || 'Eroare la automatizare');
        }

        // Succes!
        console.log('✅ Automatizare finalizată:', data);

        startAutomationBtn.innerHTML = `✅ Automatizare completă!`;

        // Mesaj de succes
        const stats = data.stats || {};
        const successCount = stats.success || 0;
        const failedCount = stats.failed || 0;

        let alertMsg = `🎉 AUTOMATIZARE FINALIZATĂ!\n\n`;
        alertMsg += `✅ Bonuri create cu succes: ${successCount}/${totalBonuri}\n`;

        if (failedCount > 0) {
            alertMsg += `❌ Bonuri eșuate: ${failedCount}\n\n`;
            alertMsg += `Vezi log-ul pentru detalii (automatizare_oblio.log)`;
        }

        alert(alertMsg);

        // Restaurează butonul după 5 secunde
        setTimeout(() => {
            startAutomationBtn.innerHTML = originalHTML;
            startAutomationBtn.disabled = false;
        }, 5000);

    } catch (error) {
        console.error('❌ Eroare automatizare:', error);

        let errorMsg = 'Eroare la automatizare: ' + error.message;

        if (error.message.includes('Chrome WebDriver')) {
            errorMsg += '\n\n💡 Asigură-te că:\n' +
                        '- Google Chrome este instalat\n' +
                        '- ChromeDriver este instalat (vezi documentația)';
        }

        showVoucherError(errorMsg);
        startAutomationBtn.disabled = false;
        startAutomationBtn.innerHTML = originalHTML;
    }
}

/**
 * Copiere SKU individual
 */
async function copySKU(sku, button) {
    try {
        await navigator.clipboard.writeText(sku);

        // Feedback vizual
        const originalHTML = button.innerHTML;
        button.classList.add('copied');
        button.innerHTML = `
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <polyline points="20 6 9 17 4 12"></polyline>
            </svg>
            Copiat!
        `;

        setTimeout(() => {
            button.classList.remove('copied');
            button.innerHTML = originalHTML;
        }, 2000);

    } catch (error) {
        showVoucherError('Nu s-a putut copia SKU-ul');
    }
}

/**
 * Copiere toate SKU-urile
 */
async function handleCopyAllSKUs() {
    const tableBody = document.getElementById('voucherTableBody');
    const rows = tableBody.querySelectorAll('tr');

    const skus = Array.from(rows).map(row => {
        return row.querySelector('td:first-child').textContent;
    });

    const skuText = skus.join('\n');

    try {
        await navigator.clipboard.writeText(skuText);

        // Feedback vizual
        const originalHTML = copyAllBtn.innerHTML;
        copyAllBtn.innerHTML = `
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <polyline points="20 6 9 17 4 12"></polyline>
            </svg>
            Copiate ${skus.length} SKU-uri!
        `;

        setTimeout(() => {
            copyAllBtn.innerHTML = originalHTML;
        }, 3000);

    } catch (error) {
        showVoucherError('Nu s-au putut copia SKU-urile');
    }
}

/**
 * Afișare eroare voucher
 */
function showVoucherError(message) {
    errorMessageVoucher.textContent = message;
    errorAlertVoucher.style.display = 'flex';
    errorAlertVoucher.scrollIntoView({ behavior: 'smooth', block: 'center' });
}

/**
 * Ascundere eroare voucher
 */
function hideVoucherError() {
    errorAlertVoucher.style.display = 'none';
}

/**
 * Inițializare la încărcare pagină
 */
document.addEventListener('DOMContentLoaded', () => {
    console.log('OBSID Decant Manager - Inițializat');

    // Setup tab switching
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            const tabId = btn.getAttribute('data-tab');
            switchTab(tabId);
        });
    });

    // Setup automation button
    const startAutomationBtn = document.getElementById('startAutomationBtn');
    if (startAutomationBtn) {
        startAutomationBtn.addEventListener('click', startOblioAutomation);
    }

    // Setup help button
    const helpAutomationBtn = document.getElementById('helpAutomationBtn');
    if (helpAutomationBtn) {
        helpAutomationBtn.addEventListener('click', () => {
            document.getElementById('helpModal').style.display = 'block';
        });
    }

    // Close modal on background click
    const helpModal = document.getElementById('helpModal');
    if (helpModal) {
        helpModal.addEventListener('click', (e) => {
            if (e.target === helpModal) {
                helpModal.style.display = 'none';
            }
        });
    }
});
