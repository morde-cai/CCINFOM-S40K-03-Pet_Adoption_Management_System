// ------------------------------- Dark/Light Theme -------------------------------
// Apply saved theme immediately (this file loads in <head>, so there is no flash).
const saved = localStorage.getItem('theme');
const system = matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
document.documentElement.setAttribute('data-bs-theme', saved || system);

// Show the icon for the mode you would switch TO (moon in light mode, sun in dark mode).
function syncThemeIcon() {
  const icon = document.getElementById('themeIcon');
  if (!icon) return;
  icon.src = document.documentElement.dataset.bsTheme === 'dark' ? icon.dataset.sun : icon.dataset.moon;
}

document.addEventListener('DOMContentLoaded', () => {
  syncThemeIcon();
  document.getElementById('themeToggleBtn').addEventListener('click', () => {
    const html = document.documentElement;
    const next = html.dataset.bsTheme === 'dark' ? 'light' : 'dark';
    html.dataset.bsTheme = next;
    localStorage.setItem('theme', next);
    syncThemeIcon();
    document.dispatchEvent(new CustomEvent('themechange', { detail: next })); // charts can listen to this
  });
});

// ------------------------------- Chart.js helper -------------------------------
// Reads the colors from custom.css so charts match the current theme.
// Usage: const c = themeColors();  ...  document.addEventListener('themechange', () => { ...update chart... });
function themeColors() {
  const css = getComputedStyle(document.documentElement);
  const v = (name) => css.getPropertyValue(name).trim();
  return {
    primary: v('--brand-600'),
    primaryDark: v('--brand-700'),
    tint: v('--brand-100'),
    strong: v('--brand-900'),  // dark teal in light mode, near-white in dark mode
    text: v('--bs-body-color'),
    grid: v('--bs-border-color'),
  };
}
