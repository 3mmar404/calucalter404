// roi.js - Marketing ROI logic

document.addEventListener('DOMContentLoaded', () => {
  const $ = window.$;
  $('#roiForm')?.addEventListener('submit', e => {
    e.preventDefault();
    const campaignCost = parseFloat($('#campaignCost').value), sellingPrice = parseFloat($('#sellingPrice').value), costPrice = parseFloat($('#costPrice').value);
    if(campaignCost <= 0) return alert('يجب إدخال تكلفة صحيحة للحملة');
    if(sellingPrice <= 0) return alert('يجب إدخال سعر بيع صحيح');
    if(costPrice <= 0) return alert('يجب إدخال تكلفة صحيحة للقطعة');
    if(sellingPrice <= costPrice) return alert('سعر البيع يجب أن يكون أعلى من التكلفة.');
    const profitPerPiece = sellingPrice - costPrice, profitMarginRatio = profitPerPiece / sellingPrice;
    const formatCurrency = (num) => new Intl.NumberFormat('ar-EG', { style: 'currency', currency: 'EGP', minimumFractionDigits: 0, maximumFractionDigits: 2 }).format(num);
    $('#requiredSales').textContent = formatCurrency(campaignCost / profitMarginRatio);
    $('#requiredPieces').textContent = `${Math.ceil((campaignCost / profitMarginRatio) / sellingPrice)} قطعة`;
    $('#profitMargin').textContent = `${formatCurrency(profitPerPiece)} (${(profitMarginRatio * 100).toFixed(1)}%)`;
    $('#roiResults').classList.remove('hidden');
  });
});
