// shift.js - Shift closing logic (bilingual)

document.addEventListener('DOMContentLoaded', () => {
  const $ = window.$;
  const T = (k) => (window.t ? window.t(k) : k);
  const formatCurrency = (num) => (window.formatCurrency
    ? window.formatCurrency(num, { minimumFractionDigits: 2 })
    : (Number(num || 0).toFixed(2) + ' EGP'));

  let lastShift = null; // stored computed values so we can re-render on language change

  function renderShiftReport(d) {
    const resultsContainer = $('#shiftResults');
    if (!resultsContainer) return;
    resultsContainer.classList.remove('hidden');

    const netRevenueColor = d.netRevenue >= 0 ? 'text-green-600' : 'text-red-600';
    const netRevenueBg = d.netRevenue >= 0 ? 'bg-green-50 dark:bg-green-900/20' : 'bg-red-50 dark:bg-red-900/20';

    resultsContainer.innerHTML = `
      <div class="space-y-4">
        <h3 class="font-bold text-xl mb-4 text-center">${T('shift_results_title')}</h3>

        <div class="bg-green-50 dark:bg-green-900/20 p-4 rounded-lg">
          <h4 class="font-bold text-green-600 dark:text-green-400 mb-2">${T('revenue_title')}</h4>
          <div class="space-y-2 text-sm">
            <div class="flex justify-between"><span>${T('cash_box_start')}</span><span class="font-mono">${formatCurrency(d.cashBox)}</span></div>
            <div class="flex justify-between"><span>${T('cash_sales_label')}</span><span class="font-mono">${formatCurrency(d.cashSales)}</span></div>
            <div class="flex justify-between"><span>${T('other_income_label')}</span><span class="font-mono">${formatCurrency(d.otherIncome)}</span></div>
            <div class="flex justify-between border-t pt-2 font-bold"><span>${T('total_revenue')}</span><span class="font-mono">${formatCurrency(d.totalRevenue)}</span></div>
          </div>
        </div>

        <div class="bg-red-50 dark:bg-red-900/20 p-4 rounded-lg">
          <h4 class="font-bold text-red-600 dark:text-red-400 mb-2">${T('expenses_title')}</h4>
          <div class="space-y-2 text-sm">
            <div class="flex justify-between"><span>${T('expenses_label')}</span><span class="font-mono">${formatCurrency(d.expenses)}</span></div>
            <div class="flex justify-between"><span>${T('discounts_label')}</span><span class="font-mono">${formatCurrency(d.discounts)}</span></div>
            <div class="flex justify-between"><span>${T('visa_label')}</span><span class="font-mono">${formatCurrency(d.visaPayments)}</span></div>
            <div class="flex justify-between border-t pt-2 font-bold"><span>${T('total_expenses')}</span><span class="font-mono">${formatCurrency(d.totalExpenses)}</span></div>
          </div>
        </div>

        <div class="${netRevenueBg} p-4 rounded-lg">
          <div class="flex justify-between items-center"><span class="font-bold text-lg">${T('net_shift')}</span><span class="font-bold text-2xl font-mono ${netRevenueColor}">${formatCurrency(d.netRevenue)}</span></div>
        </div>

        <div class="bg-blue-50 dark:bg-blue-900/20 p-4 rounded-lg">
          <div class="flex justify-between items-center"><span class="font-bold">${T('carried_over')}</span><span class="font-bold text-xl font-mono text-blue-600">${formatCurrency(d.carriedOver)}</span></div>
        </div>

        <div class="bg-yellow-50 dark:bg-yellow-900/20 p-4 rounded-lg">
          <div class="flex justify-between items-center"><span class="font-bold">${T('cash_box_left')}</span><span class="font-bold text-xl font-mono text-yellow-600">${formatCurrency(d.cashBoxLeft)}</span></div>
        </div>

        ${d.carryMsgKey ? `<div class="p-3 bg-gray-100 dark:bg-gray-700 rounded-lg text-center font-semibold text-gray-600 dark:text-gray-300">${T(d.carryMsgKey)}</div>` : ''}

        <div class="flex gap-3 justify-center mt-6 flex-wrap">
          <button type="button" id="printShiftBtn" class="btn bg-primary text-white px-6 py-3 rounded-lg hover:bg-blue-600 transition-all"><i class="fas fa-print mr-2"></i>${T('print_report')}</button>
          <button type="button" id="saveShiftBtn" class="btn bg-green-500 text-white px-6 py-3 rounded-lg hover:bg-green-600 transition-all"><i class="fas fa-save mr-2"></i>${T('save_report')}</button>
          <button type="button" id="clearShiftBtn" class="btn bg-red-500 text-white px-6 py-3 rounded-lg hover:bg-red-600 transition-all"><i class="fas fa-trash mr-2"></i>${T('clear_data')}</button>
        </div>
      </div>`;

    setTimeout(() => {
      $('#printShiftBtn')?.addEventListener('click', () => window.print());
      $('#saveShiftBtn')?.addEventListener('click', () => {
        const dataStr = JSON.stringify(d.persist, null, 2);
        const blob = new Blob([dataStr], { type: 'application/json' });
        const url = URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = url;
        const stamp = new Date().toLocaleDateString(window.currentLang === 'en' ? 'en-GB' : 'ar-EG').replace(/\//g, '-');
        link.download = `${T('report_filename')}_${stamp}.json`;
        link.click();
        URL.revokeObjectURL(url);
      });
      $('#clearShiftBtn')?.addEventListener('click', () => {
        if (confirm(T('confirm_clear'))) {
          $('#shiftForm').reset();
          $('#shiftResults').classList.add('hidden');
          localStorage.removeItem('shiftReport');
          lastShift = null;
        }
      });
    }, 100);
  }

  function compute() {
    const getVal = (id) => {
      const el = $(id);
      if (!el) return 0;
      const v = parseFloat(el.value) || 0;
      return v < 0 ? 0 : v;
    };
    const cashBox = getVal('#cashBox'), cashSales = getVal('#cashSales'), otherIncome = getVal('#otherIncome');
    const totalRevenue = cashBox + cashSales + otherIncome;
    const expenses = getVal('#expenses'), discounts = getVal('#discounts'), visaPayments = getVal('#visaPayments');
    const totalExpenses = expenses + discounts + visaPayments;
    const netRevenue = totalRevenue - totalExpenses;

    let carriedOver = 0, cashBoxLeft = 0, carryMsgKey = '';
    if (netRevenue >= 100) {
      carriedOver = Math.floor(netRevenue / 100) * 100;
      cashBoxLeft = netRevenue - carriedOver;
    } else if (netRevenue > 0) {
      cashBoxLeft = netRevenue;
      carryMsgKey = 'msg_below_100';
    } else {
      cashBoxLeft = netRevenue;
      carryMsgKey = netRevenue < 0 ? 'msg_deficit' : 'msg_nothing_carry';
    }

    const d = { cashBox, cashSales, otherIncome, totalRevenue, expenses, discounts, visaPayments, totalExpenses, netRevenue, carriedOver, cashBoxLeft, carryMsgKey };
    d.persist = {
      timestamp: new Date().toLocaleString(window.currentLang === 'en' ? 'en-GB' : 'ar-EG'),
      inputs: { cashBox, cashSales, otherIncome, expenses, discounts, visaPayments },
      results: { totalRevenue, totalExpenses, netRevenue, carriedOver, cashBoxLeft }
    };
    return d;
  }

  $('#shiftForm')?.addEventListener('submit', e => {
    e.preventDefault();
    lastShift = compute();
    localStorage.setItem('shiftReport', JSON.stringify(lastShift.persist));
    renderShiftReport(lastShift);
  });

  document.addEventListener('languagechange', () => {
    if (lastShift && !$('#shiftResults').classList.contains('hidden')) renderShiftReport(lastShift);
  });

  // Restore last saved inputs on load.
  const savedReport = localStorage.getItem('shiftReport');
  if (savedReport) {
    try {
      const data = JSON.parse(savedReport);
      if (data.inputs) {
        const i = data.inputs;
        $('#cashBox').value = i.cashBox || 0;
        $('#cashSales').value = i.cashSales || 0;
        $('#otherIncome').value = i.otherIncome || 0;
        $('#expenses').value = i.expenses || 0;
        $('#discounts').value = i.discounts || 0;
        $('#visaPayments').value = i.visaPayments || 0;
      }
    } catch (error) {
      localStorage.removeItem('shiftReport');
    }
  }
});
