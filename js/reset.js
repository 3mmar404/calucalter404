// reset.js - Reset buttons for all tabs

document.addEventListener('DOMContentLoaded', () => {
  const $ = window.$;
  const $$ = window.$$;
  
  // Helper function to add reset button to tabs
  function addResetButton(tabId, resetFn) {
    const tab = document.getElementById(tabId);
    if (!tab) return;
    
    let existing = tab.querySelector('.reset-btn');
    if (existing) return;
    
    const btn = document.createElement('button');
    btn.type = 'button';
    btn.className = 'reset-btn btn bg-red-500 hover:bg-red-600 text-white px-4 py-2 rounded-lg shadow-lg hover:shadow-xl hover:scale-105 transition-all mb-4 float-right';
    btn.innerHTML = '<i class="fas fa-rotate-left"></i> إعادة التهيئة';
    btn.onclick = resetFn;
    
    // Add to the beginning of the tab
    tab.insertBefore(btn, tab.firstChild);
    
    // Add clear div after button
    const clearDiv = document.createElement('div');
    clearDiv.className = 'clear-both mb-4';
    tab.insertBefore(clearDiv, btn.nextSibling);
  }
  
  // Add reset buttons to all tabs
  addResetButton('calculator', () => {
    const calcDisplay = $('#calcDisplay');
    const calcExpression = $('#calcExpression');
    const historyList = $('#historyList');
    
    if (calcDisplay) calcDisplay.value = '0';
    if (calcExpression) calcExpression.textContent = '';
    if (historyList) historyList.innerHTML = '<p class="text-gray-500 text-center py-4">لا توجد عمليات محفوظة</p>';
    
    localStorage.removeItem('calcHistory');
    alert('تم مسح الحاسبة والسجل!');
  });
  
  addResetButton('inventory', () => {
    $$('.denomination-input').forEach(input => input.value = '');
    const inventoryTotal = $('#inventoryTotal');
    const expectedAmount = $('#expectedAmount');
    const differenceAmount = $('#differenceAmount');
    const discrepancySection = $('#discrepancySection');
    
    if (inventoryTotal) inventoryTotal.textContent = '0 جنيه';
    if (expectedAmount) expectedAmount.value = '';
    if (differenceAmount) differenceAmount.textContent = '0 جنيه';
    if (discrepancySection) discrepancySection.classList.add('hidden');
    
    localStorage.removeItem('inventoryTotal');
    alert('تم مسح جرد الكاش!');
  });
  
  addResetButton('formulas', () => {
    // Reset wholesale form
    const wholesaleForm = $('#wholesaleForm');
    const wholesaleResultWrapper = $('#wholesaleResultWrapper');
    if (wholesaleForm) wholesaleForm.reset();
    if (wholesaleResultWrapper) wholesaleResultWrapper.classList.add('hidden');
    
    // Reset conversion form
    const conversionForm = $('#conversionForm');
    const conversionResultWrapper = $('#conversionResultWrapper');
    if (conversionForm) conversionForm.reset();
    if (conversionResultWrapper) conversionResultWrapper.classList.add('hidden');
    
    alert('تم مسح جميع المعادلات!');
  });
  
  addResetButton('roi', () => {
    const roiForm = $('#roiForm');
    const roiResults = $('#roiResults');
    if (roiForm) roiForm.reset();
    if (roiResults) roiResults.classList.add('hidden');
    
    alert('تم مسح حاسبة ROI!');
  });
  
  addResetButton('shift', () => {
    const shiftForm = $('#shiftForm');
    const shiftResults = $('#shiftResults');
    if (shiftForm) shiftForm.reset();
    if (shiftResults) shiftResults.classList.add('hidden');
    
    // Reset all shift inputs to 0
    ['#cashBox','#cashSales','#otherIncome','#expenses','#discounts','#visaPayments'].forEach(id => {
      const el = $(id);
      if (el) el.value = '0';
    });
    
    localStorage.removeItem('shiftReport');
    alert('تم مسح بيانات الوردية!');
  });
});