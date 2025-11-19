// ==UserScript==
// @name         OBSID - Automatizare Bonuri Producție Oblio
// @namespace    http://tampermonkey.net/
// @version      1.0
// @description  Creează automat bonuri de producție în Oblio din parametrii URL
// @author       OBSID
// @match        https://www.oblio.eu/stock/production/*
// @grant        window.close
// @run-at       document-idle
// ==/UserScript==

(function() {
    'use strict';

    console.log('🤖 OBSID Automation Script - LOADED');

    // Funcție pentru așteptare
    function sleep(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }

    // Funcție pentru așteptare element
    function waitForElement(selector, timeout = 10000) {
        return new Promise((resolve, reject) => {
            const startTime = Date.now();
            const interval = setInterval(() => {
                const element = document.querySelector(selector);
                if (element) {
                    clearInterval(interval);
                    resolve(element);
                } else if (Date.now() - startTime > timeout) {
                    clearInterval(interval);
                    reject(new Error(`Element ${selector} not found after ${timeout}ms`));
                }
            }, 100);
        });
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

            console.log(`🚀 START AUTOMATION: SKU=${sku}, QTY=${qty}`);

            // Adaugă indicator vizual
            const indicator = document.createElement('div');
            indicator.id = 'obsid-automation-indicator';
            indicator.innerHTML = `
                <div style="position: fixed; top: 10px; right: 10px; z-index: 99999; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 15px 25px; border-radius: 10px; box-shadow: 0 4px 15px rgba(0,0,0,0.3); font-family: Arial, sans-serif; font-size: 14px; font-weight: bold;">
                    🤖 OBSID Automation<br>
                    <span style="font-size: 12px; opacity: 0.9;">SKU: ${sku}<br>Cantitate: ${qty}</span><br>
                    <div id="automation-status" style="margin-top: 8px; font-size: 11px; opacity: 0.8;">Se procesează...</div>
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

            // Așteaptă pagina să se încarce complet
            await sleep(1000);
            updateStatus('Așteptare pagină...');

            // PASUL 1: Găsește input-ul pentru SKU
            updateStatus('Căutare câmp SKU...');
            const ppNameInput = await waitForElement('#pp_name');
            console.log('✅ Câmp SKU găsit');

            // PASUL 2: Șterge conținutul existent
            ppNameInput.value = '';
            ppNameInput.focus();
            await sleep(300);

            // PASUL 3: Introdu SKU-ul
            updateStatus('Introducere SKU...');
            ppNameInput.value = sku;

            // Trigger input event pentru autocomplete
            ppNameInput.dispatchEvent(new Event('input', { bubbles: true }));
            ppNameInput.dispatchEvent(new Event('keyup', { bubbles: true }));

            console.log(`✅ SKU introdus: ${sku}`);
            await sleep(1500); // Așteaptă autocomplete

            // PASUL 4: Selectează primul rezultat din autocomplete
            updateStatus('Selectare produs...');

            // Încearcă să găsească autocomplete dropdown
            const autocompleteItems = document.querySelectorAll('.ui-autocomplete .ui-menu-item');

            if (autocompleteItems.length > 0) {
                console.log(`✅ Autocomplete găsit: ${autocompleteItems.length} rezultate`);
                autocompleteItems[0].click();
                await sleep(500);
            } else {
                // Dacă nu există autocomplete, trimite ENTER
                console.log('⚠️ Autocomplete nu a apărut, trimit ENTER');
                const enterEvent = new KeyboardEvent('keydown', {
                    key: 'Enter',
                    code: 'Enter',
                    keyCode: 13,
                    which: 13,
                    bubbles: true
                });
                ppNameInput.dispatchEvent(enterEvent);
                await sleep(800);
            }

            // PASUL 5: Verifică dacă produsul a fost selectat
            await sleep(500);
            const ppNameId = document.querySelector('#pp_name_id');
            if (!ppNameId || !ppNameId.value) {
                throw new Error('Produsul nu a fost selectat! SKU invalid sau nu există în baza de date.');
            }
            console.log(`✅ Produs selectat ID: ${ppNameId.value}`);

            // PASUL 6: Completează cantitatea
            updateStatus('Setare cantitate...');
            const ppQuantityInput = await waitForElement('#pp_quantity');
            ppQuantityInput.value = '';
            ppQuantityInput.focus();
            await sleep(200);
            ppQuantityInput.value = qty;
            ppQuantityInput.dispatchEvent(new Event('input', { bubbles: true }));
            ppQuantityInput.dispatchEvent(new Event('change', { bubbles: true }));
            console.log(`✅ Cantitate setată: ${qty}`);
            await sleep(300);

            // PASUL 7: Găsește și apasă butonul de salvare
            updateStatus('Salvare bon...');

            // Încearcă diferite selectors pentru butonul de salvare
            let saveButton = null;
            const saveSelectors = [
                'button[type="submit"]',
                'button:contains("Salvare")',
                '#save_production_btn',
                '.btn-primary[type="submit"]',
                'button.btn.btn-primary'
            ];

            for (const selector of saveSelectors) {
                try {
                    saveButton = document.querySelector(selector);
                    if (saveButton && saveButton.offsetParent !== null) {
                        console.log(`✅ Buton salvare găsit: ${selector}`);
                        break;
                    }
                } catch (e) {
                    continue;
                }
            }

            if (!saveButton) {
                // Caută prin toate butoanele
                const allButtons = document.querySelectorAll('button');
                for (const btn of allButtons) {
                    if (btn.textContent.includes('Salvare') || btn.textContent.includes('Salveaza')) {
                        saveButton = btn;
                        console.log('✅ Buton salvare găsit prin text');
                        break;
                    }
                }
            }

            if (saveButton) {
                saveButton.click();
                console.log('✅ Buton salvare apăsat');
                await sleep(2000); // Așteaptă salvarea

                // Verifică mesaj de succes
                const successMsg = document.querySelector('.alert-success, .success-message, [class*="success"]');
                if (successMsg) {
                    console.log('🎉 BON CREAT CU SUCCES!');
                    updateStatus('✅ BON CREAT CU SUCCES!', '#00ff00');
                } else {
                    console.log('⚠️ Nu s-a detectat mesaj de confirmare');
                    updateStatus('⚠️ Verifică rezultatul...', '#ffff00');
                }

                // Așteaptă puțin pentru vizualizare
                await sleep(2000);

                // Închide tab-ul dacă autoclose=true
                if (autoClose) {
                    updateStatus('Se închide tab-ul...', '#00ff00');
                    await sleep(1000);
                    window.close();
                }

            } else {
                throw new Error('Nu s-a găsit butonul de salvare!');
            }

        } catch (error) {
            console.error('❌ EROARE:', error);

            // Afișare eroare vizual
            const indicator = document.getElementById('obsid-automation-indicator');
            if (indicator) {
                indicator.innerHTML = `
                    <div style="position: fixed; top: 10px; right: 10px; z-index: 99999; background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); color: white; padding: 15px 25px; border-radius: 10px; box-shadow: 0 4px 15px rgba(0,0,0,0.3); font-family: Arial, sans-serif; font-size: 14px; font-weight: bold;">
                        ❌ EROARE AUTOMATIZARE<br>
                        <span style="font-size: 11px; opacity: 0.9;">${error.message}</span><br>
                        <button onclick="window.close()" style="margin-top: 10px; padding: 5px 15px; background: white; color: #f5576c; border: none; border-radius: 5px; cursor: pointer; font-weight: bold;">Închide Tab</button>
                    </div>
                `;
            }
        }
    }

    // Pornește automatizarea când pagina e încărcată
    if (document.readyState === 'complete') {
        automateProductionVoucher();
    } else {
        window.addEventListener('load', automateProductionVoucher);
    }

})();
