import math, random, sys
from build import defs, pine, smooth, pts

W, H = 900, 1600

MOUNT = [(0, 1180), (70, 1090), (140, 970), (210, 850), (270, 720), (318, 590), (352, 470), (372, 340), (384, 252), (398, 214), (536, 214), (552, 250), (572, 330), (604, 440), (650, 570), (712, 720), (780, 880), (850, 1020), (900, 1090)]
MOUNT_S = smooth(MOUNT, 10)

def top_at(x):
    for (x0, y0), (x1, y1) in zip(MOUNT_S, MOUNT_S[1:]):
        if x0 <= x <= x1:
            return y0 + (y1 - y0) * (x - x0) / (x1 - x0 or 1)
    return 9999

def inside(x, y, margin=0):
    return y >= top_at(x) + margin

WAY = [(450, 1560), (700, 1440), (250, 1320), (660, 1200), (300, 1080), (620, 960), (360, 850), (580, 745), (410, 650), (545, 560), (430, 470), (520, 385), (448, 300), (468, 222)]

def check(name, x, y, margin=0):
    if not inside(x, y, margin):
        raise SystemExit(f'{name} floats at {x:.0f},{y:.0f} (mountain edge {top_at(x):.0f})')

def steps_along():
    out = []
    for (x0, y0), (x1, y1) in zip(WAY, WAY[1:]):
        L = math.hypot(x1 - x0, y1 - y0)
        n = max(4, int(L / 24))
        for k in range(n):
            f = k / n
            out.append((x0 + (x1 - x0) * f, y0 + (y1 - y0) * f))
    return out

def scene():
    random.seed(2)
    s = ['<defs><linearGradient id="csky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#3F78B8"/><stop offset="0.45" stop-color="#8FB9DD"/><stop offset="0.8" stop-color="#E4DCC6"/><stop offset="1" stop-color="#F2D6A6"/></linearGradient>'
         '<linearGradient id="cmount" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#5D7F57"/><stop offset="0.55" stop-color="#7DA463"/><stop offset="1" stop-color="#9AC174"/></linearGradient>'
         '<linearGradient id="crock" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#6E747D"/><stop offset="0.6" stop-color="#959AA2"/><stop offset="1" stop-color="#B3B7BD"/></linearGradient>'
         '<linearGradient id="cfar" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#8FA8C8"/><stop offset="1" stop-color="#C4D0DD"/></linearGradient></defs>']
    s.append(f'<rect width="{W}" height="{H}" fill="url(#csky)"/>')
    s.append('<g id="c-nightsky" display="none"><rect width="900" height="1600" fill="#16224A" opacity="0.75"/>' + ''.join(f'<circle cx="{random.randint(0, W)}" cy="{random.randint(6, 700)}" r="{random.choice([1, 1, 1.5, 2])}" fill="#FFFFFF" opacity="{random.choice([0.5, 0.8, 1])}"/>' for _ in range(90)) + '</g>')
    s.append('<polygon points="0,700 90,560 170,640 260,500 330,600 330,1200 0,1200" fill="url(#cfar)"/><polygon points="600,620 700,480 790,580 860,500 900,540 900,1200 600,1200" fill="url(#cfar)"/>')
    s.append('<polygon points="90,560 112,590 100,592 124,616 150,612 130,590 170,640 140,600" fill="#EEF3F8" opacity="0.9"/><polygon points="700,480 722,510 712,512 732,534 760,530 740,510" fill="#EEF3F8" opacity="0.9"/>')
    s.append(f'<polygon points="{pts(MOUNT_S + [(900, 1600), (0, 1600)])}" fill="url(#cmount)"/>')
    rock = [p for p in MOUNT_S if p[1] < 700]
    lx, rx = rock[0][0], rock[-1][0]
    random.seed(12)
    edge = []
    n = 14
    for k in range(n + 1):
        x = rx - (rx - lx) * k / n
        y = 690 - 40 * math.sin(k * 0.9) - random.uniform(0, 40) - (30 if 0 < k < n else 0)
        edge.append((x, max(y, top_at(x) + 2)))
    s.append(f'<polygon points="{pts(rock + edge)}" fill="url(#crock)"/>')
    s.append(f'<polyline points="{pts(edge)}" fill="none" stroke="#6E9A52" stroke-width="10" stroke-linejoin="round"/>')
    s.append('<g stroke="#5C6169" stroke-width="2" fill="none" opacity="0.5"><path d="M380 330 L430 340"/><path d="M500 300 L548 312"/><path d="M360 420 L410 430"/><path d="M560 420 L600 436"/><path d="M340 520 L400 530"/><path d="M590 520 L630 534"/></g>')
    s.append('<g fill="#F4F7FA" opacity="0.9"><path d="M398 214 L420 226 L404 240 L390 236 Z"/><path d="M536 214 L552 250 L536 246 L522 226 Z"/></g>')
    for i in range(60):
        x = random.uniform(30, 870)
        y = random.uniform(700, 1520)
        if not inside(x, y, 40):
            continue
        near = min(math.hypot(x - a, y - b) for a, b in steps_along())
        if near < 46:
            continue
        h = 26 + (y - 700) / 820 * 46
        s.append(pine(x, y, h))
    path_pts = ' '.join(f'{x:g},{y:g}' for x, y in WAY)
    s.append(f'<polyline points="{path_pts}" fill="none" stroke="#B89A6A" stroke-width="22" stroke-linejoin="round" opacity="0.55"/>')
    st = steps_along()
    for i, (x, y) in enumerate(st):
        check(f'step {i}', x, y, 4)
        depth = (1560 - y) / 1340
        w = 40 - depth * 22
        h = 9 - depth * 4.5
        s.append(f'<g class="c-step" data-i="{i}" data-y="{y:.0f}">'
                 f'<g class="s-laid"><rect x="{x - w / 2:.1f}" y="{y - h:.1f}" width="{w:.1f}" height="{h:.1f}" fill="url(#stone)"/><rect x="{x - w / 2:.1f}" y="{y - 1.5:.1f}" width="{w:.1f}" height="1.5" fill="#5A5E65"/></g>'
                 f'<ellipse class="s-moss" cx="{x:.1f}" cy="{y - h + 1:.1f}" rx="{w * 0.32:.1f}" ry="2.6" fill="#5E8F3A"/>'
                 f'<rect class="s-ghost" x="{x - w / 2:.1f}" y="{y - h:.1f}" width="{w:.1f}" height="{h:.1f}" fill="#FFFFFF" fill-opacity="0.25" stroke="#1D1E21" stroke-opacity="0.7" stroke-width="1.6" stroke-dasharray="4 3"/>'
                 f'<circle class="s-trail" cx="{x:.1f}" cy="{y - 2:.1f}" r="1.6" fill="#7C6A4E" opacity="0.6"/></g>')
    corners = WAY[1:-1]
    for idx, (x, y) in enumerate(corners):
        check(f'landing {idx}', x, y, 6)
        depth = (1560 - y) / 1340
        w = 64 - depth * 30
        si = sum(max(4, int(math.hypot(WAY[k + 1][0] - WAY[k][0], WAY[k + 1][1] - WAY[k][1]) / 24)) for k in range(idx + 1))
        sc = 0.75 - depth * 0.35
        side = 26 if idx % 2 == 0 else -26
        s.append(f'<g class="c-land" data-i="{si}" data-x="{x}" data-y="{y}"><ellipse cx="{x}" cy="{y + 2}" rx="{w / 2 + 6:.1f}" ry="{6 - depth * 2:.1f}" fill="#8E9298"/><ellipse cx="{x}" cy="{y}" rx="{w / 2:.1f}" ry="{5 - depth * 2:.1f}" fill="#B3B7BC"/>'
                 f'<g class="l-on"><g transform="translate({x + side * sc * 1.4:.1f} {y:.1f}) scale({sc:.2f})"><use href="#toro"/></g>'
                 f'<path d="M{x - side * sc:.1f} {y:.1f} L{x - side * sc:.1f} {y - 34 * sc:.1f}" stroke="#4A2E1A" stroke-width="2"/><path d="M{x - side * sc:.1f} {y - 34 * sc:.1f} L{x - side * sc + 16 * sc:.1f} {y - 29 * sc:.1f} L{x - side * sc:.1f} {y - 24 * sc:.1f} Z" fill="#FFC21A"/>'
                 f'<circle class="l-glow" cx="{x + side * sc * 1.4:.1f}" cy="{y - 40 * sc:.1f}" r="26" fill="url(#glow)"/></g>'
                 f'<g class="l-off" transform="translate({x + side * sc * 1.4:.1f} {y:.1f}) scale({sc:.2f})" opacity="0.5"><use href="#toro"/></g></g>')
    hx, hy = WAY[4]
    s.append(f'<g transform="translate({hx - 70} {hy + 4})"><rect x="-22" y="-8" width="44" height="8" fill="#8E9298"/><rect x="-16" y="-38" width="32" height="30" fill="#7A4D2D"/><rect x="-10" y="-32" width="20" height="18" fill="#2B1E10"/><rect x="-5" y="-27" width="10" height="9" fill="#F2B33D"/><path d="M-26 -38 Q0 -56 26 -38 L22 -34 Q0 -48 -22 -34 Z" fill="#3A3F50"/></g>')
    check('shrine', hx - 70, hy + 4, 6)
    gx, gy = 467, 214
    s.append(f'<rect x="{gx - 66}" y="{gy - 6}" width="132" height="8" fill="url(#stone)"/><rect x="{gx - 52}" y="{gy - 112}" width="10" height="106" fill="#3A2416"/><rect x="{gx + 42}" y="{gy - 112}" width="10" height="106" fill="#3A2416"/>')
    s.append(f'<path d="M{gx - 70} {gy - 120} Q{gx} {gy - 134} {gx + 70} {gy - 120} L{gx + 68} {gy - 109} Q{gx} {gy - 120} {gx - 68} {gy - 109} Z" fill="#3A2416"/><rect x="{gx - 58}" y="{gy - 97}" width="116" height="8" fill="#3A2416"/><rect x="{gx - 13}" y="{gy - 109}" width="26" height="12" fill="#FFC21A"/>')
    s.append('<g fill="#FFFFFF" opacity="0.88"><ellipse cx="140" cy="600" rx="170" ry="26"/><ellipse cx="260" cy="584" rx="110" ry="24"/><ellipse cx="700" cy="560" rx="190" ry="28"/><ellipse cx="820" cy="590" rx="120" ry="22"/><ellipse cx="40" cy="640" rx="90" ry="18"/></g>')
    s.append('<g fill="#FFFFFF" opacity="0.55"><ellipse cx="450" cy="610" rx="210" ry="16"/><ellipse cx="620" cy="640" rx="140" ry="12"/></g>')
    s.append('<path d="M0 1500 Q450 1470 900 1500 L900 1600 L0 1600 Z" fill="#6E9A4C"/>')
    s.append('<g transform="translate(450 1566)"><rect x="-30" y="-6" width="60" height="8" fill="#8E9298"/><rect x="-12" y="-34" width="24" height="28" fill="#9A9EA4"/><rect x="-8" y="-28" width="16" height="10" fill="#FFC21A"/></g>')
    s.append('<g fill="#4C7A31">' + ''.join(f'<use href="#tuft" transform="translate({x} {y}) scale(1.1)"/>' for x, y in [(60, 1580), (260, 1590), (380, 1570), (600, 1585), (720, 1596), (880, 1576)]) + '</g>')
    s.append(f'<g id="c-night" display="none"><rect width="{W}" height="{H}" fill="#0D1636" opacity="0.5"/></g>')
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" class="scene climb" role="img" aria-label="The climb up the hill">{defs()}{"".join(s)}</svg>'

if __name__ == '__main__':
    out = sys.argv[1]
    open(f'{out}/climb.svg', 'w').write(scene())
    print('steps total', len(steps_along()))
