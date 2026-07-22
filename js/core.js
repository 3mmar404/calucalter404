// core.js — Theme controller, tabs, and global helpers for SmartCalc Pro
//
// Dark-mode fix: the `.dark` class is applied to BOTH <html> and <body>, and a
// single click handler is the only source of truth. The previous build had a
// second, conflicting handler inlined in index.html (it used a different
// localStorage key and toggled the class differently), so the two handlers
// fought each other on every click — that was the "toggle doesn't work" bug.

document.addEventListener('DOMContentLoaded', () => {
  const THEME_KEY = 'theme';
  const themeToggle = document.getElementById('themeToggle');

  const applyTheme = (theme) => {
    const isDark = theme === 'dark';
    document.documentElement.classList.toggle('dark', isDark);
    document.body.classList.toggle('dark', isDark);
    try { localStorage.setItem(THEME_KEY, theme); } catch (e) {}
  };

  // Initialise from the saved preference, otherwise from the OS preference.
  let saved = null;
  try { saved = localStorage.getItem(THEME_KEY); } catch (e) {}
  const prefersDark = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
  applyTheme(saved || (prefersDark ? 'dark' : 'light'));

  if (themeToggle) {
    themeToggle.addEventListener('click', () => {
      const isDark = document.documentElement.classList.contains('dark');
      applyTheme(isDark ? 'light' : 'dark');
    });
  }

  // Tabs
  const tabBtns = document.querySelectorAll('.tab-btn');
  const tabPanes = document.querySelectorAll('.tab-pane');
  tabBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      const tabId = btn.dataset.tab;
      tabBtns.forEach(b => b.classList.remove('active', 'text-primary', 'border-primary'));
      btn.classList.add('active', 'text-primary', 'border-primary');
      tabPanes.forEach(p => p.classList.toggle('active', p.id === tabId));
    });
  });

  // Global helpers (defined first because core.js loads before the other modules)
  window.$ = (selector) => document.querySelector(selector);
  window.$$ = (selector) => document.querySelectorAll(selector);
});
