// inventory.js - Cash inventory logic

document.addEventListener('DOMContentLoaded', () => {
  const $ = window.$;
  const $$ = window.$$;
  const denominations = [200, 100, 50, 20, 10, 5];
  const denominationContainer = $('#denominationContainer');
  if (!denominationContainer) return;
  denominationContainer.innerHTML = denominations.map(d => `<div class="flex items-center gap-3"><span class="font-bold text-lg w-10 text-center text-gray-500">${d}</span><input type="number" class="denomination-input input-field text-center" data-value="${d}" placeholder="0" min="0"></div>`).join('');
  function formatCurrency(num) {
    return new Intl.NumberFormat('ar-EG', { style: 'currency', currency: 'EGP', minimumFractionDigits: 0, maximumFractionDigits: 2 }).format(num);
  }
  function calculateInventoryTotal() {
    let total = Array.from($$('.denomination-input')).reduce((sum, input) => sum + (parseInt(input.value) || 0) * parseInt(input.dataset.value), 0);
    $('#inventoryTotal').textContent = formatCurrency(total);
    localStorage.setItem('inventoryTotal', total);
    return total;
  }
  denominationContainer.addEventListener('input', calculateInventoryTotal);
  $('#inventoryNo')?.addEventListener('click', () => $('#discrepancySection').classList.remove('hidden'));
  $('#inventoryYes')?.addEventListener('click', () => { alert('رائع! تم تأكيد الجرد.'); $('#discrepancySection').classList.add('hidden'); });
  $('#expectedAmount')?.addEventListener('input', e => {
    const total = calculateInventoryTotal();
    const expected = parseFloat(e.target.value) || 0;
    const difference = total - expected;
    const diffEl = $('#differenceAmount');
    diffEl.textContent = formatCurrency(difference);
    diffEl.className = 'font-bold';
    diffEl.classList.add(difference === 0 ? 'text-gray-500' : (difference > 0 ? 'text-green-500' : 'text-primary'));
  });
  // Reset button logic can be handled in core.js if needed
  if(localStorage.getItem('inventoryTotal')) {
    try {
      const savedTotal = parseFloat(localStorage.getItem('inventoryTotal')) || 0;
      $('#inventoryTotal').textContent = formatCurrency(savedTotal);
    } catch (error) {
      console.error('خطأ في استرجاع إجمالي الجرد:', error);
    }
  }
});
