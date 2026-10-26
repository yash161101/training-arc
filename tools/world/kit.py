"""Shared outdoor parts so every inside scene uses the same sky, hills, grass and weather as the valley."""
import math, random
from build import pts, pine


def sky(W, horizon, sun=(0.78, 0.18), seed=3, stars=90):
    random.seed(seed)
    sx, sy = W * sun[0], horizon * sun[1]
    s = [f'<rect width="{W}" height="{horizon + 260}" fill="url(#sky)"/>']
    s.append(f'<g class="k-day"><circle cx="{sx:.0f}" cy="{sy:.0f}" r="{W * 0.2:.0f}" fill="url(#sunglow)"/><circle cx="{sx:.0f}" cy="{sy:.0f}" r="{W * 0.048:.0f}" fill="#FFF6DC"/></g>')
    st = ''.join(f'<circle class="{"a-twinkle a-d" + str(i % 4) if i % 3 == 0 else ""}" cx="{random.uniform(0, W):.0f}" cy="{random.uniform(6, horizon * 0.85):.0f}" r="{random.choice([1, 1, 1.4, 1.8])}" fill="#FFFFFF" opacity="{random.choice([0.5, 0.7, 0.95])}"/>' for i in range(stars))
    s.append(f'<g class="k-night"><rect width="{W}" height="{horizon + 260}" fill="#16224A" opacity="0.78"/>{st}<circle cx="{sx:.0f}" cy="{sy:.0f}" r="{W * 0.1:.0f}" fill="url(#sunglow)" opacity="0.3"/><circle cx="{sx:.0f}" cy="{sy:.0f}" r="{W * 0.034:.0f}" fill="#FFF3C9"/><circle cx="{sx + W * 0.014:.0f}" cy="{sy - W * 0.01:.0f}" r="{W * 0.03:.0f}" fill="#1F2B52" opacity="0.85"/></g>')
    return ''.join(s)


def clouds(W, y0, y1, n=4, seed=8, scale=1.0, opacity=0.92):
    random.seed(seed)
    out = []
    for k in range(n):
        x = (k + 0.5) * W / n + random.uniform(-W * 0.08, W * 0.08)
        y = random.uniform(y0, y1)
        r = random.uniform(70, 120) * scale
        out.append(f'<g class="a-cloud a-c{k % 3 + 1}"><ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{r:.0f}" ry="{r * 0.15:.0f}"/><ellipse cx="{x + r * 0.45:.0f}" cy="{y - r * 0.12:.0f}" rx="{r * 0.5:.0f}" ry="{r * 0.2:.0f}"/><ellipse cx="{x - r * 0.4:.0f}" cy="{y - r * 0.06:.0f}" rx="{r * 0.36:.0f}" ry="{r * 0.13:.0f}"/></g>')
    return f'<g fill="#FFFFFF" opacity="{opacity}">{"".join(out)}</g>'


def birds(x, y):
    return (f'<g class="k-day k-clear" fill="none" stroke="#45506A" stroke-width="2" stroke-linecap="round"><g class="a-birds-s">'
            f'<path class="a-flap" d="M{x} {y} q7 -7 14 0 q7 -7 14 0"/><path class="a-flap a-d1" d="M{x + 36} {y + 18} q5 -5 10 0 q5 -5 10 0"/>'
            f'<path class="a-flap a-d2" d="M{x - 24} {y + 26} q4 -4 8 0 q4 -4 8 0"/></g></g>')


def mountains(W, base, seed=1, height=1.0):
    random.seed(seed)
    s = []
    far = [(0, base - 140 * height)]
    peaks = []
    x = 0
    while x < W:
        x += random.uniform(110, 170)
        top = base - random.uniform(170, 260) * height
        mid_x = x - random.uniform(50, 80)
        far += [(mid_x, base - random.uniform(70, 120) * height), (x, top)]
        peaks.append((x, top))
    far += [(W, base - 80 * height), (W, base + 40), (0, base + 40)]
    s.append(f'<polygon points="{pts(far)}" fill="url(#far)"/>')
    for px, py in peaks:
        d = (base - py) * 0.3
        s.append(f'<polygon points="{pts([(px, py), (px + d * 0.62, py + d), (px + d * 0.25, py + d * 0.82), (px, py + d * 1.02), (px - d * 0.22, py + d * 0.78), (px - d * 0.6, py + d)])}" fill="#EEF2F6" opacity="0.92"/>')
    mid = [(0, base - 20 * height)]
    x = 0
    while x < W:
        x += random.uniform(120, 190)
        mid += [(x - 60, base - random.uniform(70, 110) * height), (x, base - random.uniform(20, 40) * height)]
    mid += [(W, base - 30 * height), (W, base + 60), (0, base + 60)]
    s.append(f'<polygon points="{pts(mid)}" fill="url(#mid)"/>')
    s.append(f'<rect x="0" y="{base - 120 * height:.0f}" width="{W}" height="{180 * height:.0f}" fill="url(#haze)"/>')
    return ''.join(s)


def treeline(W, base, seed=5, hmin=50, hmax=90, fill='url(#forestFar)', bottom=None):
    random.seed(seed)
    bottom = bottom if bottom is not None else base + 80
    p = [(0, bottom)]
    x = -20
    while x <= W + 20:
        b = base + 8 * math.sin(x / 90 + seed)
        h = random.uniform(hmin, hmax)
        w = h * 0.32
        p += [(x - w, b - h * 0.22), (x - w * 0.5, b - h * 0.55), (x - w * 0.62, b - h * 0.55), (x, b - h), (x + w * 0.62, b - h * 0.55), (x + w * 0.5, b - h * 0.55), (x + w, b - h * 0.22)]
        x += w * random.uniform(1.2, 1.7)
    p += [(W, bottom)]
    return f'<polygon points="{pts(p)}" fill="{fill}"/>'


def tuft(x, y, sc=1.0, light=False, sway=True, d=0):
    cls = f' class="a-grass a-d{d % 4}"' if sway else ''
    return f'<g transform="translate({x:.0f} {y:.0f}) scale({sc:.2f})"><use{cls} href="#{"tuftL" if light else "tuft"}"/></g>'


def meadow(x0, x1, y0, y1, n, seed=11, avoid=(), flowers=True, size=1.0):
    random.seed(seed)
    s = []
    for i in range(n):
        x, y = random.uniform(x0, x1), random.uniform(y0, y1)
        if any(a <= x <= b and c <= y <= d for a, b, c, d in avoid):
            continue
        sc = (0.7 + (y - y0) / max(1, y1 - y0) * 0.9) * size
        s.append(tuft(x, y, sc, random.random() < 0.3, sway=random.random() < 0.6, d=i))
    if flowers:
        for i in range(n // 6):
            x, y = random.uniform(x0, x1), random.uniform(y0, y1)
            if any(a <= x <= b and c <= y <= d for a, b, c, d in avoid):
                continue
            c = random.choice(['#FFC21A', '#F7F1E3', '#F2AFC3'])
            s.append(f'<g class="a-grass a-d{i % 4}"><path d="M{x:.0f} {y:.0f} l0 -10" stroke="#4C7A31" stroke-width="1.5"/><circle cx="{x:.0f}" cy="{y - 11:.0f}" r="{3.2 * size:.1f}" fill="{c}"/></g>')
    return ''.join(s)


def pebbles(spots):
    return ''.join(f'<ellipse cx="{x}" cy="{y}" rx="{r}" ry="{r * 0.45:.1f}" fill="#7E828A"/><ellipse cx="{x - r * 0.2:.1f}" cy="{y - r * 0.15:.1f}" rx="{r * 0.65:.1f}" ry="{r * 0.22:.1f}" fill="#9EA2A8"/>' for x, y, r in spots)


def leaves(W, y0, y1, n=8, seed=4, color='#F2AFC3'):
    random.seed(seed)
    return f'<g class="k-day" fill="{color}">' + ''.join(f'<ellipse class="a-petal a-d{i % 4} a-p{i % 3}" cx="{random.uniform(40, W - 40):.0f}" cy="{random.uniform(y0, y1):.0f}" rx="3.5" ry="2.2"/>' for i in range(n)) + '</g>'


def fireflies(x0, x1, y0, y1, n=18, seed=9):
    random.seed(seed)
    return '<g class="k-night">' + ''.join(f'<circle class="a-fly a-d{i % 5}" cx="{random.uniform(x0, x1):.0f}" cy="{random.uniform(y0, y1):.0f}" r="{random.choice([1.6, 2.2, 2.6])}" fill="#D7F58A"/>' for i in range(n)) + '</g>'


def weather(W, H, seed=21):
    random.seed(seed)
    rain = []
    for col in range(int(W / 22)):
        x = col * 22 + random.uniform(0, 18)
        y0 = random.uniform(0, 80)
        for k in range(-1, int(H / 80) + 2):
            rain.append(f'M{x:.0f} {y0 + k * 80:.0f} l-5 18')
    snow = []
    for col in range(int(W / 27)):
        x = col * 27 + random.uniform(0, 20)
        y0 = random.uniform(0, 100)
        for k in range(-1, int(H / 100) + 2):
            snow.append(f'<circle cx="{x + random.uniform(-6, 6):.0f}" cy="{y0 + k * 100:.0f}" r="{random.choice([1.5, 2, 2.5])}"/>')
    s = [f'<g class="k-dusk"><rect width="{W}" height="{H}" fill="url(#duskk)"/></g>']
    s.append(f'<g class="k-cloudy"><rect width="{W}" height="{H}" fill="#7E8A9A" opacity="0.2"/></g>')
    s.append(f'<g class="k-rain"><rect width="{W}" height="{H}" fill="#4A5566" opacity="0.25"/><path class="a-rain" d="{" ".join(rain)}" stroke="#DCE6F0" stroke-width="1.4" opacity="0.55"/><rect class="a-flash" width="{W}" height="{H}" fill="#FFFFFF" opacity="0"/></g>')
    s.append(f'<g class="k-snow"><rect width="{W}" height="{H}" fill="#DDE5EE" opacity="0.18"/><g class="a-snow" fill="#FFFFFF" opacity="0.85">{"".join(snow)}</g></g>')
    s.append(f'<g class="k-fog"><rect width="{W}" height="{H}" fill="#E6EBF0" opacity="0.3"/>' + ''.join(f'<g class="a-cloud a-c{k + 1}"><rect x="-100" y="{y:.0f}" width="{W + 200}" height="{h}" fill="url(#fogband)"/></g>' for k, (y, h) in enumerate([(H * 0.45, 160), (H * 0.7, 140), (H * 0.25, 110)])) + '</g>')
    return ''.join(s)


def defs_extra():
    return ('<defs><linearGradient id="duskk" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#5E4A86" stop-opacity="0.32"/><stop offset="0.45" stop-color="#FF8A50" stop-opacity="0.3"/><stop offset="1" stop-color="#FF9A50" stop-opacity="0.08"/></linearGradient>'
            '<linearGradient id="fogband" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#F2F5F8" stop-opacity="0"/><stop offset="0.5" stop-color="#F2F5F8" stop-opacity="0.75"/><stop offset="1" stop-color="#F2F5F8" stop-opacity="0"/></linearGradient>'
            '<linearGradient id="grassk" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#8DB262"/><stop offset="0.5" stop-color="#78A04F"/><stop offset="1" stop-color="#557E36"/></linearGradient>'
            '<radialGradient id="pool" cx="0.5" cy="0.5" r="0.5"><stop offset="0" stop-color="#FFB86B" stop-opacity="0.35"/><stop offset="1" stop-color="#FFB86B" stop-opacity="0"/></radialGradient></defs>')


def night(W, H, glows=(), ident='n-night'):
    g = ''.join(f'<circle class="a-glow a-d{i % 4}" cx="{x}" cy="{y}" r="{r}" fill="url(#glow)"/>' for i, (x, y, r) in enumerate(glows))
    return f'<g id="{ident}" display="none"><rect width="{W}" height="{H}" fill="#0D1636" opacity="0.5"/>{g}</g>'


def toro(x, y, sc=1.0):
    return f'<g transform="translate({x:.0f} {y:.0f}) scale({sc:.2f})"><use href="#toro"/></g><circle class="k-night a-glow" cx="{x:.0f}" cy="{y - 40 * sc:.0f}" r="{40 * sc:.0f}" fill="url(#glow)"/>'


def shadow(x, y, rx, ry, o=0.26):
    return f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{rx:.0f}" ry="{ry:.0f}" fill="#2B1E10" opacity="{o}"/>'


def broadleaf(x, y, h, cols=('#5E9A4A', '#78B35C', '#4C8040'), sway=True, seed=3):
    random.seed(seed)
    trunk = f'<path d="M{x} {y} Q{x - h * 0.04:.0f} {y - h * 0.35:.0f} {x + h * 0.02:.0f} {y - h * 0.6:.0f}" stroke="#5B3A27" stroke-width="{h * 0.07:.0f}" fill="none" stroke-linecap="round"/>'
    trunk += f'<path d="M{x + h * 0.01:.0f} {y - h * 0.45:.0f} Q{x - h * 0.16:.0f} {y - h * 0.6:.0f} {x - h * 0.26:.0f} {y - h * 0.62:.0f} M{x + h * 0.01:.0f} {y - h * 0.52:.0f} Q{x + h * 0.18:.0f} {y - h * 0.66:.0f} {x + h * 0.28:.0f} {y - h * 0.66:.0f}" stroke="#5B3A27" stroke-width="{h * 0.03:.0f}" fill="none" stroke-linecap="round"/>'
    blobs = ''
    for k in range(7):
        cx = x + random.uniform(-h * 0.3, h * 0.3)
        cy = y - h * 0.68 - random.uniform(-h * 0.12, h * 0.2)
        r = random.uniform(h * 0.14, h * 0.2)
        blobs += f'<circle cx="{cx:.0f}" cy="{cy:.0f}" r="{r:.0f}" fill="{cols[0]}"/><circle cx="{cx + r * 0.3:.0f}" cy="{cy - r * 0.35:.0f}" r="{r * 0.6:.0f}" fill="{cols[1]}"/><circle cx="{cx - r * 0.4:.0f}" cy="{cy + r * 0.3:.0f}" r="{r * 0.45:.0f}" fill="{cols[2]}"/>'
    crown = f'<g class="a-tree">{blobs}</g>' if sway else blobs
    return shadow(x, y + 2, h * 0.3, h * 0.04, 0.22) + trunk + crown
