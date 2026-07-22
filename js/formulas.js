// formulas.js - Wholesale & conversion formulas (bilingual)

document.addEventListener('DOMContentLoaded', () => {
  const $ = window.$;
  const T = (k) => (window.t ? window.t(k) : k);
  const fmt = (n) => (window.formatCurrency ? window.formatCurrency(n) : String(n));

  let lastWholesale = null;   // { price, discount }
  let lastConversion = null;  // { pieces, unitSize }

  function renderWholesale() {
    if (!lastWholesale) return;
    const { price, discount } = lastWholesale;
    $('#wholesaleResult').textContent = fmt((price * 10 * (1 - discount / 100)) / 12);
    $('#wholesaleResultWrapper').classList.remove('hidden');
  }
  function renderConversion() {
    if (!lastConversion) return;
    const { pieces, unitSize } = lastConversion;
    const unitWord = unitSize === 12 ? T('unit_dozen_short') : T('unit_half_dozen_short');
    $('#conversionResult').textContent = `${(pieces / unitSize).toFixed(2)} ${unitWord}`;
    $('#conversionResultWrapper').classList.remove('hidden');
  }

  $('#wholesaleForm')?.addEventListener('submit', e => {
    e.preventDefault();
    const price = parseFloat($('#piecePrice').value);
    const discount = parseFloat($('#discountPercent').value) || 0;
    if (!(price > 0)) return alert(T('err_valid_piece_price'));
    lastWholesale = { price, discount };
    renderWholesale();
  });
  $('#conversionForm')?.addEventListener('submit', e => {
    e.preventDefault();
    const pieces = parseInt($('#piecesInput').value), unitSize = parseInt($('#unitSize').value);
    if (!(pieces > 0)) return alert(T('err_valid_pieces'));
    lastConversion = { pieces, unitSize };
    renderConversion();
  });

  document.addEventListener('languagechange', () => {
    if (lastWholesale && !$('#wholesaleResultWrapper').classList.contains('hidden')) renderWholesale();
    if (lastConversion && !$('#conversionResultWrapper').classList.contains('hidden')) renderConversion();
  });
});
