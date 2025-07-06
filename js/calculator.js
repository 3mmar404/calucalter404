// calculator.js - Calculator logic

document.addEventListener('DOMContentLoaded', () => {
  const $ = window.$;
  const $$ = window.$$;
  const calcDisplay = document.getElementById('calcDisplay');
  const calcExpression = document.getElementById('calcExpression');
  const historyList = document.getElementById('historyList');
  let calcHistory = JSON.parse(localStorage.getItem('calcHistory')) || [];

  function formatCurrency(num) {
    return new Intl.NumberFormat('ar-EG', { style: 'currency', currency: 'EGP', minimumFractionDigits: 0, maximumFractionDigits: 2 }).format(num);
  }
  function showErrorState() {
    if (calcDisplay) {
      calcDisplay.classList.add('text-primary', 'bg-red-500/10');
    }
  }
  function clearErrorState() {
    if (calcDisplay) {
      calcDisplay.classList.remove('text-primary', 'bg-red-500/10');
    }
  }
  function updateCalcHistoryList() {
    if (historyList) {
      historyList.innerHTML = calcHistory.length > 0 ? calcHistory.slice().reverse().map(item => `
        <div class="p-2 rounded-md bg-gray-100 dark:bg-gray-700/50 hover:bg-gray-200 dark:hover:bg-gray-700 cursor-pointer" onclick="populateDisplayFromResult('${item.result}')">
          <div class="text-gray-500 dark:text-gray-400 text-xs font-mono truncate text-right">${item.expr} =</div>
          <div class="font-bold text-lg font-mono text-right">${item.result}</div>
        </div>`).join('') : '<p class="text-gray-500 text-center py-4">لا توجد عمليات محفوظة</p>';
    }
  }
  function handleCalcInput(input) {
    if (!calcDisplay) return;
    clearErrorState();
    if (input === 'C') {
      calcDisplay.value = '0';
      if (calcExpression) calcExpression.textContent = '';
    } else if (input === 'backspace') {
      calcDisplay.value = calcDisplay.value.length > 1 ? calcDisplay.value.slice(0, -1) : '0';
    } else if (input === '=') {
      if (calcDisplay.value === 'خطأ') return;
      const expr = calcDisplay.value.replace(/([0-9])%/g, "($1/100)");
      try {
        if (/[+\-*/.]{2,}/.test(expr)) throw "Invalid format";
        const result = new Function(`return ${expr}`)();
        if (isNaN(result) || !isFinite(result)) throw "Invalid result";
        if (calcExpression) calcExpression.textContent = `${calcDisplay.value} =`;
        calcDisplay.value = parseFloat(result.toPrecision(12));
        calcHistory.push({ expr: calcExpression ? calcExpression.textContent.replace(' =', '') : calcDisplay.value, result: calcDisplay.value });
        if (calcHistory.length > 20) calcHistory.shift();
        localStorage.setItem('calcHistory', JSON.stringify(calcHistory));
        updateCalcHistoryList();
      } catch (error) {
        showErrorState();
        calcDisplay.value = 'خطأ';
      }
    } else {
      if (calcDisplay.value === '0' || calcDisplay.value === 'خطأ') calcDisplay.value = '';
      calcDisplay.value += input;
    }
  }
  const calcButtons = document.getElementById('calcButtons');
  if (calcButtons) {
    calcButtons.addEventListener('click', e => {
      const button = e.target.closest('.btn-calc');
      if (!button) return;
      handleCalcInput(button.dataset.value || button.dataset.op);
    });
  }
  
  document.addEventListener('keydown', (e) => {
    const calculatorTab = document.getElementById('calculator');
    if (!calculatorTab?.classList.contains('active')) return;
    const keyMap = { 'Enter': '=', 'Backspace': 'backspace', 'Delete': 'C', 'Escape': 'C' };
    if ('0123456789.+-*/%'.includes(e.key) || e.key in keyMap) {
      e.preventDefault();
      handleCalcInput(keyMap[e.key] || e.key);
    }
  });
  
  const clearHistoryBtn = document.getElementById('clearHistoryBtn');
  if (clearHistoryBtn) {
    clearHistoryBtn.addEventListener('click', () => {
      calcHistory = [];
      localStorage.removeItem('calcHistory');
      updateCalcHistoryList();
    });
  }
  
  window.populateDisplayFromResult = (result) => {
    if (calcDisplay) {
      calcDisplay.value = result;
      clearErrorState();
    }
  };
  
  // Initialize
  setTimeout(() => {
    updateCalcHistoryList();
  }, 100);
});
