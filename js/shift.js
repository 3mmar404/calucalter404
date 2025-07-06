// shift.js - Shift closing logic

document.addEventListener('DOMContentLoaded', () => {
  const $ = window.$;
  
  // دالة تنسيق العملة
  const formatCurrency = (num) => {
    if (isNaN(num) || num === null || num === undefined) return '0.00 ج.م';
    return new Intl.NumberFormat('ar-EG', { 
      style: 'currency', 
      currency: 'EGP', 
      minimumFractionDigits: 2, 
      maximumFractionDigits: 2 
    }).format(num);
  };

  // معالج إرسال النموذج
  $('#shiftForm')?.addEventListener('submit', e => {
    e.preventDefault();
    
    // دالة للحصول على القيم مع التحقق من صحتها
    const getVal = (id) => {
      const element = $(id);
      if (!element) return 0;
      const value = parseFloat(element.value) || 0;
      return value < 0 ? 0 : value; // تجنب القيم السالبة
    };
    
    // حساب الإيرادات
    const cashBox = getVal('#cashBox');
    const cashSales = getVal('#cashSales');
    const otherIncome = getVal('#otherIncome');
    const totalRevenue = cashBox + cashSales + otherIncome;
    
    // حساب المصروفات
    const expenses = getVal('#expenses');
    const discounts = getVal('#discounts');
    const visaPayments = getVal('#visaPayments');
    const totalExpenses = expenses + discounts + visaPayments;
    
    // حساب صافي الوردية
    const netRevenue = totalRevenue - totalExpenses;
    
    // حساب المبلغ المرحل والمتبقي للدرج
    let carriedOver = 0;
    let cashBoxLeft = 0;
    let carryMsg = '';
    
    if (netRevenue >= 100) {
      // ترحيل المئات الكاملة
      carriedOver = Math.floor(netRevenue / 100) * 100;
      cashBoxLeft = netRevenue - carriedOver;
    } else if (netRevenue > 0) {
      // إذا كان المبلغ أقل من 100 ولكن موجب
      carriedOver = 0;
      cashBoxLeft = netRevenue;
      carryMsg = 'المبلغ أقل من 100 جنيه، سيتم تركه كحصالة فقط.';
    } else {
      // إذا كان المبلغ سالب أو صفر
      carriedOver = 0;
      cashBoxLeft = netRevenue;
      carryMsg = netRevenue < 0 ? 'يوجد عجز في الوردية!' : 'لا توجد أموال للترحيل.';
    }
    
    // إنشاء تقرير النتائج
    const resultsContainer = $('#shiftResults');
    if (resultsContainer) {
      resultsContainer.classList.remove('hidden');
      
      // تحديد لون صافي الوردية
      const netRevenueColor = netRevenue >= 0 ? 'text-green-600' : 'text-red-600';
      const netRevenueBg = netRevenue >= 0 ? 'bg-green-50 dark:bg-green-900/20' : 'bg-red-50 dark:bg-red-900/20';
      
      resultsContainer.innerHTML = `
        <div class="space-y-4">
          <h3 class="font-bold text-xl mb-4 text-center">نتائج الوردية</h3>
          
          <!-- تفاصيل الإيرادات -->
          <div class="bg-green-50 dark:bg-green-900/20 p-4 rounded-lg">
            <h4 class="font-bold text-green-600 dark:text-green-400 mb-2">الإيرادات</h4>
            <div class="space-y-2 text-sm">
              <div class="flex justify-between">
                <span>الحصالة في البداية:</span>
                <span class="font-mono">${formatCurrency(cashBox)}</span>
              </div>
              <div class="flex justify-between">
                <span>مبيعات كاش:</span>
                <span class="font-mono">${formatCurrency(cashSales)}</span>
              </div>
              <div class="flex justify-between">
                <span>إيرادات أخرى:</span>
                <span class="font-mono">${formatCurrency(otherIncome)}</span>
              </div>
              <div class="flex justify-between border-t pt-2 font-bold">
                <span>إجمالي الإيرادات:</span>
                <span class="font-mono">${formatCurrency(totalRevenue)}</span>
              </div>
            </div>
          </div>
          
          <!-- تفاصيل المصروفات -->
          <div class="bg-red-50 dark:bg-red-900/20 p-4 rounded-lg">
            <h4 class="font-bold text-red-600 dark:text-red-400 mb-2">المصروفات</h4>
            <div class="space-y-2 text-sm">
              <div class="flex justify-between">
                <span>مصروفات:</span>
                <span class="font-mono">${formatCurrency(expenses)}</span>
              </div>
              <div class="flex justify-between">
                <span>خصومات:</span>
                <span class="font-mono">${formatCurrency(discounts)}</span>
              </div>
              <div class="flex justify-between">
                <span>مدفوعات فيزا:</span>
                <span class="font-mono">${formatCurrency(visaPayments)}</span>
              </div>
              <div class="flex justify-between border-t pt-2 font-bold">
                <span>إجمالي المصروفات:</span>
                <span class="font-mono">${formatCurrency(totalExpenses)}</span>
              </div>
            </div>
          </div>
          
          <!-- صافي الوردية -->
          <div class="${netRevenueBg} p-4 rounded-lg">
            <div class="flex justify-between items-center">
              <span class="font-bold text-lg">صافي الوردية:</span>
              <span class="font-bold text-2xl font-mono ${netRevenueColor}">${formatCurrency(netRevenue)}</span>
            </div>
          </div>
          
          <!-- المبلغ المرحل -->
          <div class="bg-blue-50 dark:bg-blue-900/20 p-4 rounded-lg">
            <div class="flex justify-between items-center">
              <span class="font-bold">المبلغ المرحل لليوم التالي:</span>
              <span class="font-bold text-xl font-mono text-blue-600">${formatCurrency(carriedOver)}</span>
            </div>
          </div>
          
          <!-- المتبقي للدرج -->
          <div class="bg-yellow-50 dark:bg-yellow-900/20 p-4 rounded-lg">
            <div class="flex justify-between items-center">
              <span class="font-bold">المتبقي للدرج (حصالة):</span>
              <span class="font-bold text-xl font-mono text-yellow-600">${formatCurrency(cashBoxLeft)}</span>
            </div>
          </div>
          
          <!-- رسالة إضافية -->
          ${carryMsg ? `<div class="p-3 bg-gray-100 dark:bg-gray-700 rounded-lg text-center font-semibold text-gray-600 dark:text-gray-300">${carryMsg}</div>` : ''}
          
          <!-- أزرار الإجراءات -->
          <div class="flex gap-3 justify-center mt-6">
            <button type="button" id="printShiftBtn" class="btn bg-primary text-white px-6 py-3 rounded-lg hover:bg-blue-600 transition-all">
              <i class="fas fa-print mr-2"></i>طباعة التقرير
            </button>
            <button type="button" id="saveShiftBtn" class="btn bg-green-500 text-white px-6 py-3 rounded-lg hover:bg-green-600 transition-all">
              <i class="fas fa-save mr-2"></i>حفظ التقرير
            </button>
            <button type="button" id="clearShiftBtn" class="btn bg-red-500 text-white px-6 py-3 rounded-lg hover:bg-red-600 transition-all">
              <i class="fas fa-trash mr-2"></i>مسح البيانات
            </button>
          </div>
        </div>
      `;
      
      // حفظ البيانات في localStorage
      const shiftData = {
        timestamp: new Date().toLocaleString('ar-EG'),
        inputs: { cashBox, cashSales, otherIncome, expenses, discounts, visaPayments },
        results: { totalRevenue, totalExpenses, netRevenue, carriedOver, cashBoxLeft },
        message: carryMsg
      };
      
      localStorage.setItem('shiftReport', JSON.stringify(shiftData));
      
      // إضافة أحداث الأزرار
      setTimeout(() => {
        // زر الطباعة
        $('#printShiftBtn')?.addEventListener('click', () => {
          window.print();
        });
        
        // زر الحفظ
        $('#saveShiftBtn')?.addEventListener('click', () => {
          const dataStr = JSON.stringify(shiftData, null, 2);
          const dataBlob = new Blob([dataStr], { type: 'application/json' });
          const url = URL.createObjectURL(dataBlob);
          const link = document.createElement('a');
          link.href = url;
          link.download = `تقرير_الوردية_${new Date().toLocaleDateString('ar-EG').replace(/\//g, '-')}.json`;
          link.click();
          URL.revokeObjectURL(url);
        });
        
        // زر المسح
        $('#clearShiftBtn')?.addEventListener('click', () => {
          if (confirm('هل أنت متأكد من مسح جميع البيانات؟')) {
            $('#shiftForm').reset();
            resultsContainer.classList.add('hidden');
            localStorage.removeItem('shiftReport');
          }
        });
      }, 100);
    }
  });
  
  // استرجاع آخر تقرير محفوظ عند تحميل الصفحة
  const savedReport = localStorage.getItem('shiftReport');
  if (savedReport) {
    try {
      const data = JSON.parse(savedReport);
      if (data.inputs) {
        // استرجاع القيم المدخلة
        const inputs = data.inputs;
        $('#cashBox').value = inputs.cashBox || 0;
        $('#cashSales').value = inputs.cashSales || 0;
        $('#otherIncome').value = inputs.otherIncome || 0;
        $('#expenses').value = inputs.expenses || 0;
        $('#discounts').value = inputs.discounts || 0;
        $('#visaPayments').value = inputs.visaPayments || 0;
      }
    } catch (error) {
      console.error('خطأ في استرجاع بيانات الوردية:', error);
      localStorage.removeItem('shiftReport');
    }
  }
});
