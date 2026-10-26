import { api } from './api.js';

const RAD = Math.PI / 180;
const DAY = 86400000;
let place = null;
let fetchedAt = 0;

try {
  place = JSON.parse(localStorage.getItem('ta-sky') || 'null');
} catch {}

export async function refreshSky() {
  if (Date.now() - fetchedAt < 20 * 60000) return place;
  try {
    place = await api('/api/sky');
    fetchedAt = Date.now();
    try {
      localStorage.setItem('ta-sky', JSON.stringify(place));
    } catch {}
  } catch {}
  return place;
}

function julian(ms) {
  return ms / DAY + 2440587.5;
}

export function sunTimes(date, lat, lon) {
  const noonUtc = Date.UTC(date.getFullYear(), date.getMonth(), date.getDate(), 12);
  const n = Math.round(julian(noonUtc) - 2451545.0 + 0.0008);
  const jStar = n - lon / 360;
  const M = (357.5291 + 0.98560028 * jStar) % 360;
  const C = 1.9148 * Math.sin(M * RAD) + 0.02 * Math.sin(2 * M * RAD) + 0.0003 * Math.sin(3 * M * RAD);
  const L = (M + C + 180 + 102.9372) % 360;
  const jTransit = 2451545.0 + jStar + 0.0053 * Math.sin(M * RAD) - 0.0069 * Math.sin(2 * L * RAD);
  const dec = Math.asin(Math.sin(L * RAD) * Math.sin(23.44 * RAD));
  const cosH = (Math.sin(-0.833 * RAD) - Math.sin(lat * RAD) * Math.sin(dec)) / (Math.cos(lat * RAD) * Math.cos(dec));
  if (cosH > 1) return { rise: null, set: null, polar: 'night' };
  if (cosH < -1) return { rise: null, set: null, polar: 'day' };
  const H = Math.acos(cosH) / RAD;
  const toMs = (j) => (j - 2440587.5) * DAY;
  return { rise: new Date(toMs(jTransit - H / 360)), set: new Date(toMs(jTransit + H / 360)) };
}

export function moonPhase(date) {
  const ref = Date.UTC(2000, 0, 6, 18, 14);
  const p = ((date.getTime() - ref) / DAY) % 29.530588853;
  return (p < 0 ? p + 29.530588853 : p) / 29.530588853;
}

export function weatherKind(code) {
  if (code == null) return 'clear';
  if (code >= 95) return 'storm';
  if ((code >= 71 && code <= 77) || code === 85 || code === 86) return 'snow';
  if ((code >= 51 && code <= 67) || (code >= 80 && code <= 82)) return 'rain';
  if (code === 45 || code === 48) return 'fog';
  if (code >= 2) return 'cloudy';
  return 'clear';
}

const DIWALI = { 2026: '11-08', 2027: '10-29', 2028: '10-17', 2029: '11-05', 2030: '10-26' };
const HOLI = { 2026: '03-04', 2027: '03-22', 2028: '03-11', 2029: '03-01', 2030: '03-20' };

function ymd(d) {
  return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`;
}

function near(d, md, before, after) {
  if (!md) return false;
  const t = Date.parse(`${d.getFullYear()}-${md}T00:00:00`);
  const now = Date.parse(ymd(d) + 'T00:00:00');
  return now >= t - before * DAY && now <= t + after * DAY;
}

export function festival(d, country) {
  const m = d.getMonth() + 1, day = d.getDate();
  if ((m === 12 && day === 31 && d.getHours() >= 18) || (m === 1 && day === 1)) return 'newyear';
  const india = !country || country === 'IN';
  if (india && near(d, DIWALI[d.getFullYear()], 2, 2)) return 'diwali';
  if (india && near(d, HOLI[d.getFullYear()], 1, 0)) return 'holi';
  return null;
}

export function season(d, lat, country) {
  let m = d.getMonth() + 1;
  if (lat != null && lat < 0) m = ((m + 5) % 12) + 1;
  if (country === 'IN' && m >= 6 && m <= 9) return 'monsoon';
  if (m >= 3 && m <= 5) return 'spring';
  if (m >= 6 && m <= 8) return 'summer';
  if (m >= 9 && m <= 11) return 'autumn';
  return 'winter';
}

export function skyNow(now = new Date()) {
  const p = place || {};
  let phase = 'day';
  let rise, set;
  if (p.lat != null && p.lon != null) {
    const t = sunTimes(now, p.lat, p.lon);
    if (t.polar) phase = t.polar;
    else { rise = t.rise; set = t.set; }
  } else {
    rise = new Date(now); rise.setHours(6, 15, 0, 0);
    set = new Date(now); set.setHours(18, 30, 0, 0);
  }
  if (rise && set) {
    const x = now.getTime();
    const edge = 35 * 60000;
    if (x < rise.getTime() - edge || x > set.getTime() + edge) phase = 'night';
    else if (Math.abs(x - rise.getTime()) <= edge) phase = 'dawn';
    else if (Math.abs(x - set.getTime()) <= edge) phase = 'dusk';
  }
  return {
    phase,
    night: phase === 'night',
    moon: moonPhase(now),
    weather: weatherKind(p.weather && p.weather.code),
    festival: festival(now, p.country),
    season: season(now, p.lat, p.country),
    city: p.city || null,
  };
}
