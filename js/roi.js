// roi.js - Marketing ROI logic (bilingual)

document.addEventListener('DOMContentLoaded', () => {
  const $ = window.$;
  const T = (k) => (window.t ? window.t(k) : k);
  const fmt = (n) => (window.formatCurrency ? window.formatCurrency(n) : String(n));

  let last = null; // { campaignCost, sellingPrice, costPrice }

  function render() {
    if (!last) return;
    const { campaignCost, sellingPrice, costPrice } = last;
    const profitPerPiece = sellingPrice - costPrice;
    const profitMarginRatio = profitPerPiece / sellingPrice;
    $('#requiredSales').textContent = fmt(campaignCost / profitMarginRatio);
    $('#requiredPieces').textContent = `${Math.ceil((campaignCost / profitMarginRatio) / sellingPrice)} ${T('piece_unit')}`;
    $('#profitMargin').textContent = `${fmt(profitPerPiece)} (${(profitMarginRatio * 100).toFixed(1)}%)`;
    $('#roiResults').classList.remove('hidden');
  }

  $('#roiForm')?.addEventListener('submit', e => {
    e.preventDefault();
    const campaignCost = parseFloat($('#campaignCost').value),
          sellingPrice = parseFloat($('#sellingPrice').value),
          costPrice = parseFloat($('#costPrice').value);
    if (!(campaignCost > 0)) return alert(T('err_valid_campaign'));
    if (!(sellingPrice > 0)) return alert(T('err_valid_selling'));
    if (!(costPrice > 0)) return alert(T('err_valid_cost'));
    if (sellingPrice <= costPrice) return alert(T('err_selling_gt_cost'));
    last = { campaignCost, sellingPrice, costPrice };
    render();
  });

  document.addEventListener('languagechange', () => {
    if (last && !$('#roiResults').classList.contains('hidden')) render();
  });
});
