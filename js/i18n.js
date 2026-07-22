// i18n.js — Bilingual (Arabic / English) internationalization layer for SmartCalc Pro
// Exposes: window.t(key), window.formatCurrency(num, opts), window.setLanguage(lang),
//          window.currentLang, and dispatches a `languagechange` event on toggle.
(function () {
  const translations = {
    ar: {
      // meta
      doc_title: "SmartCalc Pro — حاسبة الأعمال الذكية",
      app_name: "SmartCalc Pro",
      app_tagline: "حاسبة الأعمال الذكية",
      lang_switch_label: "EN",
      // tabs
      tab_calculator: "الحاسبة",
      tab_inventory: "جرد الكاش",
      tab_formulas: "المعادلات",
      tab_roi: "ROI التسويق",
      tab_shift: "تقفيل الوردية",
      // calculator
      calc_title: "الحاسبة",
      btn_clear: "مسح",
      history_title: "السجل",
      clear_history: "مسح السجل",
      no_history: "لا توجد عمليات محفوظة",
      calc_error: "خطأ",
      // inventory
      inv_title: "جرد الكاش",
      inv_total_label: "الإجمالي:",
      inv_is_correct: "هل الجرد صحيح؟",
      yes: "نعم",
      no: "لا",
      discrepancy_title: "فحص الفرق",
      expected_amount_label: "المبلغ المتوقع:",
      expected_amount_ph: "أدخل المبلغ المتوقع",
      difference_label: "الفرق:",
      inv_confirmed: "رائع! تم تأكيد الجرد.",
      // formulas
      wholesale_title: "حاسبة الجملة",
      piece_price_label: "سعر القطعة:",
      piece_price_ph: "أدخل سعر القطعة",
      discount_label: "نسبة الخصم (%):",
      discount_ph: "أدخل نسبة الخصم",
      calc_wholesale_btn: "احسب سعر الجملة",
      wholesale_result_label: "سعر الجملة:",
      converter_title: "محول القطع",
      pieces_count_label: "عدد القطع:",
      pieces_count_ph: "أدخل عدد القطع",
      unit_label: "الوحدة:",
      unit_dozen: "دستة (12 قطعة)",
      unit_half_dozen: "نص دستة (6 قطع)",
      convert_btn: "تحويل",
      result_label: "النتيجة:",
      unit_dozen_short: "دستة",
      unit_half_dozen_short: "نص دستة",
      err_valid_piece_price: "يجب إدخال سعر صحيح للقطعة",
      err_valid_pieces: "يجب إدخال عدد صحيح من القطع",
      // roi
      roi_title: "حاسبة ROI التسويق",
      campaign_cost_label: "تكلفة الحملة الإعلانية:",
      campaign_cost_ph: "أدخل تكلفة الحملة",
      selling_price_label: "سعر البيع للقطعة:",
      selling_price_ph: "أدخل سعر البيع",
      cost_price_label: "تكلفة القطعة:",
      cost_price_ph: "أدخل تكلفة القطعة",
      calc_roi_btn: "احسب ROI",
      results_label: "النتائج:",
      required_sales_label: "المبيعات المطلوبة:",
      required_pieces_label: "عدد القطع المطلوبة:",
      profit_margin_label: "هامش الربح:",
      piece_unit: "قطعة",
      err_valid_campaign: "يجب إدخال تكلفة صحيحة للحملة",
      err_valid_selling: "يجب إدخال سعر بيع صحيح",
      err_valid_cost: "يجب إدخال تكلفة صحيحة للقطعة",
      err_selling_gt_cost: "سعر البيع يجب أن يكون أعلى من التكلفة.",
      // shift
      shift_title: "تقفيل الوردية",
      revenue_title: "الإيرادات",
      cash_box_label: "الحصالة في بداية الوردية:",
      cash_sales_label: "مبيعات كاش:",
      other_income_label: "إيرادات أخرى:",
      expenses_title: "المصروفات",
      expenses_label: "مصروفات:",
      discounts_label: "خصومات:",
      visa_label: "مدفوعات فيزا:",
      calc_results_btn: "احسب النتائج",
      shift_results_title: "نتائج الوردية",
      cash_box_start: "الحصالة في البداية:",
      total_revenue: "إجمالي الإيرادات:",
      total_expenses: "إجمالي المصروفات:",
      net_shift: "صافي الوردية:",
      carried_over: "المبلغ المُرحّل لليوم التالي:",
      cash_box_left: "المتبقي للدرج (حصالة):",
      print_report: "طباعة التقرير",
      save_report: "حفظ التقرير",
      clear_data: "مسح البيانات",
      confirm_clear: "هل أنت متأكد من مسح جميع البيانات؟",
      report_filename: "تقرير_الوردية",
      msg_below_100: "المبلغ أقل من 100 جنيه، سيتم تركه كحصالة فقط.",
      msg_deficit: "يوجد عجز في الوردية!",
      msg_nothing_carry: "لا توجد أموال للترحيل.",
      // reset
      reset_btn: "إعادة التهيئة",
      reset_calc: "تم مسح الحاسبة والسجل!",
      reset_inv: "تم مسح جرد الكاش!",
      reset_formulas: "تم مسح جميع المعادلات!",
      reset_roi: "تم مسح حاسبة ROI!",
      reset_shift: "تم مسح بيانات الوردية!",
      // footer
      footer_html: '© 2026 <span class="text-primary font-semibold">SmartCalc Pro</span> — BY AMAR'
    },
    en: {
      doc_title: "SmartCalc Pro — Smart Business Calculator",
      app_name: "SmartCalc Pro",
      app_tagline: "Smart Business Calculator",
      lang_switch_label: "ع",
      tab_calculator: "Calculator",
      tab_inventory: "Cash Count",
      tab_formulas: "Formulas",
      tab_roi: "Marketing ROI",
      tab_shift: "Shift Closeout",
      calc_title: "Calculator",
      btn_clear: "Clear",
      history_title: "History",
      clear_history: "Clear History",
      no_history: "No saved operations",
      calc_error: "Error",
      inv_title: "Cash Count",
      inv_total_label: "Total:",
      inv_is_correct: "Is the count correct?",
      yes: "Yes",
      no: "No",
      discrepancy_title: "Discrepancy Check",
      expected_amount_label: "Expected amount:",
      expected_amount_ph: "Enter expected amount",
      difference_label: "Difference:",
      inv_confirmed: "Great! Cash count confirmed.",
      wholesale_title: "Wholesale Calculator",
      piece_price_label: "Unit price:",
      piece_price_ph: "Enter unit price",
      discount_label: "Discount (%):",
      discount_ph: "Enter discount",
      calc_wholesale_btn: "Calculate Wholesale",
      wholesale_result_label: "Wholesale price:",
      converter_title: "Unit Converter",
      pieces_count_label: "Number of pieces:",
      pieces_count_ph: "Enter number of pieces",
      unit_label: "Unit:",
      unit_dozen: "Dozen (12 pieces)",
      unit_half_dozen: "Half dozen (6 pieces)",
      convert_btn: "Convert",
      result_label: "Result:",
      unit_dozen_short: "dozen",
      unit_half_dozen_short: "half dozen",
      err_valid_piece_price: "Please enter a valid unit price",
      err_valid_pieces: "Please enter a valid number of pieces",
      roi_title: "Marketing ROI Calculator",
      campaign_cost_label: "Ad campaign cost:",
      campaign_cost_ph: "Enter campaign cost",
      selling_price_label: "Selling price per unit:",
      selling_price_ph: "Enter selling price",
      cost_price_label: "Unit cost:",
      cost_price_ph: "Enter unit cost",
      calc_roi_btn: "Calculate ROI",
      results_label: "Results:",
      required_sales_label: "Required sales:",
      required_pieces_label: "Required pieces:",
      profit_margin_label: "Profit margin:",
      piece_unit: "pcs",
      err_valid_campaign: "Please enter a valid campaign cost",
      err_valid_selling: "Please enter a valid selling price",
      err_valid_cost: "Please enter a valid unit cost",
      err_selling_gt_cost: "Selling price must be higher than cost.",
      shift_title: "Shift Closeout",
      revenue_title: "Revenue",
      cash_box_label: "Opening cash float:",
      cash_sales_label: "Cash sales:",
      other_income_label: "Other income:",
      expenses_title: "Expenses",
      expenses_label: "Expenses:",
      discounts_label: "Discounts:",
      visa_label: "Visa payments:",
      calc_results_btn: "Calculate Results",
      shift_results_title: "Shift Results",
      cash_box_start: "Opening float:",
      total_revenue: "Total revenue:",
      total_expenses: "Total expenses:",
      net_shift: "Net shift:",
      carried_over: "Carried over to next day:",
      cash_box_left: "Left in drawer (float):",
      print_report: "Print Report",
      save_report: "Save Report",
      clear_data: "Clear Data",
      confirm_clear: "Are you sure you want to clear all data?",
      report_filename: "shift_report",
      msg_below_100: "Amount is less than 100 EGP; it will be left as float only.",
      msg_deficit: "There is a shortage in this shift!",
      msg_nothing_carry: "No funds to carry over.",
      reset_btn: "Reset",
      reset_calc: "Calculator and history cleared!",
      reset_inv: "Cash count cleared!",
      reset_formulas: "All formulas cleared!",
      reset_roi: "ROI calculator cleared!",
      reset_shift: "Shift data cleared!",
      footer_html: '© 2026 <span class="text-primary font-semibold">SmartCalc Pro</span> — BY AMAR'
    }
  };

  let currentLang = 'ar';
  try {
    const saved = localStorage.getItem('lang');
    if (saved === 'ar' || saved === 'en') currentLang = saved;
  } catch (e) {}

  function t(key) {
    const dict = translations[currentLang] || translations.ar;
    if (key in dict) return dict[key];
    return (translations.ar[key] != null) ? translations.ar[key] : key;
  }

  function formatCurrency(num, opts) {
    if (num === null || num === undefined || isNaN(num)) num = 0;
    const locale = currentLang === 'en' ? 'en-EG' : 'ar-EG';
    const options = Object.assign(
      { style: 'currency', currency: 'EGP', minimumFractionDigits: 0, maximumFractionDigits: 2 },
      opts || {}
    );
    try { return new Intl.NumberFormat(locale, options).format(num); }
    catch (e) { return num + ' EGP'; }
  }

  function applyStaticTranslations(root) {
    root = root || document;
    root.querySelectorAll('[data-i18n]').forEach(function (el) {
      el.textContent = t(el.getAttribute('data-i18n'));
    });
    root.querySelectorAll('[data-i18n-html]').forEach(function (el) {
      el.innerHTML = t(el.getAttribute('data-i18n-html'));
    });
    root.querySelectorAll('[data-i18n-placeholder]').forEach(function (el) {
      el.setAttribute('placeholder', t(el.getAttribute('data-i18n-placeholder')));
    });
    root.querySelectorAll('[data-i18n-aria]').forEach(function (el) {
      el.setAttribute('aria-label', t(el.getAttribute('data-i18n-aria')));
    });
  }

  function setLanguage(lang) {
    if (lang !== 'ar' && lang !== 'en') return;
    currentLang = lang;
    window.currentLang = lang;
    try { localStorage.setItem('lang', lang); } catch (e) {}
    document.documentElement.lang = lang;
    document.documentElement.dir = lang === 'ar' ? 'rtl' : 'ltr';
    document.title = t('doc_title');
    applyStaticTranslations(document);
    document.dispatchEvent(new CustomEvent('languagechange', { detail: { lang: lang } }));
  }

  function toggleLanguage() {
    setLanguage(currentLang === 'ar' ? 'en' : 'ar');
  }

  // Expose globals
  window.currentLang = currentLang;
  window.t = t;
  window.formatCurrency = formatCurrency;
  window.setLanguage = setLanguage;
  window.i18nApply = applyStaticTranslations;

  // Set <html> attributes as early as possible
  document.documentElement.lang = currentLang;
  document.documentElement.dir = currentLang === 'ar' ? 'rtl' : 'ltr';

  document.addEventListener('DOMContentLoaded', function () {
    applyStaticTranslations(document);
    document.title = t('doc_title');
    const langToggle = document.getElementById('langToggle');
    if (langToggle) langToggle.addEventListener('click', toggleLanguage);
  });
})();
