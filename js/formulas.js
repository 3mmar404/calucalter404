// formulas.js - Wholesale & conversion formulas

document.addEventListener('DOMContentLoaded', () => {
  const $ = window.$;
  $('#wholesaleForm')?.addEventListener('submit', e => {
    e.preventDefault();
    const price = parseFloat($('#piecePrice').value);
    const discount = parseFloat($('#discountPercent').value) || 0;
    if (price <= 0) return alert('يجب إدخال سعر صحيح للقطعة');
    const formatCurrency = (num) => new Intl.NumberFormat('ar-EG', { style: 'currency', currency: 'EGP', minimumFractionDigits: 0, maximumFractionDigits: 2 }).format(num);
    $('#wholesaleResult').textContent = formatCurrency((price * 10 * (1 - discount / 100)) / 12);
    $('#wholesaleResultWrapper').classList.remove('hidden');
  });
  $('#conversionForm')?.addEventListener('submit', e => {
    e.preventDefault();
    const pieces = parseInt($('#piecesInput').value), unitSize = parseInt($('#unitSize').value);
    if (pieces <= 0) return alert('يجب إدخال عدد صحيح من القطع');
    $('#conversionResult').textContent = `${(pieces / unitSize).toFixed(2)} ${unitSize === 12 ? 'دستة' : 'نص دستة'}`;
    $('#conversionResultWrapper').classList.remove('hidden');
  });
});
