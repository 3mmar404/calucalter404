
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
        self.root.geometry("650x750")
        self.root.resizable(True, True)
        
        # إعداد الألوان والثيم
        self.colors = {
            'primary': '#2563eb',
            'secondary': '#1e40af',
            'success': '#10b981',
            'warning': '#f59e0b',
            'danger': '#ef4444',
            'info': '#0ea5e9',
            'light': '#f8fafc',
            'dark': '#1f2937',
            'white': '#ffffff',
            'gray_50': '#f9fafb',
            'gray_100': '#f3f4f6',
            'gray_200': '#e5e7eb',
            'gray_300': '#d1d5db',
            'gray_500': '#6b7280',
            'gray_600': '#4b5563',
            'gray_700': '#374151',
            'gray_800': '#1f2937',
            'gray_900': '#111827'
        }
        
        # إعداد الخطوط المحسنة
        self.fonts = {
            'arabic': ("Segoe UI", 11),
            'arabic_bold': ("Segoe UI", 11, "bold"),
            'display': ("Consolas", 16, "bold"),
            'button': ("Segoe UI", 10, "bold"),
            'title': ("Segoe UI", 13, "bold"),
            'subtitle': ("Segoe UI", 12),
            'small': ("Segoe UI", 9),
            'large': ("Segoe UI", 14, "bold")
        }
        
        # إعداد الأيقونات والرموز
        self.icons = {
            'calculator': '🧮',
            'inventory': '💰',
            'formulas': '📊',
            'roi': '📈',
            'shift': '🔄',
            'save': '💾',
            'clear': '🗑️',
            'check': '✅',
            'warning': '⚠️',
            'info': 'ℹ️',
            'money': '💵',
            'chart': '📋'
        }
        
        # متغيرات الحاسبة
        self.display_var = tk.StringVar(value="0")
        self.expression_var = tk.StringVar(value="")
        self.history = []
        self.load_history()
        
        # إعداد النافذة والستايل
        self.setup_window_style()
        self.setup_ui()
        
        # إضافة تأثيرات الانتقال والحركة
        self.setup_animations()
        
        # ربط الأحداث
        self.root.bind('<Key>', self.on_key_press)
        self.root.focus_set()
        
        # إضافة رسالة الترحيب
        self.show_welcome_message()
        
    def setup_window_style(self):
        """إعداد ستايل النافذة"""
        # تحسين مظهر النافذة
        self.root.configure(bg=self.colors['light'])
        
        # إعداد الأيقونة إذا كانت موجودة
        try:
            if os.path.exists("assets/favicon.ico"):
                self.root.iconbitmap("assets/favicon.ico")
        except:
            pass
            
        # إضافة ظل للنافذة إذا كان متاحاً
        try:
            self.root.wm_attributes('-topmost', False)
        except:
            pass
            
        # تحسين نظام التشغيل
        try:
            self.root.tk.call('tk', 'scaling', 1.2)  # تحسين الدقة
        except:
            pass
        
    def setup_ui(self):
        """إعداد واجهة المستخدم"""
        # الشريط العلوي المحسن
        header_frame = tk.Frame(self.root, bg=self.colors['primary'], height=70)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        # إضافة تدرج لوني باستخدام frames متعددة
        gradient_frame = tk.Frame(header_frame, bg=self.colors['secondary'], height=5)
        gradient_frame.pack(fill=tk.X, side=tk.BOTTOM)
        
        # العنوان مع الأيقونة
        title_container = tk.Frame(header_frame, bg=self.colors['primary'])
        title_container.pack(expand=True, fill=tk.BOTH)
        
        title_label = tk.Label(
            title_container, 
            text=f"{self.icons['calculator']} حاسبة قطونيل الذكية - Calculator 404",
            font=self.fonts['title'],
            bg=self.colors['primary'],
            fg=self.colors['white']
        )
        title_label.pack(pady=18)
        
        # إضافة خط تحت العنوان
        subtitle_label = tk.Label(
            title_container,
            text="النسخة الكاملة - جميع الأدوات في مكان واحد",
            font=self.fonts['small'],
            bg=self.colors['primary'],
            fg=self.colors['gray_200']
        )
        subtitle_label.pack(pady=(0, 10))
        
        # التبويبات الرئيسية المحسنة
        self.setup_notebook_style()
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)
        
        # ربط حدث تغيير التبويب
        self.notebook.bind('<<NotebookTabChanged>>', self.on_tab_change)
        
        # تبويب الحاسبة
        self.calc_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.calc_frame, text=f"{self.icons['calculator']} الحاسبة")
        self.setup_calculator_tab()
        
        # تبويب جرد الكاش
        self.inventory_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.inventory_frame, text=f"{self.icons['inventory']} جرد الكاش")
        self.setup_inventory_tab()
        
        # تبويب المعادلات
        self.formulas_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.formulas_frame, text=f"{self.icons['formulas']} معادلات")
        self.setup_formulas_tab()
        
        # تبويب ROI التسويق
        self.roi_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.roi_frame, text=f"{self.icons['roi']} ROI التسويق")
        self.setup_roi_tab()
        
        # تبويب تقفيل الوردية
        self.shift_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.shift_frame, text=f"{self.icons['shift']} تقفيل الوردية")
        self.setup_shift_tab()
        
        # إضافة شريط الحالة
        self.setup_status_bar()
        
    def setup_notebook_style(self):
        """إعداد ستايل التبويبات"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # تحسين ستايل التبويبات
        style.configure('TNotebook', 
                       background=self.colors['light'],
                       borderwidth=0)
        
        style.configure('TNotebook.Tab',
                       background=self.colors['gray_100'],
                       foreground=self.colors['gray_700'],
                       padding=[20, 10],
                       font=self.fonts['arabic_bold'])
        
        style.map('TNotebook.Tab',
                 background=[('selected', self.colors['primary']),
                            ('active', self.colors['gray_200'])],
                 foreground=[('selected', self.colors['white']),
                            ('active', self.colors['gray_900'])])
                            
    def setup_status_bar(self):
        """إعداد شريط الحالة"""
        status_frame = tk.Frame(self.root, bg=self.colors['gray_100'], height=30)
        status_frame.pack(fill=tk.X, side=tk.BOTTOM)
        status_frame.pack_propagate(False)
        
        # معلومات الحالة
        self.status_var = tk.StringVar(value="جاهز للاستخدام")
        status_label = tk.Label(
            status_frame,
            textvariable=self.status_var,
            font=self.fonts['small'],
            bg=self.colors['gray_100'],
            fg=self.colors['gray_600']
        )
        status_label.pack(side=tk.LEFT, padx=10, pady=5)
        
        # الوقت الحالي
        self.time_var = tk.StringVar()
        time_label = tk.Label(
            status_frame,
            textvariable=self.time_var,
            font=self.fonts['small'],
            bg=self.colors['gray_100'],
            fg=self.colors['gray_600']
        )
        time_label.pack(side=tk.RIGHT, padx=10, pady=5)
        
        # تحديث الوقت
        self.update_time()
        
    def setup_animations(self):
        """إعداد التأثيرات والحركات"""
        # تأثير الظهور التدريجي للنافذة
        self.root.attributes('-alpha', 0.0)
        self.fade_in()
        
    def fade_in(self):
        """تأثير الظهور التدريجي"""
        alpha = self.root.attributes('-alpha')
        if alpha < 1.0:
            alpha += 0.05
            self.root.attributes('-alpha', alpha)
            self.root.after(30, self.fade_in)
            
    def show_welcome_message(self):
        """عرض رسالة الترحيب"""
        self.status_var.set("🎉 مرحباً بك في حاسبة قطونيل الذكية!")
        self.root.after(3000, lambda: self.status_var.set("جاهز للاستخدام"))
        
    def add_button_hover_effects(self, button, normal_color, hover_color):
        """إضافة تأثيرات hover للأزرار"""
        def on_enter(e):
            button.config(bg=hover_color)
            
        def on_leave(e):
            button.config(bg=normal_color)
            
        button.bind("<Enter>", on_enter)
        button.bind("<Leave>", on_leave)
        
    def play_click_sound(self):
        """تشغيل صوت عند النقر"""
        try:
            # يمكن إضافة مكتبة playsound أو winsound للأصوات
            import winsound
            winsound.MessageBeep(winsound.MB_OK)
        except:
            pass  # تجاهل الأخطاء إذا لم تكن الأصوات متاحة
            
    def on_tab_change(self, event):
        """معالجة تغيير التبويب"""
        selected_tab = self.notebook.index(self.notebook.select())
        tab_names = ["الحاسبة", "جرد الكاش", "معادلات", "ROI التسويق", "تقفيل الوردية"]
        
        if selected_tab < len(tab_names):
            self.status_var.set(f"🔄 تم الانتقال إلى تبويب {tab_names[selected_tab]}")
            
            # تشغيل صوت التبديل
            self.play_click_sound()
        
    def setup_calculator_tab(self):
        """إعداد تبويب الحاسبة"""
        # منطقة العرض المحسنة
        display_container = tk.Frame(self.calc_frame, bg=self.colors['white'])
        display_container.pack(fill=tk.X, padx=15, pady=10)
        
        # إطار العرض مع تأثيرات الظل
        display_frame = tk.Frame(display_container, bg=self.colors['white'], relief="solid", bd=1)
        display_frame.pack(fill=tk.X, pady=5)
        
        # إطار داخلي للعرض
        inner_display = tk.Frame(display_frame, bg=self.colors['gray_50'], padx=15, pady=15)
        inner_display.pack(fill=tk.X, padx=2, pady=2)
        
        # العملية الحالية
        self.expression_label = tk.Label(
            inner_display,
            textvariable=self.expression_var,
            font=self.fonts['small'],
            bg=self.colors['gray_50'],
            fg=self.colors['gray_500'],
            anchor="e"
        )
        self.expression_label.pack(fill=tk.X, pady=(0, 5))
        
        # الشاشة الرئيسية المحسنة
        self.display_entry = tk.Entry(
            inner_display,
            textvariable=self.display_var,
            font=self.fonts['display'],
            justify="right",
            state="readonly",
            bg=self.colors['white'],
            fg=self.colors['gray_900'],
            relief="solid",
            bd=2,
            highlightthickness=1,
            highlightcolor=self.colors['primary']
        )
        self.display_entry.pack(fill=tk.X, pady=(0, 5), ipady=10)
        
        # أزرار الحاسبة
        self.create_buttons()
        
        # سجل العمليات
        self.create_history_section()
        
    def create_buttons(self):
        """إنشاء أزرار الحاسبة المحسنة"""
        buttons_container = tk.Frame(self.calc_frame, bg=self.colors['white'])
        buttons_container.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)
        
        # إطار الأزرار مع تأثيرات
        buttons_frame = tk.Frame(buttons_container, bg=self.colors['white'], relief="solid", bd=1)
        buttons_frame.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
        
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
                    btn = self.create_calc_button(
                        buttons_frame, btn_text, 'number',
                        lambda t=btn_text: self.on_button_click(t)
                    )
                    btn.grid(row=i, column=j, columnspan=2, sticky="nsew", padx=2, pady=2)
                elif i == 4 and j == 1:  # تخطي النقطة لأن الصفر يأخذ مكانين
                    continue
                elif i == 4 and j == 2:  # النقطة
                    btn = self.create_calc_button(
                        buttons_frame, btn_text, 'number',
                        lambda t=btn_text: self.on_button_click(t)
                    )
                    btn.grid(row=i, column=j, sticky="nsew", padx=2, pady=2)
                elif i == 4 and j == 3:  # زر يساوي
                    btn = self.create_calc_button(
                        buttons_frame, btn_text, 'equals',
                        lambda t=btn_text: self.on_button_click(t)
                    )
                    btn.grid(row=i, column=j, sticky="nsew", padx=2, pady=2)
                elif btn_text == 'C':  # زر المسح
                    btn = self.create_calc_button(
                        buttons_frame, "مسح", 'clear',
                        lambda t=btn_text: self.on_button_click(t)
                    )
                    btn.grid(row=i, column=j, sticky="nsew", padx=2, pady=2)
                elif btn_text == '←':  # زر الحذف
                    btn = self.create_calc_button(
                        buttons_frame, btn_text, 'backspace',
                        lambda t=btn_text: self.on_button_click(t)
                    )
                    btn.grid(row=i, column=j, sticky="nsew", padx=2, pady=2)
                elif btn_text in ['+', '-', '*', '/', '%']:  # أزرار العمليات
                    display_text = {'*': '×', '/': '÷'}.get(btn_text, btn_text)
                    btn = self.create_calc_button(
                        buttons_frame, display_text, 'operator',
                        lambda t=btn_text: self.on_button_click(t)
                    )
                    btn.grid(row=i, column=j, sticky="nsew", padx=2, pady=2)
                else:  # أزرار الأرقام
                    btn = self.create_calc_button(
                        buttons_frame, btn_text, 'number',
                        lambda t=btn_text: self.on_button_click(t)
                    )
                    btn.grid(row=i, column=j, sticky="nsew", padx=2, pady=2)
        
        # تكوين الشبكة
        for i in range(5):
            buttons_frame.grid_rowconfigure(i, weight=1)
        for j in range(4):
            buttons_frame.grid_columnconfigure(j, weight=1)
            
    def create_calc_button(self, parent, text, button_type, command):
        """إنشاء زر حاسبة محسن"""
        # تحديد الألوان حسب نوع الزر
        color_map = {
            'number': {
                'bg': self.colors['gray_100'],
                'fg': self.colors['gray_900'],
                'active_bg': self.colors['gray_200'],
                'active_fg': self.colors['gray_900']
            },
            'operator': {
                'bg': self.colors['primary'],
                'fg': self.colors['white'],
                'active_bg': self.colors['secondary'],
                'active_fg': self.colors['white']
            },
            'equals': {
                'bg': self.colors['success'],
                'fg': self.colors['white'],
                'active_bg': '#059669',
                'active_fg': self.colors['white']
            },
            'clear': {
                'bg': self.colors['danger'],
                'fg': self.colors['white'],
                'active_bg': '#dc2626',
                'active_fg': self.colors['white']
            },
            'backspace': {
                'bg': self.colors['warning'],
                'fg': self.colors['white'],
                'active_bg': '#d97706',
                'active_fg': self.colors['white']
            }
        }
        
        colors = color_map.get(button_type, color_map['number'])
        
        btn = tk.Button(
            parent,
            text=text,
            font=self.fonts['button'],
            command=command,
            bg=colors['bg'],
            fg=colors['fg'],
            activebackground=colors['active_bg'],
            activeforeground=colors['active_fg'],
            relief="flat",
            bd=0,
            cursor="hand2"
        )
        
        # إضافة تأثيرات hover
        def on_enter(e):
            btn.config(bg=colors['active_bg'])
            self.status_var.set(f"تم الضغط على: {text}")
            
        def on_leave(e):
            btn.config(bg=colors['bg'])
            self.status_var.set("جاهز للاستخدام")
            
        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)
        
        return btn
            
    def create_history_section(self):
        """إنشاء قسم سجل العمليات المحسن"""
        history_container = tk.Frame(self.calc_frame, bg=self.colors['white'])
        history_container.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)
        
        # إطار السجل مع تأثيرات
        history_frame = tk.Frame(history_container, bg=self.colors['white'], relief="solid", bd=1)
        history_frame.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
        
        # عنوان السجل المحسن
        history_header = tk.Frame(history_frame, bg=self.colors['gray_50'], pady=8)
        history_header.pack(fill=tk.X)
        
        # عنوان مع أيقونة
        title_frame = tk.Frame(history_header, bg=self.colors['gray_50'])
        title_frame.pack(side=tk.LEFT, padx=10)
        
        tk.Label(
            title_frame,
            text=f"{self.icons['chart']} السجل",
            font=self.fonts['arabic_bold'],
            bg=self.colors['gray_50'],
            fg=self.colors['gray_700']
        ).pack(side=tk.LEFT)
        
        # زر المسح المحسن
        clear_btn = tk.Button(
            history_header,
            text=f"{self.icons['clear']} مسح السجل",
            font=self.fonts['small'],
            command=self.clear_history,
            bg=self.colors['danger'],
            fg=self.colors['white'],
            activebackground='#dc2626',
            activeforeground=self.colors['white'],
            relief="flat",
            bd=0,
            cursor="hand2"
        )
        clear_btn.pack(side=tk.RIGHT, padx=10)
        
        # إضافة تأثيرات hover للزر
        def on_clear_enter(e):
            clear_btn.config(bg='#dc2626')
            
        def on_clear_leave(e):
            clear_btn.config(bg=self.colors['danger'])
            
        clear_btn.bind("<Enter>", on_clear_enter)
        clear_btn.bind("<Leave>", on_clear_leave)
        
        # قائمة السجل المحسنة
        list_frame = tk.Frame(history_frame, bg=self.colors['white'])
        list_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Scrollbar
        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.history_listbox = tk.Listbox(
            list_frame,
            font=self.fonts['arabic'],
            height=6,
            bg=self.colors['gray_50'],
            fg=self.colors['gray_900'],
            selectbackground=self.colors['primary'],
            selectforeground=self.colors['white'],
            relief="flat",
            bd=0,
            yscrollcommand=scrollbar.set
        )
        self.history_listbox.pack(fill=tk.BOTH, expand=True)
        self.history_listbox.bind('<Double-1>', self.on_history_select)
        
        scrollbar.config(command=self.history_listbox.yview)
        
        # تحديث السجل
        self.update_history_display()
        
    def update_time(self):
        """تحديث الوقت في شريط الحالة"""
        current_time = datetime.now().strftime("%H:%M:%S")
        current_date = datetime.now().strftime("%Y-%m-%d")
        self.time_var.set(f"📅 {current_date} ⏰ {current_time}")
        self.root.after(1000, self.update_time)  # تحديث كل ثانية
        
    def setup_inventory_tab(self):
        """إعداد تبويب جرد الكاش المحسن"""
        main_frame = tk.Frame(self.inventory_frame, bg=self.colors['white'])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # عنوان القسم المحسن
        title_frame = tk.Frame(main_frame, bg=self.colors['gray_50'], pady=15)
        title_frame.pack(fill=tk.X, pady=(0, 15))
        
        title_label = tk.Label(
            title_frame,
            text=f"{self.icons['inventory']} جرد الكاش",
            font=self.fonts['large'],
            bg=self.colors['gray_50'],
            fg=self.colors['gray_800']
        )
        title_label.pack()
        
        subtitle_label = tk.Label(
            title_frame,
            text="أدخل عدد الأوراق النقدية لكل فئة",
            font=self.fonts['subtitle'],
            bg=self.colors['gray_50'],
            fg=self.colors['gray_600']
        )
        subtitle_label.pack(pady=(5, 0))
        
        # فئات النقود المحسنة
        self.denominations = [200, 100, 50, 20, 10, 5]
        self.denomination_entries = {}
        
        # إطار الفئات
        denominations_frame = tk.Frame(main_frame, bg=self.colors['white'])
        denominations_frame.pack(fill=tk.X, pady=10)
        
        for i, denom in enumerate(self.denominations):
            # إطار كل فئة
            denom_frame = tk.Frame(denominations_frame, bg=self.colors['gray_50'], relief="solid", bd=1)
            denom_frame.pack(fill=tk.X, pady=3, padx=5)
            
            # إطار داخلي
            inner_frame = tk.Frame(denom_frame, bg=self.colors['gray_50'], padx=15, pady=10)
            inner_frame.pack(fill=tk.X)
            
            # اللون المميز لكل فئة
            color_map = {
                200: self.colors['danger'],
                100: self.colors['success'],
                50: self.colors['warning'],
                20: self.colors['info'],
                10: self.colors['primary'],
                5: self.colors['gray_600']
            }
            
            # أيقونة الفئة
            icon_label = tk.Label(
                inner_frame,
                text=self.icons['money'],
                font=self.fonts['arabic'],
                bg=self.colors['gray_50'],
                fg=color_map.get(denom, self.colors['gray_600'])
            )
            icon_label.pack(side=tk.LEFT)
            
            # تسمية الفئة
            tk.Label(
                inner_frame,
                text=f"{denom} جنيه",
                font=self.fonts['arabic_bold'],
                bg=self.colors['gray_50'],
                fg=self.colors['gray_800'],
                width=12
            ).pack(side=tk.LEFT, padx=10)
            
            # حقل الإدخال
            entry = tk.Entry(
                inner_frame,
                font=self.fonts['arabic'],
                width=12,
                justify="center",
                bg=self.colors['white'],
                fg=self.colors['gray_900'],
                relief="solid",
                bd=1,
                highlightthickness=1,
                highlightcolor=color_map.get(denom, self.colors['primary'])
            )
            entry.pack(side=tk.LEFT, padx=10)
            entry.bind('<KeyRelease>', self.calculate_inventory_total)
            entry.bind('<FocusIn>', lambda e, d=denom: self.status_var.set(f"إدخال عدد أوراق فئة {d} جنيه"))
            entry.bind('<FocusOut>', lambda e: self.status_var.set("جاهز للاستخدام"))
            self.denomination_entries[denom] = entry
            
            # عرض القيمة الجزئية
            partial_var = tk.StringVar(value="0.00 جنيه")
            partial_label = tk.Label(
                inner_frame,
                textvariable=partial_var,
                font=self.fonts['arabic'],
                bg=self.colors['gray_50'],
                fg=color_map.get(denom, self.colors['gray_600'])
            )
            partial_label.pack(side=tk.RIGHT, padx=10)
            
            # حفظ متغير القيمة الجزئية
            entry.partial_var = partial_var
            entry.denom = denom
        
        # إجمالي الجرد المحسن
        total_frame = tk.Frame(main_frame, bg=self.colors['primary'], relief="solid", bd=2)
        total_frame.pack(fill=tk.X, pady=20)
        
        # إطار داخلي للإجمالي
        total_inner = tk.Frame(total_frame, bg=self.colors['primary'], padx=20, pady=15)
        total_inner.pack(fill=tk.X)
        
        # أيقونة الإجمالي
        tk.Label(
            total_inner,
            text="💰",
            font=self.fonts['large'],
            bg=self.colors['primary'],
            fg=self.colors['white']
        ).pack(side=tk.LEFT)
        
        tk.Label(
            total_inner,
            text="الإجمالي:",
            font=self.fonts['large'],
            bg=self.colors['primary'],
            fg=self.colors['white']
        ).pack(side=tk.LEFT, padx=10)
        
        self.inventory_total_var = tk.StringVar(value="0.00 جنيه")
        tk.Label(
            total_inner,
            textvariable=self.inventory_total_var,
            font=("Arial", 18, "bold"),
            bg=self.colors['primary'],
            fg=self.colors['white']
        ).pack(side=tk.RIGHT, padx=10)
        
        # أزرار التحقق المحسنة
        buttons_frame = tk.Frame(main_frame, bg=self.colors['white'])
        buttons_frame.pack(pady=20)
        
        tk.Label(
            buttons_frame,
            text="هل الجرد صحيح؟",
            font=self.fonts['arabic_bold'],
            bg=self.colors['white'],
            fg=self.colors['gray_800']
        ).pack(pady=10)
        
        btn_frame = tk.Frame(buttons_frame, bg=self.colors['white'])
        btn_frame.pack()
        
        # زر نعم
        yes_btn = tk.Button(
            btn_frame,
            text=f"{self.icons['check']} نعم",
            font=self.fonts['button'],
            bg=self.colors['success'],
            fg=self.colors['white'],
            activebackground='#059669',
            activeforeground=self.colors['white'],
            command=self.confirm_inventory,
            relief="flat",
            bd=0,
            cursor="hand2",
            padx=20,
            pady=10
        )
        yes_btn.pack(side=tk.LEFT, padx=10)
        
        # زر لا
        no_btn = tk.Button(
            btn_frame,
            text=f"{self.icons['warning']} لا",
            font=self.fonts['button'],
            bg=self.colors['danger'],
            fg=self.colors['white'],
            activebackground='#dc2626',
            activeforeground=self.colors['white'],
            command=self.show_discrepancy,
            relief="flat",
            bd=0,
            cursor="hand2",
            padx=20,
            pady=10
        )
        no_btn.pack(side=tk.LEFT, padx=10)
        
        # إضافة تأثيرات hover
        def on_yes_enter(e):
            yes_btn.config(bg='#059669')
            
        def on_yes_leave(e):
            yes_btn.config(bg=self.colors['success'])
            
        def on_no_enter(e):
            no_btn.config(bg='#dc2626')
            
        def on_no_leave(e):
            no_btn.config(bg=self.colors['danger'])
            
        yes_btn.bind("<Enter>", on_yes_enter)
        yes_btn.bind("<Leave>", on_yes_leave)
        no_btn.bind("<Enter>", on_no_enter)
        no_btn.bind("<Leave>", on_no_leave)
        
        # قسم الفرق
        self.discrepancy_frame = tk.Frame(main_frame, bg="#fff3cd", relief="solid", bd=2)
        
        tk.Label(
            self.discrepancy_frame,
            text="فحص الفرق",
            font=self.fonts['arabic_bold'],
            bg="#fff3cd"
        ).pack(pady=10)
        
        input_frame = tk.Frame(self.discrepancy_frame, bg="#fff3cd")
        input_frame.pack(pady=10)
        
        tk.Label(
            input_frame,
            text="المبلغ المتوقع:",
            font=self.fonts['arabic'],
            bg="#fff3cd"
        ).pack(side=tk.LEFT)
        
        self.expected_entry = tk.Entry(
            input_frame,
            font=self.fonts['arabic'],
            width=15
        )
        self.expected_entry.pack(side=tk.LEFT, padx=10)
        self.expected_entry.bind('<KeyRelease>', self.calculate_difference)
        
        self.difference_var = tk.StringVar(value="الفرق: 0.00 جنيه")
        tk.Label(
            self.discrepancy_frame,
            textvariable=self.difference_var,
            font=self.fonts['arabic_bold'],
            bg="#fff3cd"
        ).pack(pady=10)
        
    def setup_formulas_tab(self):
        """إعداد تبويب المعادلات المحسن"""
        main_frame = tk.Frame(self.formulas_frame, bg=self.colors['white'])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # العنوان الرئيسي
        title_frame = tk.Frame(main_frame, bg=self.colors['gray_50'], pady=10)
        title_frame.pack(fill=tk.X, pady=(0, 15))
        
        title_label = tk.Label(
            title_frame,
            text=f"{self.icons['formulas']} معادلات التجارة",
            font=self.fonts['large'],
            bg=self.colors['gray_50'],
            fg=self.colors['gray_800']
        )
        title_label.pack()
        
        # قسم حاسبة الجملة المحسن
        wholesale_frame = tk.Frame(main_frame, bg=self.colors['white'], relief="solid", bd=2)
        wholesale_frame.pack(fill=tk.X, pady=10, padx=5)
        
        # شريط العنوان الملون
        wholesale_header = tk.Frame(wholesale_frame, bg=self.colors['success'], height=40)
        wholesale_header.pack(fill=tk.X)
        wholesale_header.pack_propagate(False)
        
        tk.Label(
            wholesale_header,
            text=f"💰 حاسبة الجملة",
            font=self.fonts['arabic_bold'],
            bg=self.colors['success'],
            fg=self.colors['white']
        ).pack(pady=8)
        
        # محتوى القسم
        wholesale_content = tk.Frame(wholesale_frame, bg=self.colors['white'], padx=20, pady=15)
        wholesale_content.pack(fill=tk.X)
        
        # سعر القطعة
        price_frame = tk.Frame(wholesale_content, bg=self.colors['white'])
        price_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(
            price_frame,
            text="💵 سعر القطعة:",
            font=self.fonts['arabic'],
            bg=self.colors['white'],
            fg=self.colors['gray_700']
        ).pack(anchor="w", pady=5)
        
        self.piece_price_entry = tk.Entry(
            price_frame,
            font=self.fonts['arabic'],
            width=25,
            bg=self.colors['gray_50'],
            fg=self.colors['gray_900'],
            relief="solid",
            bd=1,
            highlightthickness=1,
            highlightcolor=self.colors['success']
        )
        self.piece_price_entry.pack(fill=tk.X, pady=5)
        
        # نسبة الخصم
        discount_frame = tk.Frame(wholesale_content, bg=self.colors['white'])
        discount_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(
            discount_frame,
            text="🏷️ نسبة الخصم (%):",
            font=self.fonts['arabic'],
            bg=self.colors['white'],
            fg=self.colors['gray_700']
        ).pack(anchor="w", pady=5)
        
        self.discount_entry = tk.Entry(
            discount_frame,
            font=self.fonts['arabic'],
            width=25,
            bg=self.colors['gray_50'],
            fg=self.colors['gray_900'],
            relief="solid",
            bd=1,
            highlightthickness=1,
            highlightcolor=self.colors['success']
        )
        self.discount_entry.pack(fill=tk.X, pady=5)
        self.discount_entry.insert(0, "0")
        
        # زر الحساب
        calculate_btn = tk.Button(
            wholesale_content,
            text="📊 احسب سعر الجملة",
            font=self.fonts['button'],
            bg=self.colors['success'],
            fg=self.colors['white'],
            activebackground='#059669',
            activeforeground=self.colors['white'],
            command=self.calculate_wholesale,
            relief="flat",
            bd=0,
            cursor="hand2",
            pady=10
        )
        calculate_btn.pack(pady=15, fill=tk.X)
        
        # النتيجة
        self.wholesale_result_var = tk.StringVar(value="")
        result_frame = tk.Frame(wholesale_content, bg=self.colors['gray_50'], relief="solid", bd=1)
        result_frame.pack(fill=tk.X, pady=10)
        
        self.wholesale_result_label = tk.Label(
            result_frame,
            textvariable=self.wholesale_result_var,
            font=self.fonts['large'],
            bg=self.colors['gray_50'],
            fg=self.colors['success'],
            pady=15
        )
        self.wholesale_result_label.pack()
        
        # قسم محول القطع المحسن
        conversion_frame = tk.Frame(main_frame, bg=self.colors['white'], relief="solid", bd=2)
        conversion_frame.pack(fill=tk.X, pady=10, padx=5)
        
        # شريط العنوان الملون
        conversion_header = tk.Frame(conversion_frame, bg=self.colors['info'], height=40)
        conversion_header.pack(fill=tk.X)
        conversion_header.pack_propagate(False)
        
        tk.Label(
            conversion_header,
            text=f"📦 محول القطع",
            font=self.fonts['arabic_bold'],
            bg=self.colors['info'],
            fg=self.colors['white']
        ).pack(pady=8)
        
        # محتوى القسم
        conversion_content = tk.Frame(conversion_frame, bg=self.colors['white'], padx=20, pady=15)
        conversion_content.pack(fill=tk.X)
        
        # عدد القطع
        pieces_frame = tk.Frame(conversion_content, bg=self.colors['white'])
        pieces_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(
            pieces_frame,
            text="🔢 عدد القطع:",
            font=self.fonts['arabic'],
            bg=self.colors['white'],
            fg=self.colors['gray_700']
        ).pack(anchor="w", pady=5)
        
        self.pieces_entry = tk.Entry(
            pieces_frame,
            font=self.fonts['arabic'],
            width=25,
            bg=self.colors['gray_50'],
            fg=self.colors['gray_900'],
            relief="solid",
            bd=1,
            highlightthickness=1,
            highlightcolor=self.colors['info']
        )
        self.pieces_entry.pack(fill=tk.X, pady=5)
        
        # الوحدة
        unit_frame = tk.Frame(conversion_content, bg=self.colors['white'])
        unit_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(
            unit_frame,
            text="📋 الوحدة:",
            font=self.fonts['arabic'],
            bg=self.colors['white'],
            fg=self.colors['gray_700']
        ).pack(anchor="w", pady=5)
        
        self.unit_var = tk.StringVar(value="دستة (12 قطعة)")
        unit_combo = ttk.Combobox(
            unit_frame,
            textvariable=self.unit_var,
            values=["دستة (12 قطعة)", "نص دستة (6 قطع)"],
            font=self.fonts['arabic'],
            state="readonly",
            width=23
        )
        unit_combo.pack(fill=tk.X, pady=5)
        
        # زر التحويل
        convert_btn = tk.Button(
            conversion_content,
            text="🔄 تحويل",
            font=self.fonts['button'],
            bg=self.colors['info'],
            fg=self.colors['white'],
            activebackground='#0284c7',
            activeforeground=self.colors['white'],
            command=self.convert_pieces,
            relief="flat",
            bd=0,
            cursor="hand2",
            pady=10
        )
        convert_btn.pack(pady=15, fill=tk.X)
        
        # النتيجة
        self.conversion_result_var = tk.StringVar(value="")
        result_frame2 = tk.Frame(conversion_content, bg=self.colors['gray_50'], relief="solid", bd=1)
        result_frame2.pack(fill=tk.X, pady=10)
        
        self.conversion_result_label = tk.Label(
            result_frame2,
            textvariable=self.conversion_result_var,
            font=self.fonts['large'],
            bg=self.colors['gray_50'],
            fg=self.colors['info'],
            pady=15
        )
        self.conversion_result_label.pack()
        
    def setup_roi_tab(self):
        """إعداد تبويب ROI التسويق المحسن"""
        main_frame = tk.Frame(self.roi_frame, bg=self.colors['white'])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # العنوان الرئيسي
        title_frame = tk.Frame(main_frame, bg=self.colors['primary'], pady=15)
        title_frame.pack(fill=tk.X, pady=(0, 15))
        
        title_label = tk.Label(
            title_frame,
            text=f"{self.icons['roi']} حاسبة ROI التسويق",
            font=self.fonts['large'],
            bg=self.colors['primary'],
            fg=self.colors['white']
        )
        title_label.pack()
        
        subtitle_label = tk.Label(
            title_frame,
            text="احسب العائد على الاستثمار في الحملات الإعلانية",
            font=self.fonts['subtitle'],
            bg=self.colors['primary'],
            fg=self.colors['gray_200']
        )
        subtitle_label.pack(pady=(5, 0))
        
        # إطار المدخلات
        inputs_frame = tk.Frame(main_frame, bg=self.colors['white'], relief="solid", bd=2)
        inputs_frame.pack(fill=tk.X, pady=10)
        
        inputs_content = tk.Frame(inputs_frame, bg=self.colors['white'], padx=20, pady=15)
        inputs_content.pack(fill=tk.X)
        
        # تكلفة الحملة
        cost_frame = tk.Frame(inputs_content, bg=self.colors['white'])
        cost_frame.pack(fill=tk.X, pady=8)
        
        tk.Label(
            cost_frame,
            text="💰 تكلفة الحملة الإعلانية:",
            font=self.fonts['arabic'],
            bg=self.colors['white'],
            fg=self.colors['gray_700']
        ).pack(anchor="w", pady=5)
        
        self.campaign_cost_entry = tk.Entry(
            cost_frame,
            font=self.fonts['arabic'],
            width=25,
            bg=self.colors['gray_50'],
            fg=self.colors['gray_900'],
            relief="solid",
            bd=1,
            highlightthickness=1,
            highlightcolor=self.colors['primary']
        )
        self.campaign_cost_entry.pack(fill=tk.X, pady=5)
        
        # سعر البيع
        selling_frame = tk.Frame(inputs_content, bg=self.colors['white'])
        selling_frame.pack(fill=tk.X, pady=8)
        
        tk.Label(
            selling_frame,
            text="🏷️ سعر البيع للقطعة:",
            font=self.fonts['arabic'],
            bg=self.colors['white'],
            fg=self.colors['gray_700']
        ).pack(anchor="w", pady=5)
        
        self.selling_price_entry = tk.Entry(
            selling_frame,
            font=self.fonts['arabic'],
            width=25,
            bg=self.colors['gray_50'],
            fg=self.colors['gray_900'],
            relief="solid",
            bd=1,
            highlightthickness=1,
            highlightcolor=self.colors['primary']
        )
        self.selling_price_entry.pack(fill=tk.X, pady=5)
        
        # تكلفة القطعة
        cost_piece_frame = tk.Frame(inputs_content, bg=self.colors['white'])
        cost_piece_frame.pack(fill=tk.X, pady=8)
        
        tk.Label(
            cost_piece_frame,
            text="📦 تكلفة القطعة:",
            font=self.fonts['arabic'],
            bg=self.colors['white'],
            fg=self.colors['gray_700']
        ).pack(anchor="w", pady=5)
        
        self.cost_price_entry = tk.Entry(
            cost_piece_frame,
            font=self.fonts['arabic'],
            width=25,
            bg=self.colors['gray_50'],
            fg=self.colors['gray_900'],
            relief="solid",
            bd=1,
            highlightthickness=1,
            highlightcolor=self.colors['primary']
        )
        self.cost_price_entry.pack(fill=tk.X, pady=5)
        
        # زر الحساب
        calculate_roi_btn = tk.Button(
            inputs_content,
            text="📈 احسب ROI",
            font=self.fonts['button'],
            bg=self.colors['primary'],
            fg=self.colors['white'],
            activebackground=self.colors['secondary'],
            activeforeground=self.colors['white'],
            command=self.calculate_roi,
            relief="flat",
            bd=0,
            cursor="hand2",
            pady=12
        )
        calculate_roi_btn.pack(pady=20, fill=tk.X)
        
        # النتائج
        self.roi_results_frame = tk.Frame(main_frame, bg=self.colors['white'])
        self.roi_results_frame.pack(fill=tk.X, pady=10)
        
        # إضافة تأثيرات hover للأزرار
        self.add_button_hover_effects(calculate_roi_btn, self.colors['primary'], self.colors['secondary'])
        
    def setup_shift_tab(self):
        """إعداد تبويب تقفيل الوردية"""
        main_frame = tk.Frame(self.shift_frame, bg="white")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # عنوان القسم
        title_label = tk.Label(
            main_frame,
            text="تقفيل الوردية",
            font=self.fonts['large'],
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
            font=self.fonts['arabic_bold'],
            bg="white",
            fg="#10b981"
        )
        revenue_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        
        # حقول الإيرادات
        tk.Label(revenue_frame, text="الحصالة في بداية الوردية:", font=self.fonts['arabic'], bg="white").pack(anchor="w", padx=10, pady=5)
        self.cash_box_entry = tk.Entry(revenue_frame, font=self.fonts['arabic'], width=15)
        self.cash_box_entry.pack(padx=10, pady=5)
        self.cash_box_entry.insert(0, "0")
        
        tk.Label(revenue_frame, text="مبيعات كاش:", font=self.fonts['arabic'], bg="white").pack(anchor="w", padx=10, pady=5)
        self.cash_sales_entry = tk.Entry(revenue_frame, font=self.fonts['arabic'], width=15)
        self.cash_sales_entry.pack(padx=10, pady=5)
        self.cash_sales_entry.insert(0, "0")
        
        tk.Label(revenue_frame, text="إيرادات أخرى:", font=self.fonts['arabic'], bg="white").pack(anchor="w", padx=10, pady=5)
        self.other_income_entry = tk.Entry(revenue_frame, font=self.fonts['arabic'], width=15)
        self.other_income_entry.pack(padx=10, pady=5)
        self.other_income_entry.insert(0, "0")
        
        # المصروفات
        expense_frame = tk.LabelFrame(
            input_frame,
            text="المصروفات",
            font=self.fonts['arabic_bold'],
            bg="white",
            fg="#ef4444"
        )
        expense_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5)
        
        # حقول المصروفات
        tk.Label(expense_frame, text="مصروفات:", font=self.fonts['arabic'], bg="white").pack(anchor="w", padx=10, pady=5)
        self.expenses_entry = tk.Entry(expense_frame, font=self.fonts['arabic'], width=15)
        self.expenses_entry.pack(padx=10, pady=5)
        self.expenses_entry.insert(0, "0")
        
        tk.Label(expense_frame, text="خصومات:", font=self.fonts['arabic'], bg="white").pack(anchor="w", padx=10, pady=5)
        self.discounts_entry = tk.Entry(expense_frame, font=self.fonts['arabic'], width=15)
        self.discounts_entry.pack(padx=10, pady=5)
        self.discounts_entry.insert(0, "0")
        
        tk.Label(expense_frame, text="مدفوعات فيزا:", font=self.fonts['arabic'], bg="white").pack(anchor="w", padx=10, pady=5)
        self.visa_payments_entry = tk.Entry(expense_frame, font=self.fonts['arabic'], width=15)
        self.visa_payments_entry.pack(padx=10, pady=5)
        self.visa_payments_entry.insert(0, "0")
        
        # زر الحساب
        tk.Button(
            main_frame,
            text="احسب النتائج",
            font=self.fonts['button'],
            bg="#2563eb",
            fg="white",
            command=self.calculate_shift
        ).pack(pady=20)
        
        # النتائج
        self.shift_results_frame = tk.Frame(main_frame, bg="white")
        self.shift_results_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
    # دوال جرد الكاش
    def calculate_inventory_total(self, event=None):
        """حساب إجمالي الجرد مع القيم الجزئية"""
        total = 0
        for denom, entry in self.denomination_entries.items():
            try:
                count = int(entry.get() or 0)
                partial_value = count * denom
                total += partial_value
                
                # تحديث القيمة الجزئية
                if hasattr(entry, 'partial_var'):
                    entry.partial_var.set(f"{partial_value:.2f} جنيه")
            except ValueError:
                if hasattr(entry, 'partial_var'):
                    entry.partial_var.set("0.00 جنيه")
        
        self.inventory_total_var.set(f"{total:.2f} جنيه")
        
        # تحديث شريط الحالة
        if total > 0:
            self.status_var.set(f"إجمالي الجرد: {total:.2f} جنيه")
        
    def confirm_inventory(self):
        """تأكيد صحة الجرد"""
        total = self.inventory_total_var.get()
        messagebox.showinfo("تأكيد الجرد", f"✅ رائع! تم تأكيد الجرد بمبلغ {total}")
        self.discrepancy_frame.pack_forget()
        self.status_var.set("تم تأكيد الجرد بنجاح")
        
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
                messagebox.showerror("خطأ في البيانات", "⚠️ يجب إدخال سعر صحيح للقطعة")
                return
                
            if discount < 0 or discount > 100:
                messagebox.showerror("خطأ في البيانات", "⚠️ نسبة الخصم يجب أن تكون بين 0 و 100")
                return
                
            # تطبيق معادلة الجملة: (سعر القطعة * 10 * (1 - الخصم/100)) / 12
            wholesale_price = (price * 10 * (1 - discount / 100)) / 12
            self.wholesale_result_var.set(f"💰 سعر الجملة: {wholesale_price:.2f} جنيه")
            self.status_var.set(f"تم حساب سعر الجملة: {wholesale_price:.2f} جنيه")
            
        except ValueError:
            messagebox.showerror("خطأ في الإدخال", "⚠️ يجب إدخال أرقام صحيحة فقط")
            
    def convert_pieces(self):
        """تحويل القطع"""
        try:
            pieces = int(self.pieces_entry.get())
            unit_text = self.unit_var.get()
            
            if pieces <= 0:
                messagebox.showerror("خطأ في البيانات", "⚠️ يجب إدخال عدد صحيح من القطع")
                return
                
            unit_size = 12 if "دستة" in unit_text else 6
            unit_name = "دستة" if unit_size == 12 else "نص دستة"
            
            result = pieces / unit_size
            self.conversion_result_var.set(f"📊 النتيجة: {result:.2f} {unit_name}")
            self.status_var.set(f"تم تحويل {pieces} قطعة إلى {result:.2f} {unit_name}")
            
        except ValueError:
            messagebox.showerror("خطأ في الإدخال", "⚠️ يجب إدخال رقم صحيح فقط")
            
    # دوال ROI التسويق
    def calculate_roi(self):
        """حساب ROI التسويق"""
        try:
            campaign_cost = float(self.campaign_cost_entry.get())
            selling_price = float(self.selling_price_entry.get())
            cost_price = float(self.cost_price_entry.get())
            
            if campaign_cost <= 0:
                messagebox.showerror("خطأ في البيانات", "⚠️ يجب إدخال تكلفة صحيحة للحملة الإعلانية")
                return
            if selling_price <= 0:
                messagebox.showerror("خطأ في البيانات", "⚠️ يجب إدخال سعر بيع صحيح للقطعة")
                return
            if cost_price <= 0:
                messagebox.showerror("خطأ في البيانات", "⚠️ يجب إدخال تكلفة صحيحة للقطعة")
                return
            if selling_price <= cost_price:
                messagebox.showerror("خطأ في البيانات", "⚠️ سعر البيع يجب أن يكون أعلى من التكلفة")
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
            messagebox.showerror("خطأ في الإدخال", "⚠️ يجب إدخال أرقام صحيحة فقط")
            
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
            messagebox.showerror("خطأ في الإدخال", "⚠️ يجب إدخال أرقام صحيحة فقط")
            
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
                messagebox.showinfo("تم الحفظ", "💾 تم حفظ التقرير بنجاح!")
                self.status_var.set("تم حفظ التقرير بنجاح")
        except Exception as e:
            messagebox.showerror("خطأ في الحفظ", f"⚠️ حدث خطأ أثناء الحفظ: {str(e)}")
            
    def clear_shift_data(self):
        """مسح بيانات الوردية"""
        if messagebox.askyesno("تأكيد المسح", "🗑️ هل أنت متأكد من مسح جميع البيانات؟"):
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
                
            self.status_var.set("تم مسح جميع البيانات")
        
    def on_button_click(self, button_text):
        """معالجة النقر على الأزرار"""
        # تشغيل صوت النقر
        self.play_click_sound()
        
        if button_text == 'C':
            self.clear_display()
            self.status_var.set("✨ تم مسح الشاشة")
        elif button_text == '←':
            self.backspace()
            self.status_var.set("⬅️ تم حذف آخر رقم")
        elif button_text == '=':
            self.calculate()
        else:
            self.add_to_display(button_text)
            self.status_var.set(f"✅ تم إدخال: {button_text}")
            
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
            self.status_var.set("تم حساب العملية بنجاح")
            
        except Exception as e:
            self.display_var.set("خطأ")
            self.expression_var.set("")
            self.status_var.set("حدث خطأ في الحساب")
            
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
        if messagebox.askyesno("تأكيد المسح", "🗑️ هل أنت متأكد من مسح جميع العمليات؟"):
            self.history = []
            self.save_history()
            self.update_history_display()
            self.status_var.set("تم مسح السجل بنجاح")
        
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