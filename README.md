<div align="center">

# SmartCalc Pro

**A bilingual, offline-first business toolkit — calculator, cash count, formulas, marketing ROI & shift closeout.**

حاسبة الأعمال الذكية — أداة متكاملة تعمل بدون إنترنت: حاسبة، جرد كاش، معادلات، ROI تسويقي، وتقفيل وردية.

`HTML` · `Tailwind CSS` · `Vanilla JS` · `Python (Tkinter)` · Arabic 🇪🇬 / English 🇬🇧 · Light & Dark

</div>

---

## ✨ Overview

SmartCalc Pro is a lightweight web app (with an optional Windows desktop edition) built for small retail and shop operations. It runs entirely in the browser — **no backend, no build step, no internet required.** Everything is saved locally in your browser.

It ships in **two languages** (Arabic & English) with a one-click switcher that also flips the page direction (RTL ⇄ LTR), and a **dark / light theme** that remembers your choice.

## 🧰 Features

| Tool | What it does |
|------|--------------|
| 🧮 **Calculator** | Standard calculator with keyboard support and a saved history (last 20 operations). |
| 💵 **Cash Count** | Count cash by denomination, get a live total, and check it against an expected amount. |
| 📐 **Formulas** | Wholesale price calculator and a pieces ⇄ dozen unit converter. |
| 📈 **Marketing ROI** | Work out required sales, required units, and profit margin for an ad campaign. |
| 🧾 **Shift Closeout** | Tally revenue vs. expenses, compute the net, the amount carried over, and what stays in the drawer — with print & save-to-JSON. |

**Also included**
- 🌐 Arabic / English switch (with automatic RTL/LTR) — preference saved locally.
- 🌓 Dark / light mode — follows your system by default, remembers your choice.
- 💾 Offline-first: history, cash totals and the last shift report persist in `localStorage`.
- ♻️ One-tap reset per tab.

## 🚀 Getting Started (Web)

No installation needed:

1. Download or clone the repository.
2. Open `index.html` in any modern browser.
3. Use the language button (**EN / ع**) and the theme button (🌙 / ☀️) in the header.

```bash
git clone https://github.com/3mmar404/calucalter404.git
cd calucalter404
# then just open index.html
```

> The only external dependencies are Tailwind CSS and Font Awesome, loaded via CDN. With an internet connection on first load they are cached; the app logic itself is fully offline.

## 🖥️ Desktop Edition (Windows)

A standalone Tkinter calculator is included. See **[README_DESKTOP.md](README_DESKTOP.md)** for full details.

```bash
# Run directly (requires Python 3.6+)
python calculator_app.py

# Or build a single .exe (uses PyInstaller)
python build_exe.py        # output: dist/SmartCalcPro.exe
```

## 🗂️ Project Structure

```
calucalter404/
├── index.html              # Web app shell (all tabs)
├── css/
│   └── style.css           # Styles + light/dark theming
├── js/
│   ├── i18n.js             # Bilingual dictionary + language switching
│   ├── core.js             # Theme controller (dark/light) + tabs + helpers
│   ├── calculator.js       # Calculator + history
│   ├── inventory.js        # Cash count
│   ├── formulas.js         # Wholesale + unit converter
│   ├── roi.js              # Marketing ROI
│   ├── shift.js            # Shift closeout report
│   └── reset.js            # Per-tab reset buttons
├── assets/                 # logo.svg, favicon.ico, logo.png
├── calculator_app.py       # Desktop edition (Tkinter)
├── build_exe.py            # PyInstaller build script
├── run_app.bat             # Windows launcher
├── README.md
└── README_DESKTOP.md
```

## 🌍 Adding / editing translations

All UI strings live in one place: `js/i18n.js`, under `translations.ar` and `translations.en`.
To add a string, give it a key in **both** languages, then reference it either:

- in HTML: `<span data-i18n="my_key">...</span>` (also `data-i18n-placeholder`, `data-i18n-html`, `data-i18n-aria`), or
- in JS: `t('my_key')`.

Dynamic panels re-render automatically when the language changes (via a `languagechange` event).

## 🤝 Contributing

Contributions are welcome. Open an issue to discuss a change, or send a pull request. Please keep the app dependency-free (vanilla JS) and add any new UI text to **both** languages in `js/i18n.js`.

## 📄 License

Released under the [MIT License](LICENSE). © 2026 **AMAR** ([@3mmar404](https://github.com/3mmar404)).

---

<div align="center">
Made with care · <strong>BY AMAR</strong>
</div>
