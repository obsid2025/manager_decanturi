// ==UserScript==
// @name         OBSID - Automatizare Bonuri Producție Oblio v2.1 DEBUG
// @namespace    http://tampermonkey.net/
// @version      2.1
// @description  Creează automat bonuri de producție în Oblio - VERSIUNE DEBUG
// @author       OBSID
// @match        https://www.oblio.eu/stock/production*
// @match        https://www.oblio.eu/stock/production/*
// @match        https://*.oblio.eu/stock/production*
// @include      https://www.oblio.eu/stock/production*
// @grant        window.close
// @grant        GM_log
// @run-at       document-idle
// ==/UserScript==

(function() {
    'use strict';

    // DEBUGGING - Verifică că scriptul se încarcă
    console.log('%c🤖 OBSID Automation Script v2.1 DEBUG - SCRIPT LOADED!', 'background: #667eea; color: white; font-size: 16px; padding: 5px; font-weight: bold;');
    console.log('URL current:', window.location.href);
    console.log('Document ready state:', document.readyState);
    console.log('Timestamp:', new Date().toISOString());

    // Adaugă indicator IMEDIAT (fără să aștepte DOM)
    function addLoadIndicator() {
        const indicator = document.createElement('div');
        indicator.id = 'obsid-script-loaded-indicator';
        indicator.innerHTML = `
            <div style="position: fixed; top: 10px; left: 10px; z-index: 999999; background: #00ff00; color: black; padding: 10px 20px; border-radius: 8px; box-shadow: 0 4px 15px rgba(0,0,0,0.3); font-family: Arial, sans-serif; font-size: 14px; font-weight: bold;">
                ✅ SCRIPT v2.1 LOADED!
            </div>
        `;

        if (document.body) {
            document.body.appendChild(indicator);
            console.log('✅ Indicator vizual adăugat în pagină!');
        } else {
            console.log('⚠️ document.body nu e disponibil încă, aștept...');
            setTimeout(addLoadIndicator, 100);
        }
    }

    // Funcție pentru așteptare
    function sleep(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }

    // Funcție pentru așteptare element
    function waitForElement(selector, timeout = 20000) {
        console.log(`🔍 Căutare element: ${selector} (timeout: ${timeout}ms)`);
        return new Promise((resolve, reject) => {
            const startTime = Date.now();
            const interval = setInterval(() => {
                const element = document.querySelector(selector);
                if (element && element.offsetParent !== null) {
                    clearInterval(interval);
                    console.log(`✅ Element găsit: ${selector}`);
                    resolve(element);
                } else if (Date.now() - startTime > timeout) {
                    clearInterval(interval);
                    console.error(`❌ Element ${selector} not found after ${timeout}ms`);
                    reject(new Error(`Element ${selector} not found after ${timeout}ms`));
                }
            }, 100);
        });
    }

    // Funcție pentru simulare tastare character-by-character
    async function typeIntoInput(input, text) {
        console.log(`⌨️ Începe tastarea textului: "${text}"`);
        input.value = '';
        input.focus();
        await sleep(300);

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
        console.log(`✅ Tastare completă. Value: "${input.value}"`);
        await sleep(500);
    }

    // Funcție principală de automatizare
    async function automateProductionVoucher() {
        console.log('🚀 ========== PORNIRE AUTOMATION ==========');

        try {
            // Extrage parametrii din URL
            const urlParams = new URLSearchParams(window.location.search);
            const sku = urlParams.get('sku');
            const qty = urlParams.get('qty');
            const autoClose = urlParams.get('autoclose') === 'true';

            console.log('📋 Parametri URL:');
            console.log('  - SKU:', sku);
            console.log('  - QTY:', qty);
            console.log('  - AutoClose:', autoClose);

            // Verifică dacă există parametri
            if (!sku || !qty) {
                console.log('⚠️ Nu există parametri SKU/QTY în URL - script inactiv');
                return;
            }

            console.log(`🎯 START AUTOMATION: SKU=${sku}, QTY=${qty}, AutoClose=${autoClose}`);

            // Adaugă indicator vizual de procesare
            const indicator = document.createElement('div');
            indicator.id = 'obsid-automation-indicator';
            indicator.innerHTML = `
                <div style="position: fixed; top: 10px; right: 10px; z-index: 999999; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 15px 25px; border-radius: 10px; box-shadow: 0 4px 15px rgba(0,0,0,0.3); font-family: Arial, sans-serif; font-size: 14px; font-weight: bold;">
                    🤖 OBSID Automation v2.1<br>
                    <span style="font-size: 12px; opacity: 0.9;">SKU: ${sku}<br>Cantitate: ${qty}</span><br>
                    <div id="automation-status" style="margin-top: 8px; font-size: 11px; opacity: 0.8;">Se inițializează...</div>
                </div>
            `;
            document.body.appendChild(indicator);
            console.log('✅ Indicator procesare adăugat');

            function updateStatus(message, color = 'white') {
                const statusEl = document.getElementById('automation-status');
                if (statusEl) {
                    statusEl.textContent = message;
                    statusEl.style.color = color;
                }
                console.log(`📊 Status: ${message}`);
            }

            // Așteaptă pagina să se încarce COMPLET
            updateStatus('Așteptare încărcare completă...');
            console.log('⏳ Așteptare 3 secunde pentru încărcare completă pagină + jQuery...');
            await sleep(3000);

            // PASUL 1: Găsește input-ul pentru SKU
            updateStatus('Căutare câmp SKU...');
            console.log('🔍 Căutare input #pp_name...');

            const ppNameInput = await waitForElement('#pp_name', 20000);
            console.log('✅ Input #pp_name găsit:', ppNameInput);
            console.log('  - Value curent:', ppNameInput.value);
            console.log('  - Placeholder:', ppNameInput.placeholder);

            // PASUL 2: Completează SKU-ul folosind simulare tastare
            updateStatus('Tastare SKU character-by-character...');
            console.log(`⌨️ Începe tastarea SKU: "${sku}"`);

            await typeIntoInput(ppNameInput, sku);

            console.log(`✅ SKU introdus în input. Value: "${ppNameInput.value}"`);

            // PASUL 3: Trigger autocomplete jQuery UI
            updateStatus('Trigger autocomplete jQuery UI...');
            console.log('🔍 Trigger autocomplete...');

            // Verifică dacă jQuery și jQuery UI sunt disponibile
            if (typeof window.$ !== 'undefined' && typeof window.$.ui !== 'undefined') {
                console.log('✅ jQuery și jQuery UI sunt disponibile');
                try {
                    window.$(ppNameInput).autocomplete('search', sku);
                    console.log('✅ jQuery UI autocomplete trigger-uit cu succes');
                } catch (e) {
                    console.error('❌ Eroare la trigger jQuery UI autocomplete:', e);
                }
            } else {
                console.log('⚠️ jQuery sau jQuery UI nu sunt disponibile');
                console.log('  - jQuery:', typeof window.$);
                console.log('  - jQuery UI:', typeof window.$.ui);
            }

            // Așteaptă autocomplete să apară
            updateStatus('Așteptare autocomplete...');
            console.log('⏳ Așteptare 3 secunde pentru autocomplete...');
            await sleep(3000);

            // PASUL 4: Selectează primul rezultat din autocomplete
            updateStatus('Selectare produs din autocomplete...');
            console.log('🔍 Căutare rezultate autocomplete...');

            // Încearcă multiple selectoare pentru autocomplete
            const autocompleteSelectors = [
                '.ui-autocomplete .ui-menu-item',
                '.ui-menu-item',
                '.ui-autocomplete li',
                '[role="option"]'
            ];

            let autocompleteItems = [];
            for (const selector of autocompleteSelectors) {
                autocompleteItems = document.querySelectorAll(selector);
                if (autocompleteItems.length > 0) {
                    console.log(`✅ Autocomplete găsit cu selector: ${selector}`);
                    break;
                }
            }

            console.log(`📊 Autocomplete items găsite: ${autocompleteItems.length}`);

            if (autocompleteItems.length > 0) {
                console.log(`✅ ${autocompleteItems.length} rezultate în autocomplete`);
                updateStatus(`Selectare produs (${autocompleteItems.length} rezultate)...`);

                // Click pe primul rezultat
                const firstItem = autocompleteItems[0];
                console.log('🖱️ Click pe primul rezultat:', firstItem.textContent.trim());
                firstItem.click();

                await sleep(1500);
            } else {
                console.log('⚠️ Autocomplete nu a apărut după 3s');
                updateStatus('⚠️ Autocomplete nu a apărut, trimit ENTER...');

                // Dacă nu există autocomplete, trimite ENTER
                ppNameInput.dispatchEvent(new KeyboardEvent('keydown', {
                    key: 'Enter',
                    code: 'Enter',
                    keyCode: 13,
                    which: 13,
                    bubbles: true
                }));

                await sleep(1500);
            }

            // PASUL 5: Verifică dacă produsul a fost selectat
            await sleep(1000);
            updateStatus('Verificare selecție produs...');
            console.log('🔍 Verificare #pp_name_id...');

            const ppNameId = document.querySelector('#pp_name_id');
            console.log('📊 Element #pp_name_id:', ppNameId);
            console.log('  - Value:', ppNameId?.value);

            if (!ppNameId || !ppNameId.value) {
                throw new Error(`Produsul nu a fost selectat! SKU "${sku}" invalid sau nu există în baza de date.`);
            }

            console.log(`✅ Produs selectat cu ID: ${ppNameId.value}`);

            // PASUL 6: Completează cantitatea
            updateStatus('Setare cantitate...');
            console.log('🔢 Completare cantitate...');

            const ppQuantityInput = await waitForElement('#pp_quantity', 20000);
            console.log('✅ Input #pp_quantity găsit:', ppQuantityInput);

            ppQuantityInput.value = '';
            ppQuantityInput.focus();
            await sleep(400);
            ppQuantityInput.value = qty;
            ppQuantityInput.dispatchEvent(new Event('input', { bubbles: true }));
            ppQuantityInput.dispatchEvent(new Event('change', { bubbles: true }));

            console.log(`✅ Cantitate setată: ${qty}`);
            await sleep(700);

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
                        console.log(`✅ Buton salvare găsit cu selector: ${selector}`);
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
                        console.log('✅ Buton salvare găsit prin text:', btn.textContent.trim());
                        break;
                    }
                }
            }

            if (saveButton) {
                updateStatus('Salvare bon...');
                console.log('🖱️ Click buton salvare...');

                saveButton.click();

                console.log('✅ Buton salvare apăsat');
                await sleep(4000); // Așteaptă salvarea

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
                        console.log(`✅ Mesaj succes găsit: ${selector}`);
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
                await sleep(2500);

                // Închide tab-ul dacă autoclose=true
                if (autoClose) {
                    updateStatus('Se închide tab-ul...', '#00ff00');
                    console.log('🚪 Închidere tab în 1 secundă...');
                    await sleep(1000);
                    window.close();
                } else {
                    console.log('ℹ️ Tab rămâne deschis (autoclose=false)');
                }

            } else {
                throw new Error('Nu s-a găsit butonul de salvare!');
            }

            console.log('✅ ========== AUTOMATION FINALIZATĂ ==========');

        } catch (error) {
            console.error('❌ ========== EROARE AUTOMATION ==========');
            console.error('Eroare:', error);
            console.error('Stack:', error.stack);

            // Afișare eroare vizual
            const indicator = document.getElementById('obsid-automation-indicator');
            if (indicator) {
                indicator.innerHTML = `
                    <div style="position: fixed; top: 10px; right: 10px; z-index: 999999; background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); color: white; padding: 15px 25px; border-radius: 10px; box-shadow: 0 4px 15px rgba(0,0,0,0.3); font-family: Arial, sans-serif; font-size: 14px; font-weight: bold;">
                        ❌ EROARE AUTOMATIZARE<br>
                        <span style="font-size: 11px; opacity: 0.9; display: block; margin-top: 5px; max-width: 300px; word-wrap: break-word;">${error.message}</span><br>
                        <button onclick="console.log('Detalii eroare:', ${JSON.stringify(error.message)}); window.close();" style="margin-top: 10px; padding: 5px 15px; background: white; color: #f5576c; border: none; border-radius: 5px; cursor: pointer; font-weight: bold;">Închide Tab</button>
                    </div>
                `;
            }

            // Păstrează tab-ul deschis pentru debugging
            console.log('🐛 Tab rămas deschis pentru debugging');
        }
    }

    // Adaugă indicator de loading imediat
    if (document.readyState === 'loading') {
        console.log('📄 Document loading - adăug indicator când e ready');
        document.addEventListener('DOMContentLoaded', addLoadIndicator);
    } else {
        console.log('📄 Document deja loaded - adăug indicator imediat');
        addLoadIndicator();
    }

    // Pornește automatizarea când pagina e COMPLET încărcată
    // Încercăm multiple momente de pornire pentru a prinde sigur încărcarea
    console.log('🔄 Setare listeners pentru pornire automation...');

    if (document.readyState === 'complete') {
        console.log('📄 Document ready: complete - start automation în 2s');
        setTimeout(automateProductionVoucher, 2000);
    } else {
        console.log('📄 Document ready:', document.readyState);

        // Listener pentru DOMContentLoaded
        document.addEventListener('DOMContentLoaded', () => {
            console.log('📄 DOMContentLoaded event - start automation în 2s');
            setTimeout(automateProductionVoucher, 2000);
        });

        // Listener pentru load complet
        window.addEventListener('load', () => {
            console.log('📄 Window load event - start automation în 2s');
            setTimeout(automateProductionVoucher, 2000);
        });
    }

    console.log('✅ Script v2.1 DEBUG setup complet!');

})();
