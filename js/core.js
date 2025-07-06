// core.js - Theme, Tabs, LocalStorage, and global helpers

document.addEventListener('DOMContentLoaded', () => {
  // Theme toggling
  const themeToggle = document.getElementById('themeToggle');
  const applyTheme = (theme) => {
    document.documentElement.classList.toggle('dark', theme === 'dark');
    localStorage.setItem('appTheme', theme);
  };
  if (themeToggle) {
    themeToggle.addEventListener('click', () => {
      applyTheme(!document.documentElement.classList.contains('dark') ? 'dark' : 'light');
    });
    applyTheme(localStorage.getItem('appTheme') || 'light');
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

  // Global helpers
  window.$ = (selector) => document.querySelector(selector);
  window.$$ = (selector) => document.querySelectorAll(selector);
});
