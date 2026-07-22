// inventory.js - Cash inventory logic (bilingual)

document.addEventListener('DOMContentLoaded', () => {
  const $ = window.$;
  const $$ = window.$$;
  const T = (k) => (window.t ? window.t(k) : k);
  const fmt = (n) => (window.formatCurrency ? window.formatCurrency(n) : String(n));

  const denominations = [200, 100, 50, 20, 10, 5];
  const denominationContainer = $('#denominationContainer');
  if (!denominationContainer) return;
  denominationContainer.innerHTML = denominations.map(d => `<div class="flex items-center gap-3"><span class="font-bold text-lg w-10 text-center text-gray-500">${d}</span><input type="number" class="denomination-input input-field text-center" data-value="${d}" placeholder="0" min="0"></div>`).join('');

  function calculateInventoryTotal() {
    let total = Array.from($$('.denomination-input')).reduce((sum, input) => sum + (parseInt(input.value) || 0) * parseInt(input.dataset.value), 0);
    $('#inventoryTotal').textContent = fmt(total);
    localStorage.setItem('inventoryTotal', total);
    return total;
  }
  function renderDifference() {
    const diffEl = $('#differenceAmount');
    if (!diffEl) return;
    const total = calculateInventoryTotal();
    const expected = parseFloat($('#expectedAmount')?.value) || 0;
    const difference = total - expected;
    diffEl.textContent = fmt(difference);
    diffEl.className = 'font-bold';
    diffEl.classList.add(difference === 0 ? 'text-gray-500' : (difference > 0 ? 'text-green-500' : 'text-primary'));
  }

  denominationContainer.addEventListener('input', () => {
    calculateInventoryTotal();
    const expEl = $('#expectedAmount');
    if (expEl && expEl.value !== '') renderDifference();
  });
  $('#inventoryNo')?.addEventListener('click', () => $('#discrepancySection').classList.remove('hidden'));
  $('#inventoryYes')?.addEventListener('click', () => { alert(T('inv_confirmed')); $('#discrepancySection').classList.add('hidden'); });
  $('#expectedAmount')?.addEventListener('input', renderDifference);

  // Initial totals (saved value or zero), rendered in the active language.
  let initial = 0;
  try { initial = parseFloat(localStorage.getItem('inventoryTotal')) || 0; } catch (e) {}
  $('#inventoryTotal').textContent = fmt(initial);
  const diffInit = $('#differenceAmount');
  if (diffInit) diffInit.textContent = fmt(0);

  // Re-render currency strings on language change.
  document.addEventListener('languagechange', () => {
    $('#inventoryTotal').textContent = fmt(parseFloat(localStorage.getItem('inventoryTotal')) || 0);
    const diffEl = $('#differenceAmount');
    if (!diffEl) return;
    const expEl = $('#expectedAmount');
    if (!$('#discrepancySection').classList.contains('hidden') && expEl && expEl.value !== '') renderDifference();
    else diffEl.textContent = fmt(0);
  });
});
