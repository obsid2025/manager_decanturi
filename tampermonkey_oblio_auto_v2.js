// ==UserScript==
// @name         OBSID - Automatizare Bonuri Producție Oblio v2
// @namespace    http://tampermonkey.net/
// @version      2.0
// @description  Creează automat bonuri de producție în Oblio - VERSION ÎMBUNĂTĂȚITĂ
// @author       OBSID
// @match        https://www.oblio.eu/stock/production/*
// @grant        window.close
// @run-at       document-end
// ==/UserScript==

(function() {
    'use strict';

    console.log('🤖 OBSID Automation Script v2.0 - LOADED');

    // Funcție pentru așteptare
    function sleep(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }

    // Funcție pentru așteptare element
    function waitForElement(selector, timeout = 15000) {
        return new Promise((resolve, reject) => {
            const startTime = Date.now();
            const interval = setInterval(() => {
                const element = document.querySelector(selector);
                if (element && element.offsetParent !== null) {
                    clearInterval(interval);
                    resolve(element);
                } else if (Date.now() - startTime > timeout) {
                    clearInterval(interval);
                    reject(new Error(`Element ${selector} not found after ${timeout}ms`));
                }
            }, 100);
        });
    }

    // Funcție pentru simulare tastare character-by-character
    async function typeIntoInput(input, text) {
        input.value = '';
        input.focus();
        await sleep(200);

        // Tastează fiecare caracter
        for (let i = 0; i < text.length; i++) {
            input.value += text[i];

            // Trigger evenimente pentru fiecare caracter
            input.dispatchEvent(new Event('input', { bubbles: true }));
            input.dispatchEvent(new KeyboardEvent('keydown', {
                key: text[i],
                bubbles: true
            }));
            input.dispatchEvent(new KeyboardEvent('keypress', {
                key: text[i],
                bubbles: true
            }));
            input.dispatchEvent(new KeyboardEvent('keyup', {
                key: text[i],
                bubbles: true
            }));

            await sleep(50); // Delay între caractere
        }

        // Trigger final
        input.dispatchEvent(new Event('change', { bubbles: true }));
        await sleep(300);
    }

    // Funcție principală de automatizare
    async function automateProductionVoucher() {
        try {
            // Extrage parametrii din URL
            const urlParams = new URLSearchParams(window.location.search);
            const sku = urlParams.get('sku');
            const qty = urlParams.get('qty');
            const autoClose = urlParams.get('autoclose') === 'true';

            // Verifică dacă există parametri
            if (!sku || !qty) {
                console.log('⚠️ Nu există parametri SKU/QTY în URL - script inactiv');
                return;
            }

            console.log(`🚀 START AUTOMATION v2.0: SKU=${sku}, QTY=${qty}, AutoClose=${autoClose}`);

            // Adaugă indicator vizual
            const indicator = document.createElement('div');
            indicator.id = 'obsid-automation-indicator';
            indicator.innerHTML = `
                <div style="position: fixed; top: 10px; right: 10px; z-index: 99999; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 15px 25px; border-radius: 10px; box-shadow: 0 4px 15px rgba(0,0,0,0.3); font-family: Arial, sans-serif; font-size: 14px; font-weight: bold;">
                    🤖 OBSID Automation v2<br>
                    <span style="font-size: 12px; opacity: 0.9;">SKU: ${sku}<br>Cantitate: ${qty}</span><br>
                    <div id="automation-status" style="margin-top: 8px; font-size: 11px; opacity: 0.8;">Se inițializează...</div>
                </div>
            `;
            document.body.appendChild(indicator);

            function updateStatus(message, color = 'white') {
                const statusEl = document.getElementById('automation-status');
                if (statusEl) {
                    statusEl.textContent = message;
                    statusEl.style.color = color;
                }
            }

            // Așteaptă pagina să se încarce COMPLET (inclusiv jQuery UI)
            await sleep(2000);
            updateStatus('Așteptare încărcare completă...');
            console.log('⏳ Așteptare 2 secunde pentru încărcare completă...');

            // PASUL 1: Găsește input-ul pentru SKU
            updateStatus('Căutare câmp SKU...');
            console.log('🔍 Căutare input #pp_name...');
            const ppNameInput = await waitForElement('#pp_name');
            console.log('✅ Câmp SKU găsit:', ppNameInput);

            // PASUL 2: Completează SKU-ul folosind simulare tastare
            updateStatus('Tastare SKU caracter cu caracter...');
            console.log(`⌨️ Tastare SKU: ${sku}`);

            await typeIntoInput(ppNameInput, sku);

            console.log(`✅ SKU introdus în input: "${ppNameInput.value}"`);

            // PASUL 3: Trigger autocomplete jQuery UI
            updateStatus('Trigger autocomplete...');
            console.log('🔍 Trigger autocomplete jQuery UI...');

            // Trigger autocomplete jQuery UI explicit
            if (window.$ && window.$.ui) {
                try {
                    $(ppNameInput).autocomplete('search', sku);
                    console.log('✅ jQuery UI autocomplete trigger-uit');
                } catch (e) {
                    console.log('⚠️ jQuery UI autocomplete error:', e);
                }
            }

            // Așteaptă autocomplete să apară
            await sleep(2500);

            // PASUL 4: Selectează primul rezultat din autocomplete
            updateStatus('Selectare produs din autocomplete...');
            console.log('🔍 Căutare rezultate autocomplete...');

            // Încearcă să găsească autocomplete dropdown (jQuery UI)
            let autocompleteItems = document.querySelectorAll('.ui-autocomplete .ui-menu-item');

            if (autocompleteItems.length === 0) {
                // Încercă selector alternativ
                autocompleteItems = document.querySelectorAll('.ui-menu-item');
            }

            if (autocompleteItems.length > 0) {
                console.log(`✅ Autocomplete găsit: ${autocompleteItems.length} rezultate`);
                updateStatus(`Selectare produs (${autocompleteItems.length} rezultate)...`);

                // Click pe primul rezultat
                const firstItem = autocompleteItems[0];
                console.log('🖱️ Click pe primul rezultat:', firstItem.textContent);
                firstItem.click();

                await sleep(1000);
            } else {
                console.log('⚠️ Autocomplete nu a apărut după 2.5s');
                updateStatus('⚠️ Autocomplete nu a apărut, trimit ENTER...');

                // Dacă nu există autocomplete, trimite ENTER
                ppNameInput.dispatchEvent(new KeyboardEvent('keydown', {
                    key: 'Enter',
                    code: 'Enter',
                    keyCode: 13,
                    which: 13,
                    bubbles: true
                }));

                await sleep(1000);
            }

            // PASUL 5: Verifică dacă produsul a fost selectat
            await sleep(800);
            updateStatus('Verificare selecție produs...');

            const ppNameId = document.querySelector('#pp_name_id');
            console.log('🔍 Verificare pp_name_id:', ppNameId, 'Value:', ppNameId?.value);

            if (!ppNameId || !ppNameId.value) {
                throw new Error(`Produsul nu a fost selectat! SKU "${sku}" invalid sau nu există în baza de date.`);
            }

            console.log(`✅ Produs selectat cu ID: ${ppNameId.value}`);

            // PASUL 6: Completează cantitatea
            updateStatus('Setare cantitate...');
            console.log('🔢 Completare cantitate...');

            const ppQuantityInput = await waitForElement('#pp_quantity');
            ppQuantityInput.value = '';
            ppQuantityInput.focus();
            await sleep(300);
            ppQuantityInput.value = qty;
            ppQuantityInput.dispatchEvent(new Event('input', { bubbles: true }));
            ppQuantityInput.dispatchEvent(new Event('change', { bubbles: true }));

            console.log(`✅ Cantitate setată: ${qty}`);
            await sleep(500);

            // PASUL 7: Găsește și apasă butonul de salvare
            updateStatus('Căutare buton salvare...');
            console.log('🔍 Căutare buton salvare...');

            // Încearcă diferite selectors pentru butonul de salvare
            let saveButton = null;
            const saveSelectors = [
                'button[type="submit"]',
                '#save_production_btn',
                '.btn-primary[type="submit"]',
                'button.btn.btn-primary',
                'form button[type="submit"]'
            ];

            for (const selector of saveSelectors) {
                try {
                    const btn = document.querySelector(selector);
                    if (btn && btn.offsetParent !== null) {
                        saveButton = btn;
                        console.log(`✅ Buton salvare găsit: ${selector}`);
                        break;
                    }
                } catch (e) {
                    continue;
                }
            }

            if (!saveButton) {
                // Caută prin toate butoanele
                console.log('🔍 Căutare buton prin text...');
                const allButtons = document.querySelectorAll('button');
                for (const btn of allButtons) {
                    const text = btn.textContent.toLowerCase();
                    if (text.includes('salvare') || text.includes('salveaza') || text.includes('save')) {
                        saveButton = btn;
                        console.log('✅ Buton salvare găsit prin text:', btn.textContent);
                        break;
                    }
                }
            }

            if (saveButton) {
                updateStatus('Salvare bon...');
                console.log('🖱️ Click buton salvare...');

                saveButton.click();

                console.log('✅ Buton salvare apăsat');
                await sleep(3000); // Așteaptă salvarea

                // Verifică mesaj de succes
                const successSelectors = [
                    '.alert-success',
                    '.success-message',
                    '[class*="success"]',
                    '.toast-success'
                ];

                let successMsg = null;
                for (const selector of successSelectors) {
                    successMsg = document.querySelector(selector);
                    if (successMsg && successMsg.offsetParent !== null) {
                        break;
                    }
                }

                if (successMsg) {
                    console.log('🎉 BON CREAT CU SUCCES!');
                    updateStatus('✅ BON CREAT CU SUCCES!', '#00ff00');
                } else {
                    console.log('⚠️ Nu s-a detectat mesaj de confirmare (posibil creat)');
                    updateStatus('✅ Salvat (verifică manual)', '#ffff00');
                }

                // Așteaptă puțin pentru vizualizare
                await sleep(2000);

                // Închide tab-ul dacă autoclose=true
                if (autoClose) {
                    updateStatus('Se închide tab-ul...', '#00ff00');
                    console.log('🚪 Închidere tab...');
                    await sleep(1000);
                    window.close();
                } else {
                    console.log('ℹ️ Tab rămâne deschis (autoclose=false)');
                }

            } else {
                throw new Error('Nu s-a găsit butonul de salvare!');
            }

        } catch (error) {
            console.error('❌ EROARE AUTOMATION:', error);

            // Afișare eroare vizual
            const indicator = document.getElementById('obsid-automation-indicator');
            if (indicator) {
                indicator.innerHTML = `
                    <div style="position: fixed; top: 10px; right: 10px; z-index: 99999; background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); color: white; padding: 15px 25px; border-radius: 10px; box-shadow: 0 4px 15px rgba(0,0,0,0.3); font-family: Arial, sans-serif; font-size: 14px; font-weight: bold;">
                        ❌ EROARE AUTOMATIZARE<br>
                        <span style="font-size: 11px; opacity: 0.9; display: block; margin-top: 5px; max-width: 300px; word-wrap: break-word;">${error.message}</span><br>
                        <button onclick="window.close()" style="margin-top: 10px; padding: 5px 15px; background: white; color: #f5576c; border: none; border-radius: 5px; cursor: pointer; font-weight: bold;">Închide Tab</button>
                    </div>
                `;
            }

            // Păstrează tab-ul deschis pentru debugging
            console.log('🐛 Tab rămas deschis pentru debugging');
        }
    }

    // Pornește automatizarea când pagina e COMPLET încărcată
    if (document.readyState === 'complete') {
        console.log('📄 Document ready: complete - start imediat');
        setTimeout(automateProductionVoucher, 1000);
    } else {
        console.log('📄 Document ready:', document.readyState, '- așteptare load event');
        window.addEventListener('load', () => {
            console.log('📄 Load event triggered - start automation');
            setTimeout(automateProductionVoucher, 1000);
        });
    }

})();
