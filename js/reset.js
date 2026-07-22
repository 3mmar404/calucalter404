// reset.js - Reset buttons for all tabs (bilingual)

document.addEventListener('DOMContentLoaded', () => {
  const $ = window.$;
  const $$ = window.$$;
  const T = (k) => (window.t ? window.t(k) : k);
  const fmt = (n) => (window.formatCurrency ? window.formatCurrency(n) : String(n));

  function addResetButton(tabId, resetFn) {
    const tab = document.getElementById(tabId);
    if (!tab) return;
    if (tab.querySelector('.reset-btn')) return;

    const btn = document.createElement('button');
    btn.type = 'button';
    btn.className = 'reset-btn btn bg-red-500 hover:bg-red-600 text-white px-4 py-2 rounded-lg shadow-lg hover:shadow-xl hover:scale-105 transition-all mb-4 float-right';
    // The <span data-i18n> lets the shared i18n layer re-translate this on language change.
    btn.innerHTML = `<i class="fas fa-rotate-left"></i> <span data-i18n="reset_btn">${T('reset_btn')}</span>`;
    btn.onclick = resetFn;

    tab.insertBefore(btn, tab.firstChild);
    const clearDiv = document.createElement('div');
    clearDiv.className = 'clear-both mb-4';
    tab.insertBefore(clearDiv, btn.nextSibling);
  }

  addResetButton('calculator', () => {
    const calcDisplay = $('#calcDisplay');
    const calcExpression = $('#calcExpression');
    const historyList = $('#historyList');
    if (calcDisplay) calcDisplay.value = '0';
    if (calcExpression) calcExpression.textContent = '';
    if (historyList) historyList.innerHTML = `<p class="text-gray-500 text-center py-4">${T('no_history')}</p>`;
    localStorage.removeItem('calcHistory');
    alert(T('reset_calc'));
  });

  addResetButton('inventory', () => {
    $$('.denomination-input').forEach(input => input.value = '');
    const inventoryTotal = $('#inventoryTotal');
    const expectedAmount = $('#expectedAmount');
    const differenceAmount = $('#differenceAmount');
    const discrepancySection = $('#discrepancySection');
    if (inventoryTotal) inventoryTotal.textContent = fmt(0);
    if (expectedAmount) expectedAmount.value = '';
    if (differenceAmount) differenceAmount.textContent = fmt(0);
    if (discrepancySection) discrepancySection.classList.add('hidden');
    localStorage.removeItem('inventoryTotal');
    alert(T('reset_inv'));
  });

  addResetButton('formulas', () => {
    const wholesaleForm = $('#wholesaleForm');
    const wholesaleResultWrapper = $('#wholesaleResultWrapper');
    if (wholesaleForm) wholesaleForm.reset();
    if (wholesaleResultWrapper) wholesaleResultWrapper.classList.add('hidden');
    const conversionForm = $('#conversionForm');
    const conversionResultWrapper = $('#conversionResultWrapper');
    if (conversionForm) conversionForm.reset();
    if (conversionResultWrapper) conversionResultWrapper.classList.add('hidden');
    alert(T('reset_formulas'));
  });

  addResetButton('roi', () => {
    const roiForm = $('#roiForm');
    const roiResults = $('#roiResults');
    if (roiForm) roiForm.reset();
    if (roiResults) roiResults.classList.add('hidden');
    alert(T('reset_roi'));
  });

  addResetButton('shift', () => {
    const shiftForm = $('#shiftForm');
    const shiftResults = $('#shiftResults');
    if (shiftForm) shiftForm.reset();
    if (shiftResults) shiftResults.classList.add('hidden');
    ['#cashBox','#cashSales','#otherIncome','#expenses','#discounts','#visaPayments'].forEach(id => {
      const el = $(id); if (el) el.value = '0';
    });
    localStorage.removeItem('shiftReport');
    alert(T('reset_shift'));
  });
});
