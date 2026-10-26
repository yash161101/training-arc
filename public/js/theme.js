try {
  const t = localStorage.getItem('ta-theme');
  if (t === 'light' || t === 'dark') document.documentElement.dataset.theme = t;
} catch {}
