#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Build script لتحويل التطبيق إلى exe
"""

import subprocess
import sys
import os

def install_requirements():
    """تثبيت المتطلبات"""
    print("🔧 تثبيت المتطلبات...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
        print("✅ تم تثبيت PyInstaller بنجاح")
    except subprocess.CalledProcessError:
        print("❌ فشل في تثبيت PyInstaller")
        return False
    return True

def build_exe():
    """بناء ملف exe"""
    print("🏗️  بناء ملف exe...")
    
    # إنشاء مجلد للإخراج
    output_dir = "dist"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # أوامر PyInstaller
    cmd = [
        "pyinstaller",
        "--onefile",  # ملف واحد
        "--windowed",  # بدون console
        "--name=SmartCalcPro",  # اسم الملف
        "--icon=assets/favicon.ico" if os.path.exists("assets/favicon.ico") else "",
        "--distpath=dist",  # مجلد الإخراج
        "--specpath=build",  # مجلد البناء
        "--add-data=calculator_history.json;." if os.path.exists("calculator_history.json") else "",
        "calculator_app.py"
    ]
    
    # إزالة الخيارات الفارغة
    cmd = [arg for arg in cmd if arg]
    
    try:
        subprocess.check_call(cmd)
        print("✅ تم بناء ملف exe بنجاح!")
        print(f"📁 يمكنك العثور على الملف في: {os.path.abspath('dist/SmartCalcPro.exe')}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ فشل في بناء ملف exe: {e}")
        return False

def main():
    """الدالة الرئيسية"""
    print("🚀 بدء عملية بناء التطبيق...")
    
    if not install_requirements():
        return
    
    if not build_exe():
        return
    
    print("\n🎉 تم الانتهاء من بناء التطبيق بنجاح!")
    print("💡 يمكنك الآن تشغيل SmartCalcPro.exe من مجلد dist")

if __name__ == "__main__":
    main()