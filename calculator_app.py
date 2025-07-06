#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Calculator 404 - حاسبة قطونيل الذكية
Desktop Application Version - الإصدار الكامل
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import os
import math
from decimal import Decimal, InvalidOperation
from datetime import datetime

class Calculator404:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("حاسبة قطونيل الذكية - Calculator 404")
        self.root.geometry("600x700")
        self.root.resizable(True, True)
        
        # إعداد الخطوط
        self.arabic_font = ("Arial", 11)
        self.display_font = ("Courier New", 14, "bold")
        self.button_font = ("Arial", 10, "bold")
        self.title_font = ("Arial", 12, "bold")
        
        # متغيرات الحاسبة
        self.display_var = tk.StringVar(value="0")
        self.expression_var = tk.StringVar(value="")
        self.history = []
        self.load_history()
        
        # إعداد النافذة
        self.setup_ui()
        
        # ربط الأحداث
        self.root.bind('<Key>', self.on_key_press)
        self.root.focus_set()
        
    def setup_ui(self):
        """إعداد واجهة المستخدم"""
        # الشريط العلوي
        header_frame = tk.Frame(self.root, bg="#2563eb", height=60)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(
            header_frame, 
            text="حاسبة قطونيل الذكية - Calculator 404",
            font=self.title_font,
            bg="#2563eb",
            fg="white"
        )
        title_label.pack(pady=15)
        
        # التبويبات الرئيسية
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # تبويب الحاسبة
        self.calc_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.calc_frame, text="الحاسبة")
        self.setup_calculator_tab()
        
        # تبويب جرد الكاش
        self.inventory_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.inventory_frame, text="جرد الكاش")
        self.setup_inventory_tab()
        
        # تبويب المعادلات
        self.formulas_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.formulas_frame, text="معادلات")
        self.setup_formulas_tab()
        
        # تبويب ROI التسويق
        self.roi_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.roi_frame, text="ROI التسويق")
        self.setup_roi_tab()
        
        # تبويب تقفيل الوردية
        self.shift_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.shift_frame, text="تقفيل الوردية")
        self.setup_shift_tab()
        
    def setup_calculator_tab(self):
        """إعداد تبويب الحاسبة"""
        # منطقة العرض
        display_frame = tk.Frame(self.calc_frame, bg="white", pady=10)
        display_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # العملية الحالية
        self.expression_label = tk.Label(
            display_frame,
            textvariable=self.expression_var,
            font=("Arial", 10),
            bg="white",
            fg="gray",
            anchor="e"
        )
        self.expression_label.pack(fill=tk.X)
        
        # الشاشة الرئيسية
        self.display_entry = tk.Entry(
            display_frame,
            textvariable=self.display_var,
            font=self.display_font,
            justify="right",
            state="readonly",
            bg="#f8f9fa",
            relief="solid",
            bd=2
        )
        self.display_entry.pack(fill=tk.X, pady=5)
        
        # أزرار الحاسبة
        self.create_buttons()
        
        # سجل العمليات
        self.create_history_section()
        
    def create_buttons(self):
        """إنشاء أزرار الحاسبة"""
        buttons_frame = tk.Frame(self.calc_frame, bg="white")
        buttons_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # تخطيط الأزرار
        buttons = [
            ['C', '←', '%', '/'],
            ['7', '8', '9', '*'],
            ['4', '5', '6', '-'],
            ['1', '2', '3', '+'],
            ['0', '.', '=', '=']
        ]
        
        for i, row in enumerate(buttons):
            for j, btn_text in enumerate(row):
                if i == 4 and j == 0:  # زر الصفر
                    btn = tk.Button(
                        buttons_frame,
                        text=btn_text,
                        font=self.button_font,
                        command=lambda t=btn_text: self.on_button_click(t),
                        bg="#e5e7eb",
                        relief="raised",
                        bd=2
                    )
                    btn.grid(row=i, column=j, columnspan=2, sticky="nsew", padx=1, pady=1)
                elif i == 4 and j == 1:  # تخطي النقطة لأن الصفر يأخذ مكانين
                    continue
                elif i == 4 and j == 2:  # النقطة
                    btn = tk.Button(
                        buttons_frame,
                        text=btn_text,
                        font=self.button_font,
                        command=lambda t=btn_text: self.on_button_click(t),
                        bg="#e5e7eb",
                        relief="raised",
                        bd=2
                    )
                    btn.grid(row=i, column=j, sticky="nsew", padx=1, pady=1)
                elif i == 4 and j == 3:  # زر يساوي
                    btn = tk.Button(
                        buttons_frame,
                        text=btn_text,
                        font=self.button_font,
                        command=lambda t=btn_text: self.on_button_click(t),
                        bg="#10b981",
                        fg="white",
                        relief="raised",
                        bd=2
                    )
                    btn.grid(row=i, column=j, sticky="nsew", padx=1, pady=1)
                elif btn_text == 'C':  # زر المسح
                    btn = tk.Button(
                        buttons_frame,
                        text="مسح",
                        font=self.button_font,
                        command=lambda t=btn_text: self.on_button_click(t),
                        bg="#ef4444",
                        fg="white",
                        relief="raised",
                        bd=2
                    )
                    btn.grid(row=i, column=j, sticky="nsew", padx=1, pady=1)
                elif btn_text == '←':  # زر الحذف
                    btn = tk.Button(
                        buttons_frame,
                        text=btn_text,
                        font=self.button_font,
                        command=lambda t=btn_text: self.on_button_click(t),
                        bg="#f59e0b",
                        fg="white",
                        relief="raised",
                        bd=2
                    )
                    btn.grid(row=i, column=j, sticky="nsew", padx=1, pady=1)
                elif btn_text in ['+', '-', '*', '/', '%']:  # أزرار العمليات
                    display_text = {'*': '×', '/': '÷'}.get(btn_text, btn_text)
                    btn = tk.Button(
                        buttons_frame,
                        text=display_text,
                        font=self.button_font,
                        command=lambda t=btn_text: self.on_button_click(t),
                        bg="#2563eb",
                        fg="white",
                        relief="raised",
                        bd=2
                    )
                    btn.grid(row=i, column=j, sticky="nsew", padx=1, pady=1)
                else:  # أزرار الأرقام
                    btn = tk.Button(
                        buttons_frame,
                        text=btn_text,
                        font=self.button_font,
                        command=lambda t=btn_text: self.on_button_click(t),
                        bg="#e5e7eb",
                        relief="raised",
                        bd=2
                    )
                    btn.grid(row=i, column=j, sticky="nsew", padx=1, pady=1)
        
        # تكوين الشبكة
        for i in range(5):
            buttons_frame.grid_rowconfigure(i, weight=1)
        for j in range(4):
            buttons_frame.grid_columnconfigure(j, weight=1)
            
    def create_history_section(self):
        """إنشاء قسم سجل العمليات"""
        history_frame = tk.Frame(self.calc_frame, bg="white")
        history_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # عنوان السجل
        history_header = tk.Frame(history_frame, bg="white")
        history_header.pack(fill=tk.X, pady=(0, 5))
        
        tk.Label(
            history_header,
            text="السجل",
            font=("Arial", 12, "bold"),
            bg="white"
        ).pack(side=tk.LEFT)
        
        tk.Button(
            history_header,
            text="مسح السجل",
            font=("Arial", 9),
            command=self.clear_history,
            bg="#ef4444",
            fg="white",
            relief="raised"
        ).pack(side=tk.RIGHT)
        
        # قائمة السجل
        self.history_listbox = tk.Listbox(
            history_frame,
            font=("Arial", 10),
            height=6,
            bg="#f8f9fa",
            selectbackground="#2563eb"
        )
        self.history_listbox.pack(fill=tk.BOTH, expand=True)
        self.history_listbox.bind('<Double-1>', self.on_history_select)
        
        # تحديث السجل
        self.update_history_display()
        
    def setup_inventory_tab(self):
        """إعداد تبويب جرد الكاش"""
        main_frame = tk.Frame(self.inventory_frame, bg="white")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # عنوان القسم
        title_label = tk.Label(
            main_frame,
            text="جرد الكاش",
            font=self.title_font,
            bg="white"
        )
        title_label.pack(pady=10)
        
        # فئات النقود
        self.denominations = [200, 100, 50, 20, 10, 5]
        self.denomination_entries = {}
        
        for denom in self.denominations:
            frame = tk.Frame(main_frame, bg="white")
            frame.pack(fill=tk.X, pady=5)
            
            tk.Label(
                frame,
                text=f"{denom} جنيه",
                font=self.arabic_font,
                bg="white",
                width=10
            ).pack(side=tk.LEFT)
            
            entry = tk.Entry(
                frame,
                font=self.arabic_font,
                width=10,
                justify="center"
            )
            entry.pack(side=tk.LEFT, padx=10)
            entry.bind('<KeyRelease>', self.calculate_inventory_total)
            self.denomination_entries[denom] = entry
        
        # إجمالي الجرد
        total_frame = tk.Frame(main_frame, bg="#f0f0f0", relief="solid", bd=2)
        total_frame.pack(fill=tk.X, pady=20)
        
        tk.Label(
            total_frame,
            text="الإجمالي:",
            font=self.title_font,
            bg="#f0f0f0"
        ).pack(side=tk.LEFT, padx=10, pady=10)
        
        self.inventory_total_var = tk.StringVar(value="0.00 جنيه")
        tk.Label(
            total_frame,
            textvariable=self.inventory_total_var,
            font=("Arial", 16, "bold"),
            bg="#f0f0f0",
            fg="#2563eb"
        ).pack(side=tk.RIGHT, padx=10, pady=10)
        
        # أزرار التحقق
        buttons_frame = tk.Frame(main_frame, bg="white")
        buttons_frame.pack(pady=20)
        
        tk.Label(
            buttons_frame,
            text="هل الجرد صحيح؟",
            font=self.arabic_font,
            bg="white"
        ).pack(pady=10)
        
        btn_frame = tk.Frame(buttons_frame, bg="white")
        btn_frame.pack()
        
        tk.Button(
            btn_frame,
            text="نعم",
            font=self.button_font,
            bg="#10b981",
            fg="white",
            command=self.confirm_inventory
        ).pack(side=tk.LEFT, padx=10)
        
        tk.Button(
            btn_frame,
            text="لا",
            font=self.button_font,
            bg="#ef4444",
            fg="white",
            command=self.show_discrepancy
        ).pack(side=tk.LEFT, padx=10)
        
        # قسم الفرق
        self.discrepancy_frame = tk.Frame(main_frame, bg="#fff3cd", relief="solid", bd=2)
        
        tk.Label(
            self.discrepancy_frame,
            text="فحص الفرق",
            font=self.title_font,
            bg="#fff3cd"
        ).pack(pady=10)
        
        input_frame = tk.Frame(self.discrepancy_frame, bg="#fff3cd")
        input_frame.pack(pady=10)
        
        tk.Label(
            input_frame,
            text="المبلغ المتوقع:",
            font=self.arabic_font,
            bg="#fff3cd"
        ).pack(side=tk.LEFT)
        
        self.expected_entry = tk.Entry(
            input_frame,
            font=self.arabic_font,
            width=15
        )
        self.expected_entry.pack(side=tk.LEFT, padx=10)
        self.expected_entry.bind('<KeyRelease>', self.calculate_difference)
        
        self.difference_var = tk.StringVar(value="الفرق: 0.00 جنيه")
        tk.Label(
            self.discrepancy_frame,
            textvariable=self.difference_var,
            font=self.title_font,
            bg="#fff3cd"
        ).pack(pady=10)
        
    def setup_formulas_tab(self):
        """إعداد تبويب المعادلات"""
        main_frame = tk.Frame(self.formulas_frame, bg="white")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # قسم حاسبة الجملة
        wholesale_frame = tk.LabelFrame(
            main_frame,
            text="حاسبة الجملة",
            font=self.title_font,
            bg="white"
        )
        wholesale_frame.pack(fill=tk.X, pady=10)
        
        # سعر القطعة
        tk.Label(
            wholesale_frame,
            text="سعر القطعة:",
            font=self.arabic_font,
            bg="white"
        ).pack(anchor="w", padx=10, pady=5)
        
        self.piece_price_entry = tk.Entry(
            wholesale_frame,
            font=self.arabic_font,
            width=20
        )
        self.piece_price_entry.pack(padx=10, pady=5)
        
        # نسبة الخصم
        tk.Label(
            wholesale_frame,
            text="نسبة الخصم (%):",
            font=self.arabic_font,
            bg="white"
        ).pack(anchor="w", padx=10, pady=5)
        
        self.discount_entry = tk.Entry(
            wholesale_frame,
            font=self.arabic_font,
            width=20
        )
        self.discount_entry.pack(padx=10, pady=5)
        self.discount_entry.insert(0, "0")
        
        tk.Button(
            wholesale_frame,
            text="احسب سعر الجملة",
            font=self.button_font,
            bg="#2563eb",
            fg="white",
            command=self.calculate_wholesale
        ).pack(pady=10)
        
        self.wholesale_result_var = tk.StringVar(value="")
        self.wholesale_result_label = tk.Label(
            wholesale_frame,
            textvariable=self.wholesale_result_var,
            font=("Arial", 14, "bold"),
            bg="white",
            fg="#10b981"
        )
        self.wholesale_result_label.pack(pady=10)
        
        # قسم محول القطع
        conversion_frame = tk.LabelFrame(
            main_frame,
            text="محول القطع",
            font=self.title_font,
            bg="white"
        )
        conversion_frame.pack(fill=tk.X, pady=10)
        
        # عدد القطع
        tk.Label(
            conversion_frame,
            text="عدد القطع:",
            font=self.arabic_font,
            bg="white"
        ).pack(anchor="w", padx=10, pady=5)
        
        self.pieces_entry = tk.Entry(
            conversion_frame,
            font=self.arabic_font,
            width=20
        )
        self.pieces_entry.pack(padx=10, pady=5)
        
        # الوحدة
        tk.Label(
            conversion_frame,
            text="الوحدة:",
            font=self.arabic_font,
            bg="white"
        ).pack(anchor="w", padx=10, pady=5)
        
        self.unit_var = tk.StringVar(value="دستة (12 قطعة)")
        unit_combo = ttk.Combobox(
            conversion_frame,
            textvariable=self.unit_var,
            values=["دستة (12 قطعة)", "نص دستة (6 قطع)"],
            font=self.arabic_font,
            state="readonly"
        )
        unit_combo.pack(padx=10, pady=5)
        
        tk.Button(
            conversion_frame,
            text="تحويل",
            font=self.button_font,
            bg="#2563eb",
            fg="white",
            command=self.convert_pieces
        ).pack(pady=10)
        
        self.conversion_result_var = tk.StringVar(value="")
        self.conversion_result_label = tk.Label(
            conversion_frame,
            textvariable=self.conversion_result_var,
            font=("Arial", 14, "bold"),
            bg="white",
            fg="#0ea5e9"
        )
        self.conversion_result_label.pack(pady=10)
        
    def setup_roi_tab(self):
        """إعداد تبويب ROI التسويق"""
        main_frame = tk.Frame(self.roi_frame, bg="white")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # عنوان القسم
        title_label = tk.Label(
            main_frame,
            text="حاسبة ROI التسويق",
            font=self.title_font,
            bg="white"
        )
        title_label.pack(pady=10)
        
        # تكلفة الحملة
        tk.Label(
            main_frame,
            text="تكلفة الحملة الإعلانية:",
            font=self.arabic_font,
            bg="white"
        ).pack(anchor="w", padx=10, pady=5)
        
        self.campaign_cost_entry = tk.Entry(
            main_frame,
            font=self.arabic_font,
            width=20
        )
        self.campaign_cost_entry.pack(padx=10, pady=5)
        
        # سعر البيع
        tk.Label(
            main_frame,
            text="سعر البيع للقطعة:",
            font=self.arabic_font,
            bg="white"
        ).pack(anchor="w", padx=10, pady=5)
        
        self.selling_price_entry = tk.Entry(
            main_frame,
            font=self.arabic_font,
            width=20
        )
        self.selling_price_entry.pack(padx=10, pady=5)
        
        # تكلفة القطعة
        tk.Label(
            main_frame,
            text="تكلفة القطعة:",
            font=self.arabic_font,
            bg="white"
        ).pack(anchor="w", padx=10, pady=5)
        
        self.cost_price_entry = tk.Entry(
            main_frame,
            font=self.arabic_font,
            width=20
        )
        self.cost_price_entry.pack(padx=10, pady=5)
        
        tk.Button(
            main_frame,
            text="احسب ROI",
            font=self.button_font,
            bg="#2563eb",
            fg="white",
            command=self.calculate_roi
        ).pack(pady=20)
        
        # النتائج
        self.roi_results_frame = tk.Frame(main_frame, bg="white")
        self.roi_results_frame.pack(fill=tk.X, pady=10)
        
    def setup_shift_tab(self):
        """إعداد تبويب تقفيل الوردية"""
        main_frame = tk.Frame(self.shift_frame, bg="white")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # عنوان القسم
        title_label = tk.Label(
            main_frame,
            text="تقفيل الوردية",
            font=self.title_font,
            bg="white"
        )
        title_label.pack(pady=10)
        
        # إطار الإدخال
        input_frame = tk.Frame(main_frame, bg="white")
        input_frame.pack(fill=tk.X, pady=10)
        
        # الإيرادات
        revenue_frame = tk.LabelFrame(
            input_frame,
            text="الإيرادات",
            font=self.title_font,
            bg="white",
            fg="#10b981"
        )
        revenue_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        
        # حقول الإيرادات
        tk.Label(revenue_frame, text="الحصالة في بداية الوردية:", font=self.arabic_font, bg="white").pack(anchor="w", padx=10, pady=5)
        self.cash_box_entry = tk.Entry(revenue_frame, font=self.arabic_font, width=15)
        self.cash_box_entry.pack(padx=10, pady=5)
        self.cash_box_entry.insert(0, "0")
        
        tk.Label(revenue_frame, text="مبيعات كاش:", font=self.arabic_font, bg="white").pack(anchor="w", padx=10, pady=5)
        self.cash_sales_entry = tk.Entry(revenue_frame, font=self.arabic_font, width=15)
        self.cash_sales_entry.pack(padx=10, pady=5)
        self.cash_sales_entry.insert(0, "0")
        
        tk.Label(revenue_frame, text="إيرادات أخرى:", font=self.arabic_font, bg="white").pack(anchor="w", padx=10, pady=5)
        self.other_income_entry = tk.Entry(revenue_frame, font=self.arabic_font, width=15)
        self.other_income_entry.pack(padx=10, pady=5)
        self.other_income_entry.insert(0, "0")
        
        # المصروفات
        expense_frame = tk.LabelFrame(
            input_frame,
            text="المصروفات",
            font=self.title_font,
            bg="white",
            fg="#ef4444"
        )
        expense_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5)
        
        # حقول المصروفات
        tk.Label(expense_frame, text="مصروفات:", font=self.arabic_font, bg="white").pack(anchor="w", padx=10, pady=5)
        self.expenses_entry = tk.Entry(expense_frame, font=self.arabic_font, width=15)
        self.expenses_entry.pack(padx=10, pady=5)
        self.expenses_entry.insert(0, "0")
        
        tk.Label(expense_frame, text="خصومات:", font=self.arabic_font, bg="white").pack(anchor="w", padx=10, pady=5)
        self.discounts_entry = tk.Entry(expense_frame, font=self.arabic_font, width=15)
        self.discounts_entry.pack(padx=10, pady=5)
        self.discounts_entry.insert(0, "0")
        
        tk.Label(expense_frame, text="مدفوعات فيزا:", font=self.arabic_font, bg="white").pack(anchor="w", padx=10, pady=5)
        self.visa_payments_entry = tk.Entry(expense_frame, font=self.arabic_font, width=15)
        self.visa_payments_entry.pack(padx=10, pady=5)
        self.visa_payments_entry.insert(0, "0")
        
        # زر الحساب
        tk.Button(
            main_frame,
            text="احسب النتائج",
            font=self.button_font,
            bg="#2563eb",
            fg="white",
            command=self.calculate_shift
        ).pack(pady=20)
        
        # النتائج
        self.shift_results_frame = tk.Frame(main_frame, bg="white")
        self.shift_results_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
    # دوال جرد الكاش
    def calculate_inventory_total(self, event=None):
        """حساب إجمالي الجرد"""
        total = 0
        for denom, entry in self.denomination_entries.items():
            try:
                count = int(entry.get() or 0)
                total += count * denom
            except ValueError:
                pass
        
        self.inventory_total_var.set(f"{total:.2f} جنيه")
        
    def confirm_inventory(self):
        """تأكيد صحة الجرد"""
        messagebox.showinfo("تأكيد", "رائع! تم تأكيد الجرد.")
        self.discrepancy_frame.pack_forget()
        
    def show_discrepancy(self):
        """إظهار قسم الفرق"""
        self.discrepancy_frame.pack(fill=tk.X, pady=10)
        
    def calculate_difference(self, event=None):
        """حساب الفرق بين الجرد والمتوقع"""
        try:
            total = float(self.inventory_total_var.get().replace(" جنيه", ""))
            expected = float(self.expected_entry.get() or 0)
            difference = total - expected
            
            color = "black" if difference == 0 else ("green" if difference > 0 else "red")
            self.difference_var.set(f"الفرق: {difference:.2f} جنيه")
        except ValueError:
            self.difference_var.set("الفرق: 0.00 جنيه")
            
    # دوال المعادلات
    def calculate_wholesale(self):
        """حساب سعر الجملة"""
        try:
            price = float(self.piece_price_entry.get())
            discount = float(self.discount_entry.get() or 0)
            
            if price <= 0:
                messagebox.showerror("خطأ", "يجب إدخال سعر صحيح للقطعة")
                return
                
            # تطبيق معادلة الجملة: (سعر القطعة * 10 * (1 - الخصم/100)) / 12
            wholesale_price = (price * 10 * (1 - discount / 100)) / 12
            self.wholesale_result_var.set(f"سعر الجملة: {wholesale_price:.2f} جنيه")
            
        except ValueError:
            messagebox.showerror("خطأ", "يجب إدخال أرقام صحيحة")
            
    def convert_pieces(self):
        """تحويل القطع"""
        try:
            pieces = int(self.pieces_entry.get())
            unit_text = self.unit_var.get()
            
            if pieces <= 0:
                messagebox.showerror("خطأ", "يجب إدخال عدد صحيح من القطع")
                return
                
            unit_size = 12 if "دستة" in unit_text else 6
            unit_name = "دستة" if unit_size == 12 else "نص دستة"
            
            result = pieces / unit_size
            self.conversion_result_var.set(f"النتيجة: {result:.2f} {unit_name}")
            
        except ValueError:
            messagebox.showerror("خطأ", "يجب إدخال رقم صحيح")
            
    # دوال ROI التسويق
    def calculate_roi(self):
        """حساب ROI التسويق"""
        try:
            campaign_cost = float(self.campaign_cost_entry.get())
            selling_price = float(self.selling_price_entry.get())
            cost_price = float(self.cost_price_entry.get())
            
            if campaign_cost <= 0:
                messagebox.showerror("خطأ", "يجب إدخال تكلفة صحيحة للحملة")
                return
            if selling_price <= 0:
                messagebox.showerror("خطأ", "يجب إدخال سعر بيع صحيح")
                return
            if cost_price <= 0:
                messagebox.showerror("خطأ", "يجب إدخال تكلفة صحيحة للقطعة")
                return
            if selling_price <= cost_price:
                messagebox.showerror("خطأ", "سعر البيع يجب أن يكون أعلى من التكلفة")
                return
                
            # حساب هامش الربح
            profit_per_piece = selling_price - cost_price
            profit_margin_ratio = profit_per_piece / selling_price
            
            # حساب المبيعات المطلوبة
            required_sales = campaign_cost / profit_margin_ratio
            required_pieces = math.ceil(required_sales / selling_price)
            
            # مسح النتائج السابقة
            for widget in self.roi_results_frame.winfo_children():
                widget.destroy()
                
            # عرض النتائج
            tk.Label(
                self.roi_results_frame,
                text="النتائج:",
                font=self.title_font,
                bg="white"
            ).pack(pady=10)
            
            results_frame = tk.Frame(self.roi_results_frame, bg="white")
            results_frame.pack(fill=tk.X, pady=10)
            
            # المبيعات المطلوبة
            sales_frame = tk.Frame(results_frame, bg="#e6f3ff", relief="solid", bd=1)
            sales_frame.pack(fill=tk.X, pady=5)
            
            tk.Label(
                sales_frame,
                text="المبيعات المطلوبة:",
                font=self.arabic_font,
                bg="#e6f3ff"
            ).pack(side=tk.LEFT, padx=10, pady=10)
            
            tk.Label(
                sales_frame,
                text=f"{required_sales:.2f} جنيه",
                font=("Arial", 12, "bold"),
                bg="#e6f3ff",
                fg="#0ea5e9"
            ).pack(side=tk.RIGHT, padx=10, pady=10)
            
            # عدد القطع المطلوبة
            pieces_frame = tk.Frame(results_frame, bg="#e6ffe6", relief="solid", bd=1)
            pieces_frame.pack(fill=tk.X, pady=5)
            
            tk.Label(
                pieces_frame,
                text="عدد القطع المطلوبة:",
                font=self.arabic_font,
                bg="#e6ffe6"
            ).pack(side=tk.LEFT, padx=10, pady=10)
            
            tk.Label(
                pieces_frame,
                text=f"{required_pieces} قطعة",
                font=("Arial", 12, "bold"),
                bg="#e6ffe6",
                fg="#10b981"
            ).pack(side=tk.RIGHT, padx=10, pady=10)
            
            # هامش الربح
            margin_frame = tk.Frame(results_frame, bg="#fff3e6", relief="solid", bd=1)
            margin_frame.pack(fill=tk.X, pady=5)
            
            tk.Label(
                margin_frame,
                text="هامش الربح:",
                font=self.arabic_font,
                bg="#fff3e6"
            ).pack(side=tk.LEFT, padx=10, pady=10)
            
            tk.Label(
                margin_frame,
                text=f"{profit_per_piece:.2f} جنيه ({profit_margin_ratio*100:.1f}%)",
                font=("Arial", 12, "bold"),
                bg="#fff3e6",
                fg="#f59e0b"
            ).pack(side=tk.RIGHT, padx=10, pady=10)
            
        except ValueError:
            messagebox.showerror("خطأ", "يجب إدخال أرقام صحيحة")
            
    # دوال تقفيل الوردية
    def calculate_shift(self):
        """حساب نتائج الوردية"""
        try:
            # جمع البيانات
            cash_box = float(self.cash_box_entry.get() or 0)
            cash_sales = float(self.cash_sales_entry.get() or 0)
            other_income = float(self.other_income_entry.get() or 0)
            expenses = float(self.expenses_entry.get() or 0)
            discounts = float(self.discounts_entry.get() or 0)
            visa_payments = float(self.visa_payments_entry.get() or 0)
            
            # حساب الإجماليات
            total_revenue = cash_box + cash_sales + other_income
            total_expenses = expenses + discounts + visa_payments
            net_revenue = total_revenue - total_expenses
            
            # حساب المبلغ المرحل
            carried_over = 0
            cash_box_left = 0
            message = ""
            
            if net_revenue >= 100:
                carried_over = (net_revenue // 100) * 100
                cash_box_left = net_revenue - carried_over
            elif net_revenue > 0:
                carried_over = 0
                cash_box_left = net_revenue
                message = "المبلغ أقل من 100 جنيه، سيتم تركه كحصالة فقط."
            else:
                carried_over = 0
                cash_box_left = net_revenue
                message = "يوجد عجز في الوردية!" if net_revenue < 0 else "لا توجد أموال للترحيل."
                
            # مسح النتائج السابقة
            for widget in self.shift_results_frame.winfo_children():
                widget.destroy()
                
            # عرض النتائج
            tk.Label(
                self.shift_results_frame,
                text="نتائج الوردية",
                font=self.title_font,
                bg="white"
            ).pack(pady=10)
            
            # الإيرادات
            revenue_frame = tk.Frame(self.shift_results_frame, bg="#e6ffe6", relief="solid", bd=2)
            revenue_frame.pack(fill=tk.X, pady=5)
            
            tk.Label(
                revenue_frame,
                text="إجمالي الإيرادات:",
                font=self.arabic_font,
                bg="#e6ffe6"
            ).pack(side=tk.LEFT, padx=10, pady=10)
            
            tk.Label(
                revenue_frame,
                text=f"{total_revenue:.2f} جنيه",
                font=("Arial", 12, "bold"),
                bg="#e6ffe6",
                fg="#10b981"
            ).pack(side=tk.RIGHT, padx=10, pady=10)
            
            # المصروفات
            expense_frame = tk.Frame(self.shift_results_frame, bg="#ffe6e6", relief="solid", bd=2)
            expense_frame.pack(fill=tk.X, pady=5)
            
            tk.Label(
                expense_frame,
                text="إجمالي المصروفات:",
                font=self.arabic_font,
                bg="#ffe6e6"
            ).pack(side=tk.LEFT, padx=10, pady=10)
            
            tk.Label(
                expense_frame,
                text=f"{total_expenses:.2f} جنيه",
                font=("Arial", 12, "bold"),
                bg="#ffe6e6",
                fg="#ef4444"
            ).pack(side=tk.RIGHT, padx=10, pady=10)
            
            # صافي الوردية
            net_bg = "#e6ffe6" if net_revenue >= 0 else "#ffe6e6"
            net_color = "#10b981" if net_revenue >= 0 else "#ef4444"
            
            net_frame = tk.Frame(self.shift_results_frame, bg=net_bg, relief="solid", bd=2)
            net_frame.pack(fill=tk.X, pady=5)
            
            tk.Label(
                net_frame,
                text="صافي الوردية:",
                font=self.title_font,
                bg=net_bg
            ).pack(side=tk.LEFT, padx=10, pady=10)
            
            tk.Label(
                net_frame,
                text=f"{net_revenue:.2f} جنيه",
                font=("Arial", 14, "bold"),
                bg=net_bg,
                fg=net_color
            ).pack(side=tk.RIGHT, padx=10, pady=10)
            
            # المبلغ المرحل
            carry_frame = tk.Frame(self.shift_results_frame, bg="#e6f3ff", relief="solid", bd=2)
            carry_frame.pack(fill=tk.X, pady=5)
            
            tk.Label(
                carry_frame,
                text="المبلغ المرحل:",
                font=self.arabic_font,
                bg="#e6f3ff"
            ).pack(side=tk.LEFT, padx=10, pady=10)
            
            tk.Label(
                carry_frame,
                text=f"{carried_over:.2f} جنيه",
                font=("Arial", 12, "bold"),
                bg="#e6f3ff",
                fg="#0ea5e9"
            ).pack(side=tk.RIGHT, padx=10, pady=10)
            
            # المتبقي للدرج
            left_frame = tk.Frame(self.shift_results_frame, bg="#fff3e6", relief="solid", bd=2)
            left_frame.pack(fill=tk.X, pady=5)
            
            tk.Label(
                left_frame,
                text="المتبقي للدرج:",
                font=self.arabic_font,
                bg="#fff3e6"
            ).pack(side=tk.LEFT, padx=10, pady=10)
            
            tk.Label(
                left_frame,
                text=f"{cash_box_left:.2f} جنيه",
                font=("Arial", 12, "bold"),
                bg="#fff3e6",
                fg="#f59e0b"
            ).pack(side=tk.RIGHT, padx=10, pady=10)
            
            # الرسالة الإضافية
            if message:
                tk.Label(
                    self.shift_results_frame,
                    text=message,
                    font=self.arabic_font,
                    bg="white",
                    fg="#ef4444" if "عجز" in message else "#10b981"
                ).pack(pady=10)
                
            # أزرار الإجراءات
            actions_frame = tk.Frame(self.shift_results_frame, bg="white")
            actions_frame.pack(pady=20)
            
            tk.Button(
                actions_frame,
                text="حفظ التقرير",
                font=self.button_font,
                bg="#10b981",
                fg="white",
                command=lambda: self.save_shift_report({
                    'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    'inputs': {
                        'cash_box': cash_box,
                        'cash_sales': cash_sales,
                        'other_income': other_income,
                        'expenses': expenses,
                        'discounts': discounts,
                        'visa_payments': visa_payments
                    },
                    'results': {
                        'total_revenue': total_revenue,
                        'total_expenses': total_expenses,
                        'net_revenue': net_revenue,
                        'carried_over': carried_over,
                        'cash_box_left': cash_box_left
                    },
                    'message': message
                })
            ).pack(side=tk.LEFT, padx=10)
            
            tk.Button(
                actions_frame,
                text="مسح البيانات",
                font=self.button_font,
                bg="#ef4444",
                fg="white",
                command=self.clear_shift_data
            ).pack(side=tk.LEFT, padx=10)
            
        except ValueError:
            messagebox.showerror("خطأ", "يجب إدخال أرقام صحيحة")
            
    def save_shift_report(self, data):
        """حفظ تقرير الوردية"""
        try:
            filename = filedialog.asksaveasfilename(
                defaultextension=".json",
                filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
                title="حفظ تقرير الوردية"
            )
            
            if filename:
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
                messagebox.showinfo("نجح", "تم حفظ التقرير بنجاح!")
        except Exception as e:
            messagebox.showerror("خطأ", f"حدث خطأ أثناء الحفظ: {str(e)}")
            
    def clear_shift_data(self):
        """مسح بيانات الوردية"""
        if messagebox.askyesno("تأكيد", "هل أنت متأكد من مسح جميع البيانات؟"):
            self.cash_box_entry.delete(0, tk.END)
            self.cash_box_entry.insert(0, "0")
            self.cash_sales_entry.delete(0, tk.END)
            self.cash_sales_entry.insert(0, "0")
            self.other_income_entry.delete(0, tk.END)
            self.other_income_entry.insert(0, "0")
            self.expenses_entry.delete(0, tk.END)
            self.expenses_entry.insert(0, "0")
            self.discounts_entry.delete(0, tk.END)
            self.discounts_entry.insert(0, "0")
            self.visa_payments_entry.delete(0, tk.END)
            self.visa_payments_entry.insert(0, "0")
            
            # مسح النتائج
            for widget in self.shift_results_frame.winfo_children():
                widget.destroy()
        
    def on_button_click(self, button_text):
        """معالجة النقر على الأزرار"""
        if button_text == 'C':
            self.clear_display()
        elif button_text == '←':
            self.backspace()
        elif button_text == '=':
            self.calculate()
        else:
            self.add_to_display(button_text)
            
    def add_to_display(self, value):
        """إضافة قيمة للعرض"""
        current = self.display_var.get()
        if current == "0" or current == "خطأ":
            self.display_var.set(value)
        else:
            self.display_var.set(current + value)
            
    def clear_display(self):
        """مسح العرض"""
        self.display_var.set("0")
        self.expression_var.set("")
        
    def backspace(self):
        """حذف آخر حرف"""
        current = self.display_var.get()
        if len(current) > 1:
            self.display_var.set(current[:-1])
        else:
            self.display_var.set("0")
            
    def calculate(self):
        """حساب التعبير الرياضي"""
        try:
            expression = self.display_var.get()
            if expression == "خطأ":
                return
                
            # معالجة النسبة المئوية
            expression = expression.replace('%', '/100')
            
            # التحقق من صحة التعبير
            if not self.is_valid_expression(expression):
                raise ValueError("تعبير غير صحيح")
                
            # الحساب
            result = eval(expression)
            
            if not isinstance(result, (int, float)) or not math.isfinite(result):
                raise ValueError("نتيجة غير صحيحة")
                
            # تحديث العرض
            self.expression_var.set(f"{self.display_var.get()} =")
            result_str = self.format_result(result)
            self.display_var.set(result_str)
            
            # إضافة للسجل
            self.add_to_history(expression, result_str)
            
        except Exception as e:
            self.display_var.set("خطأ")
            self.expression_var.set("")
            
    def is_valid_expression(self, expression):
        """التحقق من صحة التعبير الرياضي"""
        # التحقق من وجود عمليات متتالية
        operators = ['+', '-', '*', '/', '.']
        for i in range(len(expression) - 1):
            if expression[i] in operators and expression[i+1] in operators:
                return False
        return True
        
    def format_result(self, result):
        """تنسيق النتيجة"""
        if isinstance(result, float):
            if result.is_integer():
                return str(int(result))
            else:
                return f"{result:.10g}"
        return str(result)
        
    def add_to_history(self, expression, result):
        """إضافة عملية للسجل"""
        self.history.append({"expression": expression, "result": result})
        if len(self.history) > 20:
            self.history.pop(0)
        self.save_history()
        self.update_history_display()
        
    def update_history_display(self):
        """تحديث عرض السجل"""
        self.history_listbox.delete(0, tk.END)
        for item in reversed(self.history):
            display_text = f"{item['expression']} = {item['result']}"
            self.history_listbox.insert(0, display_text)
            
    def on_history_select(self, event):
        """معالجة اختيار عنصر من السجل"""
        selection = self.history_listbox.curselection()
        if selection:
            index = selection[0]
            # الحصول على النتيجة من السجل
            history_index = len(self.history) - 1 - index
            if 0 <= history_index < len(self.history):
                result = self.history[history_index]["result"]
                self.display_var.set(result)
                self.expression_var.set("")
                
    def clear_history(self):
        """مسح السجل"""
        self.history = []
        self.save_history()
        self.update_history_display()
        
    def save_history(self):
        """حفظ السجل في ملف"""
        try:
            with open("calculator_history.json", "w", encoding="utf-8") as f:
                json.dump(self.history, f, ensure_ascii=False, indent=2)
        except Exception:
            pass
            
    def load_history(self):
        """تحميل السجل من ملف"""
        try:
            if os.path.exists("calculator_history.json"):
                with open("calculator_history.json", "r", encoding="utf-8") as f:
                    self.history = json.load(f)
        except Exception:
            self.history = []
            
    def on_key_press(self, event):
        """معالجة الضغط على المفاتيح"""
        key = event.keysym
        char = event.char
        
        if char in '0123456789.+-*/%':
            self.add_to_display(char)
        elif key == 'Return' or key == 'KP_Enter':
            self.calculate()
        elif key == 'BackSpace':
            self.backspace()
        elif key == 'Delete' or key == 'Escape':
            self.clear_display()
            
    def run(self):
        """تشغيل التطبيق"""
        self.root.mainloop()

if __name__ == "__main__":
    app = Calculator404()
    app.run()