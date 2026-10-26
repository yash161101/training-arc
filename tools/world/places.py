import math, random, sys
from build import defs, pine, pts
import kit


def svg(name, w, h, label, body):
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" class="scene place-{name}" role="img" aria-label="{label}">{defs()}{kit.defs_extra()}{body}</svg>'


def swaying_pine(x, y, h, c1='#2F5B47', c2='#3E6F57'):
    return f'<g class="a-tree a-d{int(x) % 4}">{pine(x, y, h, c1, c2)}</g>'


def cliff():
    W, H = 900, 1600
    random.seed(21)
    s = [kit.sky(W, 420, sun=(0.86, 0.1), seed=6), kit.clouds(W, 40, 150, n=3, seed=3, scale=0.9), kit.birds(560, 70), kit.mountains(W, 330, seed=4, height=0.8)]
    face = [(0, 1600), (0, 262), (36, 244), (70, 236), (120, 234), (168, 222), (190, 200), (240, 150), (420, 132), (600, 120), (760, 150), (900, 170), (900, 1600)]
    s.append(f'<polygon points="{pts(face)}" fill="url(#rock)"/>')
    s.append('<g stroke="#4B5058" stroke-width="2.5" fill="none" opacity="0.5">' + ''.join(f'<path d="M{random.randint(170, 420)} {y} L{random.randint(600, 880)} {y + random.randint(-14, 14)}"/>' for y in range(240, 1500, 90)) + '</g>')
    s.append('<g stroke="#454A52" stroke-width="2" fill="none" opacity="0.45">' + ''.join(f'<path d="M{x} {y} l{random.randint(-10, 10)} 40 l{random.randint(-12, 12)} 46 l{random.randint(-8, 8)} 30"/>' for x, y in [(260, 300), (700, 420), (330, 760), (780, 980), (240, 1180), (640, 1300)]) + '</g>')
    s.append('<g fill="#A3A8AF" opacity="0.45">' + ''.join(f'<path d="M{x} {y} l{random.randint(50, 110)} 8 l-4 18 l-{random.randint(50, 100)} -6 Z"/>' for x, y in [(620, 300), (700, 520), (250, 640), (660, 880), (300, 1060), (720, 1180), (260, 1330)]) + '</g>')
    ledges = [(230, 470, 70), (700, 610, 80), (250, 905, 60), (760, 1090, 70), (300, 1250, 70), (690, 1400, 60)]
    for x, y, w in ledges:
        s.append(f'<path d="M{x - w} {y} L{x + w} {y - 4} L{x + w - 8} {y + 10} L{x - w + 6} {y + 12} Z" fill="#6E737B"/><path d="M{x - w} {y} L{x + w} {y - 4}" stroke="#9EA2A8" stroke-width="3"/>')
        s.append(f'<path d="M{x - w * 0.8:.0f} {y + 1} Q{x:.0f} {y - 7} {x + w * 0.7:.0f} {y - 2}" stroke="#5E8A4A" stroke-width="6" fill="none" stroke-linecap="round"/>')
        s.append(kit.tuft(x - w * 0.5, y, 1.0, False, True, x) + kit.tuft(x + w * 0.4, y - 2, 0.8, True, True, y))
    for x, y, w in ledges[1::2]:
        s.append(f'<g transform="translate({x + w * 0.1:.0f} {y - 2})"><g class="a-tree"><path d="M0 0 Q-4 -14 2 -26" stroke="#5B3A27" stroke-width="4" fill="none"/><circle cx="-8" cy="-28" r="12" fill="#4C8040"/><circle cx="8" cy="-32" r="14" fill="#5E9A4A"/><circle cx="2" cy="-40" r="10" fill="#78B35C"/></g></g>')
    top = '<path d="M0 262 L36 244 L70 236 L120 234 L168 222 L190 200 L240 150 L420 132 L600 120 L760 150 L900 170 L900 196 L760 176 L600 146 L420 158 L250 176 L204 222 L170 240 L120 250 L70 252 L36 260 L0 276 Z" fill="#5E8A4A"/>'
    s.append(top)
    for x, y in [(250, 176), (420, 158), (600, 146), (840, 186)]:
        s.append(f'<g class="a-sway a-d{x % 4}"><path d="M{x} {y} Q{x - 8} {y + 50} {x + 4} {y + 110} Q{x + 10} {y + 150} {x} {y + 190}" stroke="#4C7639" stroke-width="3" fill="none"/>' + ''.join(f'<ellipse cx="{x + (4 if k % 2 else -6)}" cy="{y + 30 + k * 34}" rx="6" ry="3.5" fill="#5E8F3A"/>' for k in range(5)) + '</g>')
    s.append(swaying_pine(300, 142, 80) + swaying_pine(660, 128, 70) + swaying_pine(820, 166, 64) + swaying_pine(40, 252, 56))
    s.append(kit.meadow(220, 880, 136, 170, 20, seed=31, flowers=False, size=0.8))
    s.append('<path d="M60 238 Q112 228 166 236 L166 250 Q112 244 60 252 Z" fill="url(#water)"/><path d="M70 240 Q112 234 156 240" stroke="#CFEAF4" stroke-width="2" fill="none" class="a-ripple"/>')
    s.append('<path d="M60 246 Q112 238 166 246 L170 1500 L54 1500 Z" fill="url(#fall)"/>')
    for k in range(34):
        x = 62 + k * 3.1
        s.append(f'<path class="a-fall a-d{k % 4}" d="M{x:.1f} {random.randint(250, 380)} L{x + (x - 112) * 0.05:.1f} {random.randint(1100, 1480)}" stroke="#FFFFFF" stroke-width="{random.choice([1, 1.5, 2])}" opacity="{random.uniform(0.5, 0.95):.2f}"/>')
    s.append('<path d="M60 246 Q112 236 166 246 Q160 262 112 266 Q66 262 60 246 Z" fill="#F2FAFC"/>')
    s.append('<g fill="#666B74"><path d="M44 640 Q60 626 76 636 Q76 654 60 660 Q44 658 44 640 Z"/><path d="M152 980 Q168 966 184 976 Q184 994 168 998 Q152 996 152 980 Z"/></g><g fill="#FFFFFF" opacity="0.9"><ellipse class="a-mist" cx="76" cy="636" rx="18" ry="7"/><ellipse class="a-mist a-d2" cx="152" cy="976" rx="18" ry="7"/></g>')
    s.append('<ellipse cx="200" cy="1530" rx="270" ry="42" fill="url(#water)"/>')
    s.append('<g stroke="#BFE3EF" stroke-width="2" fill="none" opacity="0.7"><path class="a-ripple" d="M10 1530 Q200 1556 420 1528"/><path class="a-ripple a-d2" d="M60 1544 Q200 1562 360 1546"/><path class="a-ripple a-d3" d="M140 1516 Q220 1524 300 1514"/></g>')
    s.append('<ellipse class="a-mist" cx="110" cy="1476" rx="150" ry="56" fill="url(#mist)"/><ellipse class="a-mist a-d1" cx="60" cy="1430" rx="80" ry="40" fill="url(#mist)"/><ellipse class="a-mist a-d3" cx="190" cy="1450" rx="90" ry="38" fill="url(#mist)"/>')
    s.append('<g class="a-foam" fill="#FFFFFF" opacity="0.92"><ellipse cx="112" cy="1500" rx="74" ry="12"/><ellipse cx="50" cy="1508" rx="26" ry="7"/><ellipse cx="176" cy="1508" rx="28" ry="7"/></g>')
    s.append('<path d="M0 1560 Q450 1520 900 1550 L900 1600 L0 1600 Z" fill="url(#ground)"/>')
    s.append(kit.pebbles([(430, 1554, 18), (470, 1566, 12), (760, 1560, 16)]))
    s.append(''.join(f'<g transform="translate({x} {y})"><use class="a-grass a-d{i % 4}" href="#reed"/></g>' for i, (x, y) in enumerate([(380, 1548), (404, 1556), (20, 1560), (330, 1552)])))
    s.append(kit.meadow(440, 900, 1556, 1598, 26, seed=41))
    rx = 520
    s.append(f'<rect x="{rx - 40}" y="130" width="80" height="16" fill="url(#wood)"/><rect x="{rx - 6}" y="112" width="12" height="30" fill="#5E3920"/>')
    s.append(f'<g class="a-rope"><path d="M{rx} 146 Q{rx + 8} 800 {rx - 4} 1520" stroke="#C9A46A" stroke-width="7" fill="none"/><path d="M{rx} 146 Q{rx + 8} 800 {rx - 4} 1520" stroke="#8F6E3E" stroke-width="2" fill="none" stroke-dasharray="4 7"/></g>')
    holds = []
    n = 100
    for i in range(n):
        y = 1480 - i * 12.6
        side = -1 if i % 2 == 0 else 1
        x = rx + side * (30 + random.uniform(0, 26)) + 4 * math.sin(i / 3)
        holds.append((x, y))
    for i, (x, y) in enumerate(holds):
        sc = 1 - i / n * 0.35
        s.append(f'<g class="u" data-i="{i}" data-y="{y:.0f}"><g class="u-on"><ellipse cx="{x:.1f}" cy="{y + 3:.1f}" rx="{11 * sc:.1f}" ry="{5 * sc:.1f}" fill="#4B4F57"/><ellipse cx="{x:.1f}" cy="{y:.1f}" rx="{10 * sc:.1f}" ry="{6 * sc:.1f}" fill="#FFC21A" stroke="#1D1E21" stroke-width="1.5"/></g>'
                 f'<ellipse class="u-moss" cx="{x:.1f}" cy="{y - 2:.1f}" rx="{8 * sc:.1f}" ry="{3 * sc:.1f}" fill="#5E8F3A"/>'
                 f'<ellipse class="u-ghost" cx="{x:.1f}" cy="{y:.1f}" rx="{10 * sc:.1f}" ry="{6 * sc:.1f}" fill="#FFFFFF" fill-opacity="0.25" stroke="#1D1E21" stroke-width="1.5" stroke-dasharray="3 2"/>'
                 f'<circle class="u-off" cx="{x:.1f}" cy="{y:.1f}" r="2" fill="#E9EAEC" opacity="0.6"/></g>')
    for at in (20, 40, 60, 80, 99):
        x, y = holds[at]
        ly = y + 14
        s.append(f'<g class="u-land" data-i="{at + 1}"><path d="M{rx - 120} {ly} L{rx + 120} {ly - 4} L{rx + 110} {ly + 12} L{rx - 112} {ly + 14} Z" fill="#7E838A"/><path d="M{rx - 120} {ly} L{rx + 120} {ly - 4}" stroke="#9EA2A8" stroke-width="3"/>'
                 f'<g class="l-on"><path d="M{rx + 80} {ly - 2} L{rx + 80} {ly - 40}" stroke="#4A2E1A" stroke-width="3"/><path class="a-flag" d="M{rx + 81} {ly - 40} L{rx + 104} {ly - 34} L{rx + 81} {ly - 27} Z" fill="#FFC21A"/></g></g>')
    s.append(kit.leaves(W, 200, 1400, n=6, seed=12, color='#78B35C'))
    s.append(kit.weather(W, H))
    s.append(kit.night(W, H))
    s.append(kit.fireflies(240, 880, 1380, 1580, 16))
    return svg('cliff', W, H, 'The cliff climb', ''.join(s))


def yard():
    W, H = 900, 1300
    random.seed(31)
    s = [kit.sky(W, 640, sun=(0.18, 0.16), seed=7), kit.clouds(W, 70, 300, n=4, seed=5), kit.birds(520, 220), kit.mountains(W, 610, seed=2)]
    s.append(kit.treeline(W, 700, seed=6, hmin=70, hmax=110))
    s.append(kit.treeline(W, 732, seed=8, hmin=60, hmax=120, fill='url(#forestNear)'))
    s.append('<path d="M0 720 Q450 690 900 720 L900 1300 L0 1300 Z" fill="url(#ground)"/>')
    s.append('<path d="M0 760 Q450 740 900 770 L900 800 Q450 772 0 790 Z" fill="#A8CB76" opacity="0.35"/>')
    s.append('<ellipse cx="450" cy="1010" rx="460" ry="190" fill="url(#dirt)"/><ellipse cx="450" cy="1000" rx="400" ry="150" fill="#DCC292" opacity="0.6"/>')
    s.append('<g stroke="#C4A26E" stroke-width="2" fill="none" opacity="0.6"><ellipse cx="450" cy="1004" rx="300" ry="110"/><ellipse cx="450" cy="1004" rx="200" ry="72"/></g>')
    s.append(kit.meadow(0, 900, 740, 830, 40, seed=12, avoid=[(60, 840, 820, 1300)]))
    rk = 820
    s.append(kit.shadow(rk + 10, 786, 60, 7) + f'<rect x="{rk - 50}" y="700" width="8" height="86" fill="url(#wood)"/><rect x="{rk + 44}" y="700" width="8" height="86" fill="url(#wood)"/><rect x="{rk - 56}" y="712" width="114" height="7" fill="#5E3920"/><rect x="{rk - 56}" y="752" width="114" height="7" fill="#5E3920"/>'
             + ''.join(f'<path d="M{rk - 38 + k * 18} 696 L{rk - 34 + k * 18} 784" stroke="{c}" stroke-width="5" stroke-linecap="round"/>' for k, c in enumerate(['#A06C43', '#C9A46A', '#8F6E3E', '#A06C43', '#C9A46A'])))
    s.append(kit.shadow(96, 778, 30, 5) + '<path d="M90 778 L90 560" stroke="#4A2E1A" stroke-width="5"/><g class="a-flag"><path d="M92 566 L128 566 L128 690 L110 680 L92 690 Z" fill="#FFC21A"/><g fill="#1D1E21"><rect x="99" y="604" width="6" height="6"/><rect x="107" y="604" width="6" height="6"/><rect x="107" y="596" width="6" height="6"/><rect x="115" y="604" width="6" height="6"/><rect x="115" y="596" width="6" height="6"/><rect x="115" y="588" width="6" height="6"/></g></g><path d="M92 566 L128 566" stroke="#4A2E1A" stroke-width="4"/>')
    posts = [(180, 860, 0.62), (330, 850, 0.62), (570, 850, 0.62), (720, 860, 0.62), (120, 1080, 1.0), (330, 1110, 1.0), (570, 1110, 1.0), (780, 1080, 1.0)]
    vines = []
    u = 0
    for p, (x, y, k) in enumerate(posts):
        h = 230 * k
        w = 34 * k
        s.append(f'<ellipse cx="{x - 10 * k:.0f}" cy="{y + 4:.0f}" rx="{40 * k:.0f}" ry="{9 * k:.0f}" fill="#2B1E10" opacity="0.28"/><rect x="{x - w / 2:.0f}" y="{y - h:.0f}" width="{w:.0f}" height="{h:.0f}" fill="url(#wood)"/><ellipse cx="{x}" cy="{y - h:.0f}" rx="{w / 2:.0f}" ry="{7 * k:.0f}" fill="#C08B5A"/>')
        for b in range(5):
            by = y - h + 26 * k + b * 36 * k
            bh = 22 * k
            s.append(f'<g class="u" data-i="{u}" data-y="{by:.0f}"><g class="u-on"><rect x="{x - w / 2 - 3:.0f}" y="{by:.0f}" width="{w + 6:.0f}" height="{bh:.0f}" fill="#D8B878"/><path d="M{x - w / 2 - 3:.0f} {by + bh * 0.33:.0f} H{x + w / 2 + 3:.0f} M{x - w / 2 - 3:.0f} {by + bh * 0.66:.0f} H{x + w / 2 + 3:.0f}" stroke="#A88746" stroke-width="2"/></g>'
                     f'<rect class="u-ghost" x="{x - w / 2 - 3:.0f}" y="{by:.0f}" width="{w + 6:.0f}" height="{bh:.0f}" fill="#FFFFFF" fill-opacity="0.2" stroke="#1D1E21" stroke-width="1.6" stroke-dasharray="4 3"/></g>')
            u += 1
        vines.append(f'<path d="M{x - w / 2:.0f} {y:.0f} Q{x - w / 2 - 10 * k:.0f} {y - h * 0.4:.0f} {x - w / 3:.0f} {y - h * 0.6:.0f} Q{x:.0f} {y - h * 0.8:.0f} {x - w / 2:.0f} {y - h * 0.95:.0f}" stroke="#4C7A34" stroke-width="{3 * k:.1f}" fill="none"/><circle cx="{x - w / 2 - 6 * k:.0f}" cy="{y - h * 0.4:.0f}" r="{5 * k:.1f}" fill="#5E8F3A"/><circle cx="{x - w / 4:.0f}" cy="{y - h * 0.7:.0f}" r="{5 * k:.1f}" fill="#5E8F3A"/>')
    x, y = 450, 1000
    s.append(f'<g class="k-day">' + ''.join(f'<ellipse class="a-dust a-d{k}" cx="{x + dx}" cy="{y - 4}" rx="{r}" ry="{r * 0.5:.0f}" fill="#E8D3A6"/>' for k, (dx, r) in enumerate([(-40, 16), (30, 12), (60, 10)])) + '</g>')
    s.append(f'<g id="n-dummy"><ellipse cx="{x - 14}" cy="{y + 6}" rx="50" ry="10" fill="#2B1E10" opacity="0.3"/><g class="a-breathe"><rect x="{x - 8}" y="{y - 250}" width="16" height="250" fill="url(#wood)"/><rect x="{x - 60}" y="{y - 186}" width="120" height="16" fill="url(#wood)"/>'
             f'<path d="M{x - 34} {y - 214} Q{x} {y - 232} {x + 34} {y - 214} L{x + 40} {y - 70} Q{x} {y - 52} {x - 40} {y - 70} Z" fill="#D9BC7C"/><path d="M{x - 36} {y - 170} Q{x} {y - 158} {x + 36} {y - 170} M{x - 38} {y - 116} Q{x} {y - 104} {x + 38} {y - 116}" stroke="#A88746" stroke-width="3" fill="none"/>'
             f'<circle cx="{x}" cy="{y - 238}" r="28" fill="#D9BC7C"/><rect x="{x - 26}" y="{y - 252}" width="52" height="10" fill="#FFC21A"/><path class="a-flag" d="M{x + 26} {y - 250} L{x + 56} {y - 260} L{x + 52} {y - 238} Z" fill="#FFC21A"/></g></g>')
    s.append(f'<g id="n-vines" display="none">{"".join(vines)}</g>')
    tx, ty = 860, 1230
    s.append(kit.shadow(tx - 20, ty + 4, 90, 12, 0.3) + f'<path d="M{tx} {ty} Q{tx - 14} {ty - 200} {tx + 6} {ty - 420}" stroke="#5B3A27" stroke-width="30" fill="none" stroke-linecap="round"/><path d="M{tx - 4} {ty - 330} Q{tx - 120} {ty - 360} {tx - 190} {ty - 350}" stroke="#5B3A27" stroke-width="12" fill="none" stroke-linecap="round"/>')
    bx, by = tx - 160, ty - 352
    s.append(f'<g class="a-swing"><path d="M{bx} {by} L{bx} {by + 120}" stroke="#C9A46A" stroke-width="3"/><rect x="{bx - 22}" y="{by + 120}" width="44" height="96" rx="16" fill="#8A5A34"/><path d="M{bx - 22} {by + 150} H{bx + 22} M{bx - 22} {by + 186} H{bx + 22}" stroke="#5E3920" stroke-width="3"/><rect x="{bx - 22}" y="{by + 120}" width="44" height="10" fill="#5E3920"/></g>')
    s.append(f'<g class="a-tree">' + ''.join(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{c}"/>' for cx, cy, r, c in [(tx - 40, ty - 470, 90, '#3E6F57'), (tx + 30, ty - 520, 80, '#4C8040'), (tx - 120, ty - 420, 70, '#3E6F57'), (tx - 20, ty - 560, 60, '#5E9A4A'), (tx - 90, ty - 500, 50, '#5E9A4A'), (tx + 40, ty - 430, 60, '#4C8040')]) + '</g>')
    s.append(kit.toro(60, 1250, 1.6) + kit.toro(720, 1270, 1.4))
    s.append(kit.meadow(0, 900, 1190, 1298, 30, seed=14, avoid=[(780, 900, 1180, 1300)]))
    s.append(kit.leaves(W, 500, 1100, n=7, seed=9, color='#F2AFC3'))
    s.append(kit.weather(W, H))
    s.append(kit.night(W, H))
    s.append(kit.fireflies(0, 900, 760, 1260, 22))
    return svg('yard', W, H, 'The push yard', ''.join(s))


def forge():
    W, H = 900, 1300
    random.seed(41)
    s = ['<defs><linearGradient id="ray" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FFF4D2" stop-opacity="0.35"/><stop offset="1" stop-color="#FFF4D2" stop-opacity="0"/></linearGradient></defs>']
    s.append('<rect width="900" height="1300" fill="url(#plank)"/>')
    s.append('<g stroke="#55361F" stroke-width="2">' + ''.join(f'<path d="M0 {y} H900"/>' for y in range(60, 900, 56)) + '</g>')
    s.append('<g stroke="#7A4D2D" stroke-width="1.2" opacity="0.6">' + ''.join(f'<path d="M{random.randint(20, 860)} {y + random.randint(14, 40)} q{random.randint(20, 40)} -4 {random.randint(50, 90)} 0"/>' for y in range(60, 900, 56) for _ in range(3)) + '</g>')
    s.append('<g fill="#4A2E1A">' + ''.join(f'<rect x="{x}" y="0" width="14" height="900"/>' for x in (0, 300, 600, 886)) + '</g>')
    wx0, wy0, wx1, wy1 = 470, 30, 840, 190
    s.append(f'<clipPath id="fwin"><rect x="{wx0}" y="{wy0}" width="{wx1 - wx0}" height="{wy1 - wy0}"/></clipPath><g clip-path="url(#fwin)">')
    s.append(f'<rect x="{wx0}" y="{wy0}" width="{wx1 - wx0}" height="{wy1 - wy0}" fill="url(#sky)"/>')
    s.append(f'<polygon points="{wx0},{wy1 - 40} {wx0 + 60},{wy1 - 90} {wx0 + 120},{wy1 - 60} {wx0 + 200},{wy1 - 110} {wx0 + 280},{wy1 - 70} {wx1},{wy1 - 96} {wx1},{wy1} {wx0},{wy1}" fill="url(#far)"/>')
    s.append(f'<polygon points="{wx0 + 180},{wy1 - 100} {wx0 + 200},{wy1 - 110} {wx0 + 222},{wy1 - 96} {wx0 + 204},{wy1 - 92}" fill="#EEF2F6"/>')
    s.append(kit.treeline(wx1, wy1 - 18, seed=3, hmin=26, hmax=44, fill='url(#forestNear)', bottom=wy1))
    s.append(f'<g fill="#FFFFFF" opacity="0.9"><g class="a-cloud"><ellipse cx="{wx0 + 90}" cy="{wy0 + 40}" rx="60" ry="10"/><ellipse cx="{wx0 + 120}" cy="{wy0 + 32}" rx="30" ry="10"/></g><g class="a-cloud a-c2"><ellipse cx="{wx0 + 270}" cy="{wy0 + 56}" rx="70" ry="9"/></g></g>')
    s.append(f'<g class="k-night"><rect x="{wx0}" y="{wy0}" width="{wx1 - wx0}" height="{wy1 - wy0}" fill="#16224A" opacity="0.82"/>' + ''.join(f'<circle class="a-twinkle a-d{k % 4}" cx="{random.randint(wx0, wx1)}" cy="{random.randint(wy0, wy0 + 90)}" r="1.4" fill="#FFFFFF"/>' for k in range(14)) + f'<circle cx="{wx1 - 60}" cy="{wy0 + 40}" r="12" fill="#FFF3C9"/></g>')
    s.append(f'<g class="k-rain"><rect x="{wx0}" y="{wy0}" width="{wx1 - wx0}" height="{wy1 - wy0}" fill="#4A5566" opacity="0.35"/><path class="a-rain" d="' + ' '.join(f'M{x} {y} l-5 18' for x in range(wx0, wx1, 18) for y in range(wy0 - 80, wy1, 80)) + '" stroke="#DCE6F0" stroke-width="1.4" opacity="0.6"/></g>')
    s.append(f'<g class="k-snow"><g class="a-snow" fill="#FFFFFF">' + ''.join(f'<circle cx="{x + random.randint(-5, 5)}" cy="{y}" r="2"/>' for x in range(wx0, wx1, 26) for y in range(wy0 - 100, wy1, 100)) + '</g></g>')
    s.append('</g>')
    s.append(f'<rect x="{wx0 - 10}" y="{wy0 - 10}" width="{wx1 - wx0 + 20}" height="{wy1 - wy0 + 20}" fill="none" stroke="#4A2E1A" stroke-width="14"/><path d="M{(wx0 + wx1) / 2} {wy0} V{wy1} M{wx0} {(wy0 + wy1) / 2} H{wx1}" stroke="#4A2E1A" stroke-width="6"/><rect x="{wx0 - 16}" y="{wy1 + 4}" width="{wx1 - wx0 + 32}" height="10" fill="#5E3920"/>')
    s.append(f'<polygon class="a-shimmer k-day" points="{wx0},{wy1} {wx1},{wy1} 760,900 300,900" fill="url(#ray)" opacity="0.5"/>')
    s.append('<path d="M0 900 L900 900 L900 1300 L0 1300 Z" fill="#6B6F76"/><g stroke="#55595F" stroke-width="2">' + ''.join(f'<path d="M0 {y} H900"/>' for y in (960, 1040, 1140, 1260)) + ''.join(f'<path d="M{x} {a} V{b}"/>' for a, b, xs in ((900, 960, (120, 330, 560, 780)), (960, 1040, (60, 250, 470, 690)), (1040, 1140, (150, 380, 620, 840)), (1140, 1260, (90, 300, 520, 750))) for x in xs) + '</g>')
    s.append('<ellipse cx="200" cy="960" rx="300" ry="70" fill="url(#pool)"/>')
    s.append('<path d="M60 380 L320 380 L300 300 L80 300 Z" fill="#5F636A"/><rect x="150" y="0" width="80" height="300" fill="#7E828A"/><rect x="60" y="560" width="260" height="340" fill="#8C9096"/><g stroke="#6E7278" stroke-width="2"><path d="M60 640 H320 M60 720 H320 M60 800 H320 M150 560 V640 M240 640 V720 M120 720 V800 M260 720 V800"/></g>')
    s.append('<rect x="90" y="470" width="200" height="94" fill="#2E2A28"/>')
    sparks = ''.join(f'<circle class="a-spark a-d{k % 4} a-p{k % 3}" cx="{random.randint(150, 230)}" cy="{random.randint(470, 520)}" r="{random.choice([1.6, 2.2, 2.8])}" fill="{random.choice(["#FFE08A", "#FFB020", "#FF7A2E"])}"/>' for k in range(16))
    smoke = '<g fill="#B8B4AE" opacity="0.55">' + ''.join(f'<circle class="a-smoke a-d{k}" cx="{176 + k * 10}" cy="{440 - k * 6}" r="{14 + k * 4}"/>' for k in range(4)) + '</g>'
    s.append('<g id="n-fire"><circle class="a-glow" cx="190" cy="520" r="230" fill="url(#glow)"/><ellipse cx="190" cy="556" rx="96" ry="18" fill="url(#coal)"/>'
             '<path class="a-flicker" d="M150 556 Q140 520 160 494 Q166 520 176 506 Q180 470 196 452 Q204 490 214 478 Q228 506 222 530 Q236 520 236 556 Z" fill="#FF9A2E"/>'
             f'<path class="a-flicker a-d2" d="M170 556 Q166 530 180 512 Q186 530 192 520 Q200 500 208 494 Q214 520 212 556 Z" fill="#FFE08A"/>{smoke}{sparks}</g>')
    s.append('<g id="n-cold" display="none"><ellipse cx="190" cy="556" rx="96" ry="16" fill="#5A5C61"/><g fill="#7E8186"><circle cx="160" cy="550" r="6"/><circle cx="196" cy="546" r="7"/><circle cx="224" cy="552" r="5"/></g></g>')
    s.append('<g transform="translate(372 880)"><g class="a-pump"><path d="M-40 -12 L40 -26 L44 -6 L-40 6 Z" fill="#6E4428"/><path d="M-40 -12 Q-50 -40 0 -46 Q44 -40 40 -26" fill="#8A5A34"/><path d="M-30 -20 Q0 -36 30 -30" stroke="#5E3920" stroke-width="2" fill="none"/></g><path d="M40 -16 L80 -16" stroke="#3A3C42" stroke-width="7"/><path d="M-40 -6 L-70 -60" stroke="#6E4428" stroke-width="6" stroke-linecap="round"/></g>')
    s.append('<g transform="translate(330 900)">' + ''.join(f'<ellipse cx="{dx}" cy="{dy}" rx="14" ry="9" fill="#2E2A28"/><ellipse cx="{dx - 3}" cy="{dy - 3}" rx="6" ry="3" fill="#4A4645"/>' for dx, dy in [(-120, -6), (-100, -16), (-84, -4), (-106, 2)]) + '</g>')
    s.append('<g stroke="#2E3035" stroke-width="5" stroke-linecap="round" fill="none"><path d="M330 600 L340 760 M350 600 L340 760"/><path d="M380 610 L380 730"/></g><rect x="370" y="594" width="20" height="18" fill="#3A3C42"/><path d="M318 596 H400" stroke="#4A2E1A" stroke-width="6"/>')
    rack_x0, rack_y0 = 400, 260
    s.append(f'<rect x="{rack_x0 - 20}" y="{rack_y0 - 30}" width="500" height="560" fill="#5E3920"/><rect x="{rack_x0 - 10}" y="{rack_y0 - 20}" width="480" height="540" fill="#7A4D2D"/>')
    u = 0
    for row in range(3):
        y = rack_y0 + 40 + row * 175
        s.append(f'<rect x="{rack_x0}" y="{y - 14}" width="460" height="10" fill="#4A2E1A"/>')
        for col in range(8):
            x = rack_x0 + 30 + col * 57
            kind = (row * 8 + col) % 3
            s.append(f'<circle cx="{x}" cy="{y - 9}" r="4" fill="#2E2A28"/>')
            if kind == 0:
                item = f'<rect x="{x - 3}" y="{y}" width="6" height="70" fill="#3A3C42"/><rect x="{x - 14}" y="{y + 4}" width="28" height="18" fill="#2E3035"/><rect x="{x - 14}" y="{y + 50}" width="28" height="18" fill="#2E3035"/><rect x="{x - 14}" y="{y + 4}" width="28" height="4" fill="#FFC21A"/>'
                ghost = f'<rect x="{x - 14}" y="{y + 4}" width="28" height="64"/>'
            elif kind == 1:
                item = f'<path d="M{x - 12} {y + 24} Q{x - 12} {y + 2} {x} {y + 2} Q{x + 12} {y + 2} {x + 12} {y + 24}" stroke="#2E3035" stroke-width="6" fill="none"/><circle cx="{x}" cy="{y + 50}" r="24" fill="#2E3035"/><circle cx="{x - 8}" cy="{y + 42}" r="5" fill="#4A4D55"/><rect x="{x - 6}" y="{y + 58}" width="12" height="4" fill="#FFC21A"/>'
                ghost = f'<circle cx="{x}" cy="{y + 46}" r="26"/>'
            else:
                item = f'<path d="M{x - 4} {y} L{x + 4} {y} L{x + 6} {y + 110} L{x} {y + 124} L{x - 6} {y + 110} Z" fill="#B9BDC3"/><rect x="{x - 12}" y="{y + 18}" width="24" height="6" fill="#2E3035"/><rect x="{x - 4}" y="{y}" width="8" height="18" fill="#6E4428"/><path d="M{x} {y + 30} L{x} {y + 110}" stroke="#E7E8EA" stroke-width="1.5"/>'
                ghost = f'<rect x="{x - 8}" y="{y}" width="16" height="122"/>'
            s.append(f'<g class="u" data-i="{u}" data-y="{y:.0f}"><g class="u-on">{item}</g><g class="u-ghost" fill="#FFFFFF" fill-opacity="0.15" stroke="#1D1E21" stroke-width="1.6" stroke-dasharray="4 3">{ghost}</g></g>')
            u += 1
    s.append('<g class="a-sway a-d2"><path d="M430 0 L430 120" stroke="#3A2416" stroke-width="2"/><rect x="412" y="120" width="36" height="46" rx="14" fill="#F2B33D"/><path d="M412 136 H448 M412 150 H448" stroke="#C9851B" stroke-width="2"/><rect x="420" y="116" width="20" height="5" fill="#3A2416"/><rect x="420" y="165" width="20" height="5" fill="#3A2416"/></g><circle class="a-glow" cx="430" cy="144" r="70" fill="url(#glow)" opacity="0.6"/>')
    ax, ay = 540, 1080
    s.append(f'<ellipse cx="{ax}" cy="{ay + 110}" rx="170" ry="22" fill="#2B1E10" opacity="0.35"/><rect x="{ax - 60}" y="{ay}" width="120" height="110" fill="#6E4428"/><ellipse cx="{ax}" cy="{ay}" rx="60" ry="14" fill="#A06C43"/>')
    s.append(f'<path d="M{ax - 130} {ay - 70} h220 l-26 30 h-40 v40 h-60 v-40 h-40 Z" fill="#2E3035"/><path d="M{ax - 126} {ay - 70} h212" stroke="#5F636A" stroke-width="5"/>')
    s.append(f'<rect class="a-glow" x="{ax - 90}" y="{ay - 82}" width="110" height="12" rx="4" fill="#FF8A2E"/><rect x="{ax - 70}" y="{ay - 80}" width="60" height="5" fill="#FFE08A" class="a-glow a-d2"/>')
    s.append(f'<path d="M{ax + 40} {ay - 150} L{ax + 110} {ay - 76}" stroke="#6E4428" stroke-width="12" stroke-linecap="round"/><rect x="{ax + 16}" y="{ay - 176}" width="54" height="30" fill="#3A3C42" transform="rotate(45 {ax + 43} {ay - 161})"/>')
    s.append('<ellipse cx="790" cy="1190" rx="70" ry="18" fill="#2B1E10" opacity="0.3"/><rect x="730" y="1050" width="120" height="140" fill="#6E4428"/><g stroke="#4A2E1A" stroke-width="5"><path d="M730 1080 H850 M730 1160 H850"/></g><ellipse cx="790" cy="1050" rx="60" ry="14" fill="#8FC4D8"/><ellipse class="a-ripple" cx="790" cy="1050" rx="40" ry="8" fill="none" stroke="#CFEAF4" stroke-width="2"/>')
    s.append('<g fill="#FFFFFF" opacity="0.5"><circle class="a-smoke a-d1" cx="780" cy="1030" r="12"/><circle class="a-smoke a-d3" cx="800" cy="1020" r="10"/></g>')
    s.append(kit.night(W, H, [(190, 520, 260), (430, 144, 90)]))
    return svg('forge', W, H, 'The forge', ''.join(s))


def boulders():
    W, H = 900, 1300
    random.seed(51)
    s = [kit.sky(W, 560, sun=(0.8, 0.16), seed=8), kit.clouds(W, 60, 260, n=4, seed=9), kit.birds(480, 180), kit.mountains(W, 520, seed=5)]
    s.append(kit.treeline(W, 560, seed=4, hmin=60, hmax=100))
    s.append(swaying_pine(70, 600, 200) + swaying_pine(830, 600, 220) + swaying_pine(150, 600, 150, '#355E4C', '#46705A'))
    rx, ry = 520, 548
    s.append(f'<path d="M{rx - 190} {ry} Q{rx - 150} {ry - 10} {rx - 130} {ry - 50} L{rx + 130} {ry - 50} Q{rx + 150} {ry - 10} {rx + 190} {ry} Z" fill="url(#roof)"/><path d="M{rx - 130} {ry - 50} Q{rx - 70} {ry - 100} {rx} {ry - 110} Q{rx + 70} {ry - 100} {rx + 130} {ry - 50} Z" fill="url(#roof)"/>'
             f'<g stroke="#4F5970" stroke-width="1.5" opacity="0.8" fill="none"><path d="M{rx - 100} {ry - 54} Q{rx - 50} {ry - 92} {rx} {ry - 100} Q{rx + 50} {ry - 92} {rx + 100} {ry - 54}"/><path d="M{rx - 160} {ry - 6} Q{rx - 136} {ry - 16} {rx - 124} {ry - 40} L{rx + 124} {ry - 40} Q{rx + 136} {ry - 16} {rx + 160} {ry - 6}"/></g>'
             f'<rect x="{rx - 28}" y="{ry - 118}" width="56" height="10" fill="#262B38"/><path d="M{rx - 32} {ry - 115} l-9 -9 M{rx + 32} {ry - 115} l9 -9" stroke="#262B38" stroke-width="6" stroke-linecap="round"/><path d="M{rx - 190} {ry} l-14 -12 M{rx + 190} {ry} l14 -12" stroke="#262B38" stroke-width="7" stroke-linecap="round"/><rect x="{rx - 16}" y="{ry - 84}" width="32" height="20" fill="#5E3920"/><rect x="{rx - 12}" y="{ry - 81}" width="24" height="14" fill="#F6EDDB"/><g fill="#1D1E21"><rect x="{rx - 8}" y="{ry - 74}" width="5" height="5"/><rect x="{rx - 2}" y="{ry - 74}" width="5" height="5"/><rect x="{rx - 2}" y="{ry - 80}" width="5" height="5"/><rect x="{rx + 4}" y="{ry - 74}" width="5" height="5"/><rect x="{rx + 4}" y="{ry - 80}" width="5" height="5"/></g>')
    s.append('<rect x="0" y="560" width="900" height="120" fill="#C9BCA2"/><rect x="0" y="548" width="900" height="16" fill="#5E3920"/><rect x="0" y="548" width="900" height="4" fill="#7A4D2D"/><g fill="#A99B80">' + ''.join(f'<rect x="{x}" y="564" width="2" height="116"/>' for x in range(0, 900, 60)) + '</g>')
    s.append('<rect x="0" y="664" width="900" height="16" fill="#8E9298"/><g stroke="#6E7278" stroke-width="1.5">' + ''.join(f'<path d="M{x} 664 V680"/>' for x in range(30, 900, 70)) + '</g>')
    s.append('<path d="M0 680 L900 680 L900 1300 L0 1300 Z" fill="#D9D3C4"/>')
    s.append('<g fill="#5E8F3A" opacity="0.85">' + ''.join(f'<ellipse cx="{x}" cy="686" rx="{r}" ry="6"/>' for x, r in [(40, 50), (230, 30), (420, 40), (660, 36), (880, 44)]) + '</g>')
    s.append('<g stroke="#BDB5A2" stroke-width="2" fill="none">' + ''.join(f'<path d="M0 {y} Q225 {y - 6} 450 {y} Q675 {y + 6} 900 {y}"/>' for y in range(700, 1300, 22)) + '</g>')
    s.append('<g transform="translate(60 760)">' + kit.broadleaf(0, 0, 230, cols=('#C2452B', '#E0663A', '#9E3020'), seed=7) + '</g>')
    s.append(kit.leaves(W, 520, 900, n=8, seed=17, color='#D9542F'))
    fx, fy = 730, 735
    s.append(f'<ellipse cx="{fx}" cy="{fy + 12}" rx="80" ry="18" fill="#8E9298"/><ellipse cx="{fx}" cy="{fy + 10}" rx="66" ry="13" fill="url(#water)"/><ellipse class="a-ripple" cx="{fx - 30}" cy="{fy + 10}" rx="20" ry="5" fill="none" stroke="#CFEAF4" stroke-width="2"/>')
    s.append(kit.pebbles([(fx - 70, fy + 18, 12), (fx + 72, fy + 14, 10), (fx + 50, fy + 26, 9)]))
    s.append(f'<path d="M{fx + 40} {fy + 4} L{fx + 40} {fy - 44} M{fx + 60} {fy + 4} L{fx + 60} {fy - 44}" stroke="#7E6A3A" stroke-width="5"/><path d="M{fx + 96} {fy - 76} L{fx + 70} {fy - 62}" stroke="#9DB04A" stroke-width="9" stroke-linecap="round"/><path d="M{fx + 96} {fy - 76} L{fx + 98} {fy + 2}" stroke="#7E8A3A" stroke-width="6"/>')
    s.append(f'<g class="a-tip"><path d="M{fx + 4} {fy - 30} L{fx + 74} {fy - 54}" stroke="#A8BA52" stroke-width="12" stroke-linecap="round"/><path d="M{fx + 4} {fy - 30} L{fx + 74} {fy - 54}" stroke="#7E8A3A" stroke-width="2" stroke-dasharray="2 18"/></g><circle cx="{fx + 50}" cy="{fy - 44}" r="4" fill="#5E3920"/>')
    spots = []
    for row, (y, k, xs) in enumerate([(800, 0.55, (170, 340, 560, 730)), (960, 0.75, (130, 340, 560, 770)), (1160, 1.0, (150, 450, 750))]):
        for x in xs:
            spots.append((x, y, k))
    s.append('<g stroke="#C9C0AB" stroke-width="2" fill="none">' + ''.join(f'<ellipse cx="{x}" cy="{y}" rx="{90 * k:.0f}" ry="{24 * k:.0f}"/><ellipse cx="{x}" cy="{y}" rx="{112 * k:.0f}" ry="{32 * k:.0f}"/>' for x, y, k in spots) + '</g>')
    s.append('<g fill="#B6AE9C">' + ''.join(f'<ellipse cx="{x}" cy="{y}" rx="{r}" ry="{r * 0.4:.0f}"/>' for x, y, r in [(450, 1270, 34), (440, 1210, 26), (460, 1060, 22), (448, 1000, 20), (452, 880, 16), (448, 840, 14), (450, 760, 12)]) + '</g>')
    for i, (x, y, k) in enumerate(spots[:12]):
        r = 70 * k
        s.append(f'<g class="u" data-i="{i}" data-y="{y:.0f}">'
                 f'<g class="u-on"><ellipse cx="{x}" cy="{y + 4}" rx="{r * 1.2:.0f}" ry="{12 * k:.0f}" fill="#2B1E10" opacity="0.25"/>'
                 f'<path d="M{x - r:.0f} {y:.0f} Q{x - r * 1.05:.0f} {y - r * 1.1:.0f} {x - 10 * k:.0f} {y - r * 1.25:.0f} L{x - 4 * k:.0f} {y:.0f} Z" fill="url(#boulder)"/>'
                 f'<path d="M{x + 10 * k:.0f} {y:.0f} L{x + 16 * k:.0f} {y - r * 1.25:.0f} Q{x + r * 1.05:.0f} {y - r * 1.1:.0f} {x + r:.0f} {y:.0f} Z" fill="url(#boulder)"/>'
                 f'<path d="M{x - 10 * k:.0f} {y - r * 1.25:.0f} L{x - 4 * k:.0f} {y:.0f} L{x + 2 * k:.0f} {y:.0f} L{x - 2 * k:.0f} {y - r * 1.25:.0f} Z" fill="url(#cut)"/>'
                 f'<text class="u-label" x="{x + r * 0.5:.0f}" y="{y - r * 0.4:.0f}" text-anchor="middle" font-family="IBM Plex Mono, monospace" font-weight="600" font-size="{18 * k:.0f}" fill="#3A3D44"></text></g>'
                 f'<g class="u-ghost"><ellipse cx="{x}" cy="{y + 4}" rx="{r * 1.2:.0f}" ry="{12 * k:.0f}" fill="#2B1E10" opacity="0.25"/><path d="M{x - r:.0f} {y:.0f} Q{x - r:.0f} {y - r * 1.3:.0f} {x:.0f} {y - r * 1.3:.0f} Q{x + r:.0f} {y - r * 1.3:.0f} {x + r:.0f} {y:.0f} Z" fill="url(#boulder)"/>'
                 f'<path d="M{x - r * 0.7:.0f} {y - r * 0.92:.0f} Q{x:.0f} {y - r * 1.4:.0f} {x + r * 0.6:.0f} {y - r * 1.02:.0f} Q{x:.0f} {y - r * 1.22:.0f} {x - r * 0.7:.0f} {y - r * 0.92:.0f} Z" fill="#6E9B4A"/>'
                 f'<path d="M{x + r * 0.2:.0f} {y - r * 1.28:.0f} L{x + r * 0.2:.0f} {y - r * 1.8:.0f}" stroke="#4A2E1A" stroke-width="{3 * k:.1f}"/><path class="a-flag" d="M{x + r * 0.2:.0f} {y - r * 1.8:.0f} L{x + r * 0.2 + 28 * k:.0f} {y - r * 1.72:.0f} L{x + r * 0.2:.0f} {y - r * 1.62:.0f} Z" fill="#FFC21A"/></g>'
                 f'<ellipse class="u-off" cx="{x}" cy="{y - 2}" rx="{r:.0f}" ry="{18 * k:.0f}" fill="none" stroke="#9E9682" stroke-width="2" stroke-dasharray="6 5"/></g>')
    s.append(kit.toro(60, 1240, 1.6) + kit.toro(860, 1240, 1.6))
    s.append(kit.weather(W, H))
    s.append(kit.night(W, H, [(60, 1160, 80), (860, 1160, 80)]))
    s.append(kit.fireflies(0, 900, 700, 1250, 18))
    return svg('boulders', W, H, 'The boulder garden', ''.join(s))


if __name__ == '__main__':
    out = sys.argv[1]
    for name, fn in (('cliff', cliff), ('yard', yard), ('forge', forge), ('boulders', boulders)):
        open(f'{out}/{name}.svg', 'w').write(fn())
