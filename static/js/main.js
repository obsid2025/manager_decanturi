// TERMINAL JS - OBSID DECANT MANAGER

// Global State
let currentFilename = null;
let currentVouchers = [];
let socket = io();
let isProcessing = false;
let currentInputType = null;

// DOM Elements
let dom = {};

// --- INITIALIZATION ---

document.addEventListener('DOMContentLoaded', () => {
    // Initialize DOM elements here to ensure they exist
    dom = {
        nav: {
            analysis: document.getElementById('cmd-analysis'),
            production: document.getElementById('cmd-production')
        },
        modules: {
            analysis: document.getElementById('raport-tab'), // Fixed ID: raport-tab
            production: document.getElementById('voucher-tab') // Fixed ID: voucher-tab
        },
        analysis: {
            fileInput: document.getElementById('fileInput'),
            uploadBox: document.querySelector('#raport-tab .upload-box'), // More specific
            fileName: document.getElementById('fileName'),
            executeBtn: document.getElementById('processBtn'),
            results: document.getElementById('resultsSection'),
            tableBody: document.getElementById('tableBody'),
            summaryGrid: document.getElementById('summaryGrid'),
            exportBtn: document.getElementById('exportBtn'),
            stats: {
                finalized: document.getElementById('comenziFinalizate'),
                cancelled: document.getElementById('comenziAnulate'),
                total: document.getElementById('totalComenzi'),
                grandTotal: document.getElementById('totalGeneral')
            }
        },
        production: {
            fileInput: document.getElementById('fileInputVoucher'),
            fileName: document.getElementById('fileNameVoucher'),
            processBtn: document.getElementById('processBtnVoucher'),
            loading: document.getElementById('loadingVoucher'),
            resultsSection: document.getElementById('resultsSectionVoucher'),
            stats: {
                totalBonuri: document.getElementById('totalBonuri'),
                totalBucati: document.getElementById('totalBucati')
            },
            copyBtn: document.getElementById('copyAllBtn'),
            runBtn: document.getElementById('startAutomationBtn'),
            stopBtn: document.getElementById('stopAutomationBtn'),
            tableBody: document.getElementById('voucherTableBody'),
            errorAlert: document.getElementById('errorAlertVoucher'),
            errorMessage: document.getElementById('errorMessageVoucher'),
            status: document.getElementById('terminalStatus')
        },
        logs: document.getElementById('terminalLogs'),
        cli: {
            input: document.getElementById('cliInput'),
            section: document.getElementById('cliInputSection'),
            prompt: document.getElementById('cliPrompt')
        }
    };

    initTypewriter();
    
    try {
        initEventListeners();
        logSystem('SYSTEM_INIT', 'Terminal initialized. Ready for input.');
        logSystem('SYSTEM_CHECK', 'Connected to server via Socket.IO');
        
        // Debug: Check if elements exist
        if (!dom.production.fileInput) logSystem('ERR', 'Production File Input NOT FOUND', 'error');
        if (!dom.production.fileName) logSystem('ERR', 'Production File Name Display NOT FOUND', 'error');
        if (!dom.production.processBtn) logSystem('ERR', 'Production Process Button NOT FOUND', 'error');
        
    } catch (e) {
        logSystem('CRITICAL_ERR', e.message, 'error');
        console.error(e);
    }
});

function initTypewriter() {
    const titleElement = document.getElementById('typewriter-title');
    if (titleElement) {
        const text = "OBSID_DECANT_MANAGER_V2.0";
        let i = 0;
        titleElement.innerHTML = '';
        
        function type() {
            if (i < text.length) {
                titleElement.innerHTML += text.charAt(i);
                i++;
                setTimeout(type, 100); // Typing speed
            } else {
                // titleElement.classList.add('blink'); // Removed blinking cursor effect
            }
        }
        type();
    }
}

function initEventListeners() {
    // Navigation
    dom.nav.analysis.addEventListener('click', (e) => {
        e.preventDefault();
        switchModule('analysis');
    });
    dom.nav.production.addEventListener('click', (e) => {
        e.preventDefault();
        switchModule('production');
    });

    // File Upload (Analysis)
    dom.analysis.uploadBox.addEventListener('click', (e) => {
        // Prevent triggering if clicking on the button itself (to avoid double trigger)
        if (e.target.tagName !== 'BUTTON') {
            dom.analysis.fileInput.click();
        }
    });
    dom.analysis.uploadBox.addEventListener('dragover', (e) => {
        e.preventDefault();
        dom.analysis.uploadBox.style.borderColor = 'var(--terminal-green)';
        dom.analysis.uploadBox.style.backgroundColor = 'rgba(0, 255, 0, 0.1)';
    });
    dom.analysis.uploadBox.addEventListener('dragleave', () => {
        dom.analysis.uploadBox.style.borderColor = 'var(--terminal-dim)';
        dom.analysis.uploadBox.style.backgroundColor = 'transparent';
    });
    dom.analysis.uploadBox.addEventListener('drop', (e) => {
        e.preventDefault();
        dom.analysis.uploadBox.style.borderColor = 'var(--terminal-dim)';
        dom.analysis.uploadBox.style.backgroundColor = 'transparent';
        
        if (e.dataTransfer.files.length > 0) {
            handleFileSelect(e.dataTransfer.files[0]);
        }
    });
    dom.analysis.fileInput.addEventListener('change', (e) => {
        if (e.target.files.length > 0) {
            handleFileSelect(e.target.files[0]);
        }
    });

    // Execute Analysis
    dom.analysis.executeBtn.addEventListener('click', executeAnalysis);

    // Export
    dom.analysis.exportBtn.addEventListener('click', exportReport);

    // Production File Upload
    if (dom.production.fileInput) {
        // Click handler for the custom button
        const uploadBtn = document.querySelector('#voucher-tab .upload-box button');
        if (uploadBtn) {
            uploadBtn.onclick = (e) => {
                e.preventDefault();
                logSystem('DEBUG', 'Upload button clicked', 'info');
                dom.production.fileInput.click();
            };
        } else {
            logSystem('WARN', 'Upload button selector failed', 'warning');
        }

        dom.production.fileInput.addEventListener('change', (e) => {
            logSystem('DEBUG', `File input changed. Files: ${e.target.files.length}`, 'info');
            if (e.target.files.length > 0) {
                handleVoucherFileSelect(e.target.files[0]);
            }
        });
    } else {
        logSystem('ERR', "Production file input not found in DOM!", 'error');
    }

    // Process Vouchers
    if (dom.production.processBtn) {
        dom.production.processBtn.addEventListener('click', processVouchers);
    }

    // Copy All
    if (dom.production.copyBtn) {
        dom.production.copyBtn.addEventListener('click', copyAllSkus);
    }

    // Automation
    dom.production.runBtn.addEventListener('click', startAutomation);
    dom.production.stopBtn.addEventListener('click', stopAutomation);

    // CLI Input
    dom.cli.input.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            if (currentInputType) {
                submitInput();
            } else {
                handleCliCommand(dom.cli.input.value);
                dom.cli.input.value = '';
            }
        }
    });
}

// --- CORE FUNCTIONS ---

function switchModule(moduleName) {
    // Update Nav
    dom.nav.analysis.classList.remove('active');
    dom.nav.production.classList.remove('active');
    dom.nav[moduleName].classList.add('active');

    // Update Content
    dom.modules.analysis.classList.remove('active');
    dom.modules.production.classList.remove('active');
    dom.modules[moduleName].classList.add('active');

    logSystem('NAV', `Switched to module: ${moduleName.toUpperCase()}`);
}

function logSystem(source, message, type = 'info') {
    const entry = document.createElement('div');
    entry.className = 'log-entry';
    
    const time = new Date().toLocaleTimeString('ro-RO', { hour12: false });
    const colorClass = type === 'error' ? 'val-error' : (type === 'success' ? 'val-success' : (type === 'warning' ? 'val-yellow' : 'val-info'));
    
    entry.innerHTML = `
        <span class="timestamp">[${time}]</span>
        <span class="${colorClass}">${source}:</span>
        <span>${message}</span>
    `;
    
    dom.logs.appendChild(entry);
    dom.logs.scrollTop = dom.logs.scrollHeight;
}

// --- ANALYSIS MODULE ---

function handleFileSelect(file) {
    const ext = file.name.split('.').pop().toLowerCase();
    if (ext !== 'xlsx' && ext !== 'xls') {
        logSystem('UPLOAD_ERROR', 'Invalid file format. Expected .xlsx or .xls', 'error');
        return;
    }

    dom.analysis.fileName.textContent = file.name;
    dom.analysis.fileName.classList.remove('dim');
    dom.analysis.fileName.classList.add('val-success');
    
    // Show execute button
    dom.analysis.executeBtn.style.display = 'inline-block';
    
    // Update hidden input if drag/drop was used
    if (dom.analysis.fileInput.files[0] !== file) {
        const container = new DataTransfer();
        container.items.add(file);
        dom.analysis.fileInput.files = container.files;
    }

    logSystem('FILE_LOAD', `File loaded: ${file.name}`);
}

async function executeAnalysis() {
    const file = dom.analysis.fileInput.files[0];
    if (!file) {
        logSystem('EXEC_ERROR', 'No file selected for analysis.', 'error');
        return;
    }

    logSystem('ANALYSIS', 'Starting analysis sequence...', 'info');
    dom.analysis.executeBtn.disabled = true;
    dom.analysis.executeBtn.textContent = '[ PROCESSING... ]';

    const formData = new FormData();
    formData.append('file', file);

    try {
        const response = await fetch('/upload', {
            method: 'POST',
            body: formData
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || 'Unknown server error');
        }

        currentFilename = data.filename;
        renderResults(data);
        logSystem('ANALYSIS', 'Analysis complete. Results rendered.', 'success');

    } catch (error) {
        logSystem('ANALYSIS_FAIL', error.message, 'error');
    } finally {
        dom.analysis.executeBtn.disabled = false;
        dom.analysis.executeBtn.textContent = '[ EXECUTE_ANALYSIS ]';
    }
}

function renderResults(data) {
    // Stats
    dom.analysis.stats.finalized.textContent = data.comenzi_finalizate;
    dom.analysis.stats.cancelled.textContent = data.comenzi_anulate;
    dom.analysis.stats.total.textContent = data.total_comenzi;
    dom.analysis.stats.grandTotal.textContent = data.sumar.total;

    // Table
    dom.analysis.tableBody.innerHTML = '';
    data.randuri.forEach(rand => {
        const tr = document.createElement('tr');
        
        // Helper for cell creation
        const createCell = (text, className = '') => {
            const td = document.createElement('td');
            td.textContent = text;
            if (className) td.className = className;
            return td;
        };

        tr.appendChild(createCell(rand.parfum || '', rand.este_prim ? 'val-success' : ''));
        tr.appendChild(createCell(rand.sku || '', 'dim'));
        tr.appendChild(createCell(`${rand.cantitate_ml} ml`));
        tr.appendChild(createCell(rand.bucati));
        tr.appendChild(createCell(rand.total || '', rand.total ? 'val-yellow' : ''));

        dom.analysis.tableBody.appendChild(tr);
    });

    // Summary Grid
    dom.analysis.summaryGrid.innerHTML = '';
    Object.entries(data.sumar.cantitati).forEach(([ml, bucati]) => {
        const div = document.createElement('div');
        div.className = 'terminal-card';
        div.style.padding = '10px';
        div.style.textAlign = 'center';
        div.innerHTML = `
            <div class="val-success" style="font-size: 1.5rem;">${bucati}</div>
            <div class="dim">${ml} ml</div>
        `;
        dom.analysis.summaryGrid.appendChild(div);
    });

    dom.analysis.results.style.display = 'block';
}

async function exportReport() {
    if (!currentFilename) {
        logSystem('EXPORT_ERR', 'No analysis data available to export.', 'error');
        return;
    }
    
    logSystem('EXPORT', `Downloading report: ${currentFilename}...`);
    window.location.href = `/export/${currentFilename}`;
}

// --- PRODUCTION MODULE (VOUCHERS) ---

function handleVoucherFileSelect(file) {
    logSystem('DEBUG', `Handling file: ${file.name}`, 'info');
    
    const ext = file.name.split('.').pop().toLowerCase();
    if (ext !== 'xlsx' && ext !== 'xls') {
        logSystem('UPLOAD_ERROR', 'Invalid file format. Expected .xlsx or .xls', 'error');
        return;
    }

    if (dom.production.fileName) {
        dom.production.fileName.textContent = file.name;
        dom.production.fileName.classList.remove('dim');
        dom.production.fileName.classList.add('val-success');
    } else {
        logSystem('ERR', 'fileName element missing', 'error');
    }
    
    // Show process button
    if (dom.production.processBtn) {
        dom.production.processBtn.style.display = 'inline-block';
        logSystem('DEBUG', 'Process button shown', 'info');
    } else {
        logSystem('ERR', "Process button not found in DOM", 'error');
    }
    
    logSystem('FILE_LOAD', `Production file loaded: ${file.name}`);
}

async function processVouchers() {
    const file = dom.production.fileInput.files[0];
    if (!file) {
        logSystem('EXEC_ERROR', 'No file selected for vouchers.', 'error');
        return;
    }

    logSystem('PRODUCTION', 'Processing vouchers...', 'info');
    dom.production.processBtn.disabled = true;
    dom.production.loading.style.display = 'block';
    dom.production.errorAlert.style.display = 'none';

    const formData = new FormData();
    formData.append('file', file);

    try {
        const response = await fetch('/process-vouchers', {
            method: 'POST',
            body: formData
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || 'Unknown server error');
        }

        currentVouchers = data.bonuri;
        renderVouchers(data);
        logSystem('PRODUCTION', `Processed ${data.total_bonuri} vouchers.`, 'success');

    } catch (error) {
        logSystem('PRODUCTION_FAIL', error.message, 'error');
        dom.production.errorAlert.style.display = 'block';
        dom.production.errorMessage.textContent = error.message;
    } finally {
        dom.production.processBtn.disabled = false;
        dom.production.loading.style.display = 'none';
    }
}

function renderVouchers(data) {
    dom.production.stats.totalBonuri.textContent = data.total_bonuri;
    dom.production.stats.totalBucati.textContent = data.total_bucati;

    dom.production.tableBody.innerHTML = '';
    data.bonuri.forEach(bon => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td class="dim">${bon.sku}</td>
            <td>${bon.nume}</td>
            <td class="val-success">${bon.cantitate}</td>
            <td class="dim">${bon.comenzi ? bon.comenzi.join(', ') : ''}</td>
            <td><button class="terminal-btn sm-btn" onclick="copyToClipboard('${bon.sku}')">[ COPY ]</button></td>
        `;
        dom.production.tableBody.appendChild(tr);
    });

    dom.production.resultsSection.style.display = 'block';
    dom.production.runBtn.style.display = 'inline-block';
}

function copyAllSkus() {
    if (!currentVouchers.length) return;
    const skus = currentVouchers.map(b => b.sku).join('\n');
    navigator.clipboard.writeText(skus).then(() => {
        logSystem('CLIPBOARD', 'All SKUs copied to clipboard.', 'success');
    });
}

function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(() => {
        logSystem('CLIPBOARD', `Copied: ${text}`, 'success');
    });
}

// --- PRODUCTION MODULE (AUTOMATION) ---

function startAutomation() {
    if (isProcessing) return;

    if (!currentVouchers || currentVouchers.length === 0) {
        logSystem('AUTO_ERR', 'No vouchers loaded. Please process a file first.', 'error');
        return;
    }

    logSystem('AUTO_INIT', 'Initializing Oblio Automation Bot...');

    // Show stop button, hide run button
    dom.production.runBtn.style.display = 'none';
    dom.production.stopBtn.style.display = 'inline-block';
    dom.production.stopBtn.disabled = false;
    dom.production.status.textContent = 'STATUS: RUNNING';
    dom.production.status.className = 'val-success blink';

    isProcessing = true;

    // Check if force mode is enabled
    const forceModeCheckbox = document.getElementById('forceModeCheckbox');
    const forceMode = forceModeCheckbox ? forceModeCheckbox.checked : false;

    socket.emit('start_automation_live', {
        bonuri: currentVouchers,
        force_mode: forceMode
    });
}

function stopAutomation() {
    logSystem('STOP_CMD', 'Sending INTERRUPT signal to server...', 'warning');
    socket.emit('stop_automation');
    dom.production.stopBtn.textContent = '[ STOPPING... ]';
    dom.production.stopBtn.disabled = true;
}

// --- SOCKET.IO EVENTS ---

socket.on('connect', () => {
    logSystem('NET', 'Socket connected.');
});

socket.on('log', (data) => {
    // data = { type: 'info'|'error'|'success', message: "..." }
    logSystem('SERVER', data.message, data.type);
});

socket.on('automation_stopped', (data) => {
    logSystem('STOP_CONFIRM', 'Process stopped by user.', 'success');
    resetAutomationUI();
});

socket.on('progress', (data) => {
    logSystem('PROGRESS', `Processing ${data.current}/${data.total}: ${data.sku} (${data.nume})`, 'info');
});

socket.on('bon_complete', (data) => {
    if (data.success) {
        logSystem('SUCCESS', data.message, 'success');
    } else {
        logSystem('FAIL', data.message, 'error');
    }
});

socket.on('automation_complete', (data) => {
    logSystem('COMPLETE', data.message || 'Automation sequence finished.', data.success ? 'success' : 'error');
    resetAutomationUI();
});

socket.on('input_required', (prompt) => {
    logSystem('INPUT', prompt.message || `Input required: ${prompt.type}`, 'warning');
    showInputSection(prompt);
});

function resetAutomationUI() {
    isProcessing = false;
    dom.production.runBtn.style.display = 'inline-block';
    dom.production.runBtn.disabled = false;
    dom.production.stopBtn.style.display = 'none';
    dom.production.stopBtn.disabled = true;
    dom.production.stopBtn.textContent = '[ KILL_PROCESS ]';
    dom.production.status.textContent = 'STATUS: IDLE';
    dom.production.status.className = 'dim';
}

// --- CLI HANDLER ---

function handleCliCommand(cmd) {
    const command = cmd.trim().toLowerCase();
    logSystem('USER', `> ${command}`);

    switch(command) {
        case 'help':
            logSystem('HELP', 'Available commands: help, clear, status, analysis, production, stop, /stop');
            break;
        case 'clear':
            dom.logs.innerHTML = '';
            break;
        case 'status':
            logSystem('STATUS', isProcessing ? 'Automation RUNNING' : 'System IDLE');
            break;
        case 'analysis':
            switchModule('analysis');
            break;
        case 'production':
            switchModule('production');
            break;
        case 'stop':
        case '/stop':
            if (isProcessing) {
                stopAutomation();
            } else {
                logSystem('INFO', 'No automation running.', 'info');
            }
            break;
        default:
            logSystem('ERR', `Command not found: ${command}`, 'error');
    }
}

// --- CLI / INPUT HANDLER ---

function showInputSection(prompt) {
    currentInputType = prompt.type;
    
    if (dom.cli.section) {
        dom.cli.section.style.display = 'block';
        dom.cli.input.focus();
        
        if (prompt.type === 'password') {
            dom.cli.input.type = 'password';
            dom.cli.prompt.textContent = 'PASSWORD>';
            dom.cli.input.placeholder = 'Enter password...';
        } else if (prompt.type === '2fa') {
            dom.cli.input.type = 'text';
            dom.cli.prompt.textContent = '2FA_CODE>';
            dom.cli.input.placeholder = 'Enter 2FA code...';
        } else {
            dom.cli.input.type = 'text';
            dom.cli.prompt.textContent = 'INPUT>';
            dom.cli.input.placeholder = 'Enter value...';
        }
    }
}

function submitInput() {
    const value = dom.cli.input.value.trim();
    if (!value) return;

    logSystem('USER', `Sending input (${currentInputType})...`);
    
    socket.emit('user_input', {
        type: currentInputType,
        value: value
    });

    dom.cli.input.value = '';
    // Reset to default CLI state instead of hiding
    currentInputType = null;
    dom.cli.input.type = 'text';
    dom.cli.prompt.textContent = '$';
    dom.cli.input.placeholder = 'Type command...';
}
