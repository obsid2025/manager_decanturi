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
 * NOTĂ: document.cookie NU poate accesa HttpOnly cookies (cele de sesiune)
 * Pentru sesiune completă, trebuie să fie logat în același browser
 * 
 * @param {string} domain - Domeniul pentru care să extragă cookies (ex: 'oblio.eu')
 * @returns {Array} Lista de cookies în format compatibil cu Selenium
 */
function getCookiesForDomain(domain) {
    const allCookies = document.cookie.split(';');
    const cookies = [];
    
    console.log(`🍪 document.cookie raw: "${document.cookie}"`);
    
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
            console.log(`  🍪 Cookie found: ${name} = ${value.substring(0, 20)}...`);
        }
    }
    
    if (cookies.length === 0) {
        console.warn('⚠️ ATENȚIE: Niciun cookie găsit pentru ' + domain);
        console.warn('⚠️ Cookies HttpOnly (sesiune) NU pot fi accesate din JavaScript');
        console.warn('💡 Soluție: Folosește browser reuse pe Windows sau autentificare manuală pe server');
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
let socket = null;
let currentInputType = null;

/**
 * Inițializare Socket.IO connection
 */
function initializeSocket() {
    if (socket) {
        return; // Already connected
    }

    socket = io({
        transports: ['polling', 'websocket'],  // Polling PRIMUL pentru a ocoli problema Traefik
        reconnection: true,
        reconnectionDelay: 1000,
        reconnectionAttempts: 5,
        upgrade: false  // Nu încerca upgrade la WebSocket
    });

    // Connection events
    socket.on('connect', () => {
        console.log('🔌 Conectat la WebSocket');
        console.log('🆔 Socket ID frontend:', socket.id);
        updateTerminalStatus('🟢 Conectat', '#4ade80');
    });

    socket.on('disconnect', () => {
        console.log('⚠️ Deconectat de la WebSocket');
        updateTerminalStatus('🔴 Deconectat', '#ef4444');
    });

    socket.on('connect_error', (error) => {
        console.error('❌ Eroare conexiune WebSocket:', error);
        updateTerminalStatus('🔴 Eroare conexiune', '#ef4444');
    });

    // Log events
    socket.on('log', (data) => {
        appendTerminalLog(data.type, data.message);
    });

    // Input required events
    socket.on('input_required', (prompt) => {
        console.log('🔔 EVENT PRIMIT: input_required', prompt);
        showInputSection(prompt);
    });

    // Automation complete events
    socket.on('automation_complete', (data) => {
        handleAutomationComplete(data);
    });
}

/**
 * Start automatizare Oblio - Cu Terminal Live
 */
async function startOblioAutomation() {
    if (!currentBonuriData || currentBonuriData.length === 0) {
        showVoucherError('Nu există bonuri de procesat!');
        return;
    }

    const totalBonuri = currentBonuriData.length;

    // Confirmă acțiunea
    const confirmMsg = `🤖 AUTOMATIZARE OBLIO CU TERMINAL LIVE\n\n` +
        `Total bonuri: ${totalBonuri}\n\n` +
        `✅ Vei vedea logs live în terminal\n` +
        `✅ Poți introduce credențiale când sunt necesare\n` +
        `✅ Totul rulează pe server (cloud)\n\n` +
        `Pornești automatizarea?`;

    if (!confirm(confirmMsg)) {
        return;
    }

    // Deschide terminal modal
    openTerminal();

    // Asigură-te că Socket.IO este inițializat
    initializeSocket();

    // IMPORTANT: Așteaptă ca socket-ul să fie conectat înainte de emit
    const waitForConnection = () => {
        if (socket && socket.connected) {
            console.log(`🚀 START AUTOMATION LIVE: ${totalBonuri} bonuri`);
            console.log('🔗 Socket connected:', socket.connected, 'ID:', socket.id);
            socket.emit('start_automation_live', {
                bonuri: currentBonuriData
            });
        } else {
            console.log('⏳ Aștept conexiune socket...');
            setTimeout(waitForConnection, 100);
        }
    };

    waitForConnection();
}

/**
 * Deschide Terminal Modal
 */
function openTerminal() {
    const modal = document.getElementById('terminalModal');
    const logsDiv = document.getElementById('terminalLogs');
    const inputSection = document.getElementById('terminalInput');

    // Reset terminal
    logsDiv.innerHTML = '';
    inputSection.style.display = 'none';

    // Clear input fields
    document.getElementById('emailInput').value = '';
    document.getElementById('passwordInput').value = '';
    document.getElementById('twoFAInput').value = '';

    // Afișează modal
    modal.style.display = 'block';

    // Set status
    updateTerminalStatus('🟡 Conectare...', '#fbbf24');
}

/**
 * Închide Terminal Modal
 */
function closeTerminal() {
    const modal = document.getElementById('terminalModal');
    modal.style.display = 'none';
}

/**
 * Append log la terminal
 */
function appendTerminalLog(type, message) {
    const logsDiv = document.getElementById('terminalLogs');
    const logEntry = document.createElement('div');
    logEntry.style.marginBottom = '0.5rem';
    logEntry.style.lineHeight = '1.6';

    // Culori în funcție de tip
    let color = '#d4d4d8'; // default gray
    let icon = 'ℹ️';

    if (type === 'error') {
        color = '#ef4444';
        icon = '❌';
    } else if (type === 'success') {
        color = '#4ade80';
        icon = '✅';
    } else if (type === 'warning') {
        color = '#fbbf24';
        icon = '⚠️';
    } else if (type === 'info') {
        color = '#60a5fa';
        icon = 'ℹ️';
    }

    logEntry.innerHTML = `<span style="color: ${color};">${icon} ${message}</span>`;
    logsDiv.appendChild(logEntry);

    // Auto-scroll la final
    logsDiv.scrollTop = logsDiv.scrollHeight;
}

/**
 * Update terminal status bar
 */
function updateTerminalStatus(text, color) {
    const statusDiv = document.getElementById('terminalStatus');
    if (statusDiv) {
        statusDiv.textContent = text;
        statusDiv.style.color = color;
    }
}

/**
 * Afișare secțiune input când server-ul cere credențiale
 */
function showInputSection(prompt) {
    console.log('🔍 showInputSection CALLED with prompt:', prompt);

    const inputSection = document.getElementById('terminalInput');
    const promptDiv = document.getElementById('inputPrompt');
    const emailSection = document.getElementById('emailInputSection');
    const passwordSection = document.getElementById('passwordInputSection');
    const twoFASection = document.getElementById('twoFAInputSection');

    console.log('📋 Elements found:', {
        inputSection: !!inputSection,
        promptDiv: !!promptDiv,
        emailSection: !!emailSection,
        passwordSection: !!passwordSection,
        twoFASection: !!twoFASection
    });

    // Ascunde toate input-urile
    emailSection.style.display = 'none';
    passwordSection.style.display = 'none';
    twoFASection.style.display = 'none';

    // Determină ce input să afișeze
    if (prompt.type === 'email') {
        currentInputType = 'email';
        promptDiv.textContent = prompt.message || '📧 Introdu email-ul pentru Oblio:';
        emailSection.style.display = 'block';
        setTimeout(() => document.getElementById('emailInput').focus(), 100);
    } else if (prompt.type === 'password') {
        currentInputType = 'password';
        promptDiv.textContent = prompt.message || '🔑 Introdu parola pentru Oblio:';
        passwordSection.style.display = 'block';
        setTimeout(() => document.getElementById('passwordInput').focus(), 100);
    } else if (prompt.type === '2fa') {
        currentInputType = '2fa';
        promptDiv.textContent = prompt.message || '🔢 Introdu codul 2FA (6 cifre):';
        twoFASection.style.display = 'block';
        setTimeout(() => document.getElementById('twoFAInput').focus(), 100);
    }

    // Afișează secțiunea de input
    inputSection.style.display = 'block';

    // Append log
    appendTerminalLog('warning', prompt.message || 'Se așteaptă input de la utilizator...');
}

/**
 * Trimite input către server prin WebSocket
 */
function submitInput() {
    let value = '';

    if (currentInputType === 'email') {
        value = document.getElementById('emailInput').value.trim();
        if (!value) {
            appendTerminalLog('error', '❌ Email-ul nu poate fi gol!');
            return;
        }
    } else if (currentInputType === 'password') {
        value = document.getElementById('passwordInput').value;
        if (!value) {
            appendTerminalLog('error', '❌ Parola nu poate fi goală!');
            return;
        }
    } else if (currentInputType === '2fa') {
        value = document.getElementById('twoFAInput').value.trim();
        if (!/^\d{6}$/.test(value)) {
            appendTerminalLog('error', '❌ Codul 2FA trebuie să aibă 6 cifre!');
            return;
        }
    }

    // Trimite input către server
    socket.emit('user_input', {
        type: currentInputType,
        value: value
    });

    // Ascunde secțiunea de input
    document.getElementById('terminalInput').style.display = 'none';

    // Log
    appendTerminalLog('info', `✉️ Input trimis către server...`);
}

/**
 * Gestionare finalizare automatizare
 */
function handleAutomationComplete(data) {
    const stats = data.stats || {};
    const successCount = stats.success || 0;
    const failedCount = stats.failed || 0;
    const totalBonuri = currentBonuriData.length;

    appendTerminalLog('success', `🎉 AUTOMATIZARE FINALIZATĂ!`);
    appendTerminalLog('info', `✅ Bonuri create cu succes: ${successCount}/${totalBonuri}`);

    if (failedCount > 0) {
        appendTerminalLog('error', `❌ Bonuri eșuate: ${failedCount}`);
    }

    updateTerminalStatus('✅ Finalizat', '#4ade80');

    // Afișează buton de închidere după 3 secunde
    setTimeout(() => {
        const logsDiv = document.getElementById('terminalLogs');
        const closeBtn = document.createElement('button');
        closeBtn.textContent = '✖️ Închide Terminal';
        closeBtn.style.cssText = 'margin-top: 1rem; padding: 0.75rem 1.5rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border: none; border-radius: 6px; cursor: pointer; font-size: 1rem; font-weight: bold;';
        closeBtn.onclick = closeTerminal;
        logsDiv.appendChild(closeBtn);
    }, 3000);
}

/**
 * Handle Enter key for input submission
 */
document.addEventListener('keydown', (e) => {
    const terminalModal = document.getElementById('terminalModal');
    if (terminalModal.style.display === 'block' && e.key === 'Enter') {
        const inputSection = document.getElementById('terminalInput');
        if (inputSection.style.display === 'block') {
            submitInput();
        }
    }
});

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
