import math, random, sys

W, H = 2400, 800

def pts(p):
    return ' '.join(f'{x:g},{y:g}' for x, y in p)

def defs():
    return '''<defs>
<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#6E9FCC"/><stop offset="0.5" stop-color="#B7CFE2"/><stop offset="0.82" stop-color="#F1DDBC"/><stop offset="1" stop-color="#F6CF9E"/></linearGradient>
<radialGradient id="sunglow" cx="0.5" cy="0.5" r="0.5"><stop offset="0" stop-color="#FFF4D2"/><stop offset="0.3" stop-color="#FFE3A8" stop-opacity="0.65"/><stop offset="1" stop-color="#FFE3A8" stop-opacity="0"/></radialGradient>
<linearGradient id="far" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#A3B3CF"/><stop offset="1" stop-color="#D8D9DF"/></linearGradient>
<linearGradient id="mid" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#7A92B2"/><stop offset="1" stop-color="#AEB9C6"/></linearGradient>
<linearGradient id="plateau" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#7A9294"/><stop offset="1" stop-color="#93A6A4"/></linearGradient>
<linearGradient id="haze" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#F3E3C8" stop-opacity="0"/><stop offset="1" stop-color="#F3E3C8" stop-opacity="0.7"/></linearGradient>
<linearGradient id="forestFar" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#557A73"/><stop offset="1" stop-color="#6C8C80"/></linearGradient>
<linearGradient id="forestNear" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#355E4C"/><stop offset="1" stop-color="#46705A"/></linearGradient>
<linearGradient id="ground" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#8DB262"/><stop offset="0.5" stop-color="#78A04F"/><stop offset="1" stop-color="#557E36"/></linearGradient>
<linearGradient id="hill" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#5F8A4C"/><stop offset="0.65" stop-color="#7EA75A"/><stop offset="1" stop-color="#9BC06B"/></linearGradient>
<linearGradient id="rock" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#5E636C"/><stop offset="0.55" stop-color="#80858E"/><stop offset="0.85" stop-color="#9A9EA5"/><stop offset="1" stop-color="#6A6F78"/></linearGradient>
<linearGradient id="wet" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#3F454E"/><stop offset="1" stop-color="#4E555E"/></linearGradient>
<linearGradient id="fall" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#BFE0EC"/><stop offset="0.35" stop-color="#F4FBFD"/><stop offset="0.7" stop-color="#E2F2F8"/><stop offset="1" stop-color="#A8D0E0"/></linearGradient>
<linearGradient id="water" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#6FAFC9"/><stop offset="1" stop-color="#4F8FAF"/></linearGradient>
<linearGradient id="dirt" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#D8BC8A"/><stop offset="1" stop-color="#C4A26E"/></linearGradient>
<linearGradient id="wood" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#6A4126"/><stop offset="0.5" stop-color="#A06C43"/><stop offset="1" stop-color="#5A361E"/></linearGradient>
<linearGradient id="plank" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#8C5D3A"/><stop offset="1" stop-color="#694128"/></linearGradient>
<linearGradient id="roof" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#424B60"/><stop offset="1" stop-color="#262B38"/></linearGradient>
<linearGradient id="wall" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#F6EDDB"/><stop offset="1" stop-color="#E1D3B8"/></linearGradient>
<linearGradient id="stone" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ABAFB5"/><stop offset="1" stop-color="#7E828A"/></linearGradient>
<linearGradient id="boulder" x1="1" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#B9BDC3"/><stop offset="0.5" stop-color="#8A8F96"/><stop offset="1" stop-color="#5C6067"/></linearGradient>
<linearGradient id="cut" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#DEE1E5"/><stop offset="1" stop-color="#B6BAC0"/></linearGradient>
<radialGradient id="coal" cx="0.5" cy="0.5" r="0.5"><stop offset="0" stop-color="#FFEDB0"/><stop offset="0.5" stop-color="#FF9A2E"/><stop offset="1" stop-color="#C2410C"/></radialGradient>
<radialGradient id="glow" cx="0.5" cy="0.5" r="0.5"><stop offset="0" stop-color="#FFC75A" stop-opacity="0.75"/><stop offset="1" stop-color="#FFC75A" stop-opacity="0"/></radialGradient>
<radialGradient id="mist" cx="0.5" cy="0.5" r="0.5"><stop offset="0" stop-color="#FFFFFF" stop-opacity="0.85"/><stop offset="1" stop-color="#FFFFFF" stop-opacity="0"/></radialGradient>
<g id="tuft"><path d="M-12 0 Q-10 -16 -5 -21 Q-5 -9 0 0 Q2 -19 7 -24 Q6 -9 12 0 Z" fill="#4C7A31"/></g>
<g id="tuftL"><path d="M-12 0 Q-10 -16 -5 -21 Q-5 -9 0 0 Q2 -19 7 -24 Q6 -9 12 0 Z" fill="#94C063"/></g>
<g id="reed"><path d="M0 0 Q-2 -30 -6 -46 M4 0 Q4 -34 8 -52 M-4 0 Q-8 -24 -14 -36" stroke="#5E7E3A" stroke-width="2.5" fill="none"/><ellipse cx="8" cy="-54" rx="2.5" ry="7" fill="#7A5A34"/></g>
<g id="toro"><rect x="-13" y="-6" width="26" height="6" fill="#8E9298"/><rect x="-5" y="-30" width="10" height="24" fill="#9A9EA4"/><rect x="-12" y="-34" width="24" height="5" fill="#7E828A"/><rect x="-9" y="-50" width="18" height="16" fill="#9A9EA4"/><rect x="-5" y="-46" width="10" height="9" fill="#F2B33D"/><path d="M-17 -50 L0 -62 L17 -50 Z" fill="#6E7278"/><rect x="-2" y="-67" width="4" height="6" fill="#6E7278"/></g>
</defs>'''

def ridge(x0, x1, base, amp, seed, step=18):
    random.seed(seed)
    out = []
    x = x0
    while x <= x1:
        out.append((x, base + amp * math.sin(x / 210 + seed) + amp * 0.5 * math.sin(x / 77 + seed * 2)))
        x += step
    return out

def forest(x0, x1, base_fn, hmin, hmax, seed, fill):
    random.seed(seed)
    p = [(x0, H)]
    x = x0
    while x <= x1:
        b = base_fn(x)
        h = random.uniform(hmin, hmax)
        w = h * 0.32
        p += [(x - w, b - h * 0.22), (x - w * 0.5, b - h * 0.55), (x - w * 0.62, b - h * 0.55), (x, b - h), (x + w * 0.62, b - h * 0.55), (x + w * 0.5, b - h * 0.55), (x + w, b - h * 0.22)]
        x += w * random.uniform(1.2, 1.7)
    p += [(x1, H)]
    return f'<polygon points="{pts(p)}" fill="{fill}"/>'

def pine(x, y, h, c1='#2F5B47', c2='#3E6F57', trunk='#4A3324'):
    w = h * 0.36
    body = [(x, y - h), (x + w * 0.55, y - h * 0.6), (x + w * 0.32, y - h * 0.6), (x + w * 0.8, y - h * 0.3), (x + w * 0.5, y - h * 0.3), (x + w, y - h * 0.06), (x - w, y - h * 0.06), (x - w * 0.5, y - h * 0.3), (x - w * 0.8, y - h * 0.3), (x - w * 0.32, y - h * 0.6), (x - w * 0.55, y - h * 0.6)]
    lit = [(x, y - h), (x + w * 0.55, y - h * 0.6), (x + w * 0.32, y - h * 0.6), (x + w * 0.8, y - h * 0.3), (x + w * 0.5, y - h * 0.3), (x + w, y - h * 0.06), (x + w * 0.1, y - h * 0.06)]
    return f'<rect x="{x - h * 0.03:g}" y="{y - h * 0.08:g}" width="{h * 0.06:g}" height="{h * 0.1:g}" fill="{trunk}"/><polygon points="{pts(body)}" fill="{c1}"/><polygon points="{pts(lit)}" fill="{c2}"/>'

def mountains():
    s = []
    far = [(0, 470), (120, 330), (210, 380), (340, 250), (430, 320), (560, 270), (690, 350), (820, 230), (930, 300), (1060, 260), (1180, 330), (1320, 210), (1450, 300), (1570, 255), (1700, 330), (1830, 240), (1960, 320), (2080, 270), (2210, 340), (2320, 290), (2400, 330), (2400, 560), (0, 560)]
    s.append(f'<polygon points="{pts(far)}" fill="url(#far)"/>')
    for (px, py), (lx, ly), (rx, ry) in [((340, 250), (210, 380), (430, 320)), ((820, 230), (690, 350), (930, 300)), ((1320, 210), (1180, 330), (1450, 300)), ((1830, 240), (1700, 330), (1960, 320))]:
        t = 0.33
        a = (px + (lx - px) * t, py + (ly - py) * t)
        b = (px + (rx - px) * t, py + (ry - py) * t)
        m1 = (px + (lx - px) * t * 0.6 + 8, py + (ly - py) * t * 0.85)
        m2 = (px + (rx - px) * t * 0.4, py + (ry - py) * t * 1.1)
        s.append(f'<polygon points="{pts([(px, py), b, m2, (px + 4, py + (ly - py) * t * 0.7), m1, a])}" fill="#EEF2F6" opacity="0.92"/>')
    mid = [(0, 520), (160, 400), (300, 460), (450, 380), (600, 450), (760, 390), (900, 470), (1060, 400), (1220, 470), (1380, 390), (1540, 460), (1700, 400), (1880, 470), (2040, 410), (2200, 470), (2400, 420), (2400, 600), (0, 600)]
    s.append(f'<polygon points="{pts(mid)}" fill="url(#mid)"/>')
    return ''.join(s)

def village():
    win = []
    s = [f'<path d="M520 560 Q560 492 610 474 L840 474 Q890 492 930 560 Z" fill="url(#plateau)"/>']
    col = '#647C8E'
    roofc = '#4F657A'
    y = 474
    for x, w, h in [(626, 26, 12), (660, 34, 14), (702, 22, 10), (748, 30, 13), (788, 26, 11), (818, 18, 9)]:
        s.append(f'<rect x="{x}" y="{y - h}" width="{w}" height="{h}" fill="{col}"/><path d="M{x - 4} {y - h} L{x + w / 2} {y - h - 9} L{x + w + 4} {y - h} Z" fill="{roofc}"/>')
        win.append(f'<rect x="{x + w / 2 - 2}" y="{y - h + 4}" width="4" height="4" fill="#FFD37A"/>')
    tx = 726
    s.append(f'<rect x="{tx}" y="{y - 46}" width="12" height="46" fill="{col}"/>')
    for i, yy in enumerate([y - 18, y - 32, y - 46]):
        w = 26 - i * 5
        s.append(f'<path d="M{tx + 6 - w} {yy} L{tx + 6} {yy - 8} L{tx + 6 + w} {yy} Z" fill="{roofc}"/>')
    s.append(f'<rect x="{tx + 5}" y="{y - 62}" width="2" height="9" fill="{roofc}"/>')
    s.append(f'<g id="w-vwin" display="none">{"".join(win)}</g>')
    return ''.join(s)

def cliff():
    top = [(0, 112), (50, 98), (110, 118), (170, 104), (206, 140), (232, 176), (300, 176), (326, 142), (360, 128), (404, 168)]
    face = [(414, 250), (402, 330), (428, 420), (416, 520), (446, 600), (440, 660), (0, 660)]
    s = [f'<polygon points="{pts(top + face)}" fill="url(#rock)"/>']
    s.append('<g stroke="#4B5058" stroke-width="2" fill="none" opacity="0.55"><path d="M16 190 L120 206 L190 194"/><path d="M8 290 L96 302 L180 290"/><path d="M340 300 L404 314"/><path d="M14 400 L160 414"/><path d="M340 450 L420 462"/><path d="M30 520 L150 530"/><path d="M350 560 L432 572"/></g>')
    s.append('<g fill="#A7ABB2" opacity="0.45"><path d="M340 210 L398 222 L404 242 L346 236 Z"/><path d="M40 330 L120 340 L114 360 L46 352 Z"/><path d="M356 380 L410 390 L414 408 L360 402 Z"/><path d="M90 450 L160 458 L156 474 L94 468 Z"/></g>')
    s.append('<path d="M0 112 L50 98 L110 118 L170 104 L206 140 L198 150 L170 120 L110 134 L50 114 L0 126 Z" fill="#5E8A4A"/><path d="M326 142 L360 128 L404 168 L398 178 L360 142 L330 156 Z" fill="#5E8A4A"/>')
    s.append('<path d="M406 172 Q416 210 410 250" stroke="#4C7639" stroke-width="3" fill="none"/><path d="M12 126 Q4 160 14 196" stroke="#4C7639" stroke-width="3" fill="none"/><path d="M196 152 Q206 190 200 226" stroke="#4C7639" stroke-width="2.5" fill="none"/>')
    s.append(pine(40, 102, 74) + pine(92, 112, 58) + pine(150, 110, 66) + pine(372, 136, 70))
    s.append('<path d="M228 178 Q214 300 218 420 Q204 520 206 630 L334 630 Q332 520 320 420 Q322 300 306 178 Z" fill="url(#wet)"/>')
    return ''.join(s)

def ragged(x0, y0, x1, y1, n, amp, seed):
    random.seed(seed)
    out = []
    for k in range(n + 1):
        f = k / n
        out.append((x0 + (x1 - x0) * f + (random.uniform(-amp, amp) if 0 < k < n else 0), y0 + (y1 - y0) * f))
    return out

def waterfall():
    random.seed(4)
    s = ['<path d="M246 144 Q266 138 288 144 Q296 160 304 176 L228 176 Q238 160 246 144 Z" fill="url(#water)"/><path d="M252 150 Q266 146 282 150" stroke="#CFEAF4" stroke-width="2" fill="none"/>']
    left = ragged(230, 176, 214, 612, 22, 2.5, 21)
    left = [(x - (0 if i < 2 else 3 * math.sin(i)), y) for i, (x, y) in enumerate(left)]
    right = ragged(302, 176, 324, 612, 22, 2.5, 22)
    sheet = [(230, 176), (266, 170), (302, 176)] + right[1:] + list(reversed(left[1:]))
    s.append(f'<polygon points="{pts(sheet)}" fill="url(#fall)"/>')
    s.append('<path d="M230 176 Q266 168 302 176 Q300 188 266 192 Q232 188 230 176 Z" fill="#F2FAFC"/>')
    for k in range(40):
        f = random.random()
        x0 = 232 + f * 68
        x1 = 216 + f * 106
        y0 = random.uniform(184, 300)
        y1 = random.uniform(y0 + 80, 600)
        xa = x0 + (x1 - x0) * (y0 - 176) / 436
        xb = x0 + (x1 - x0) * (y1 - 176) / 436
        s.append(f'<path class="a-fall a-d{k % 4}" d="M{xa:.1f} {y0:.0f} L{xb:.1f} {y1:.0f}" stroke="{random.choice(["#FFFFFF", "#FFFFFF", "#9ECBDD"])}" stroke-width="{random.choice([1, 1.5, 2, 2.5])}" opacity="{random.uniform(0.45, 0.95):.2f}"/>')
    s.append('<g fill="#666B74"><path d="M204 318 Q218 304 236 314 Q238 334 220 340 Q204 338 204 318 Z"/><path d="M306 452 Q322 438 340 450 Q340 470 322 474 Q306 472 306 452 Z"/></g>')
    s.append('<g fill="#8E939B"><path d="M210 316 Q220 308 232 314 Q220 318 214 326 Z"/><path d="M312 450 Q324 444 334 450 Q322 454 316 462 Z"/></g>')
    s.append('<g fill="#FFFFFF" opacity="0.92"><ellipse cx="236" cy="312" rx="16" ry="7"/><ellipse cx="244" cy="322" rx="10" ry="5"/><ellipse cx="306" cy="448" rx="16" ry="7"/><ellipse cx="298" cy="458" rx="10" ry="5"/></g>')
    s.append('<ellipse class="a-mist" cx="240" cy="318" rx="34" ry="16" fill="url(#mist)"/><ellipse class="a-mist a-d2" cx="304" cy="454" rx="34" ry="16" fill="url(#mist)"/>')
    s.append('<ellipse cx="300" cy="652" rx="160" ry="30" fill="url(#water)"/>')
    s.append('<path class="a-ripple" d="M150 654 Q300 684 452 650" stroke="#BFE3EF" stroke-width="2" fill="none" opacity="0.7"/><path class="a-ripple a-d2" d="M190 664 Q300 680 420 662" stroke="#BFE3EF" stroke-width="1.5" fill="none" opacity="0.5"/>')
    s.append('<ellipse class="a-mist" cx="270" cy="610" rx="130" ry="46" fill="url(#mist)"/><ellipse class="a-mist a-d1" cx="216" cy="590" rx="60" ry="30" fill="url(#mist)"/><ellipse class="a-mist a-d3" cx="330" cy="594" rx="70" ry="32" fill="url(#mist)"/>')
    s.append('<g class="a-foam" fill="#FFFFFF" opacity="0.92"><ellipse cx="270" cy="624" rx="66" ry="12"/><ellipse cx="214" cy="630" rx="24" ry="7"/><ellipse cx="326" cy="631" rx="28" ry="7"/></g>')
    s.append('<g fill="#6E737B"><ellipse cx="146" cy="660" rx="26" ry="11"/><ellipse cx="180" cy="676" rx="20" ry="9"/><ellipse cx="440" cy="664" rx="22" ry="10"/><ellipse cx="410" cy="680" rx="16" ry="7"/></g>')
    s.append('<g fill="#9A9EA5"><ellipse cx="142" cy="655" rx="18" ry="5"/><ellipse cx="438" cy="659" rx="14" ry="4"/></g>')
    return ''.join(s)

def stream():
    s = ['<path d="M420 646 Q520 650 600 676 Q690 706 740 740 Q790 772 812 800 L668 800 Q650 774 618 748 Q570 712 500 690 Q440 676 400 668 Z" fill="url(#water)"/>']
    s.append('<g stroke="#BFE3EF" stroke-width="2" fill="none" opacity="0.7" stroke-linecap="round"><path class="a-ripple" d="M470 664 Q520 670 556 684"/><path class="a-ripple a-d1" d="M600 700 Q640 716 668 736"/><path class="a-ripple a-d2" d="M700 760 Q720 774 734 790"/><path class="a-ripple a-d3" d="M640 726 Q666 744 680 760"/></g>')
    s.append('<g fill="#6E737B"><ellipse cx="600" cy="672" rx="10" ry="4"/><ellipse cx="760" cy="744" rx="12" ry="5"/><ellipse cx="640" cy="760" rx="10" ry="4"/></g>')
    s.append('<use href="#reed" x="440" y="680"/><use href="#reed" x="458" y="686"/><use href="#reed" x="790" y="752"/><use href="#reed" x="652" y="782"/><use href="#reed" x="560" y="662"/>')
    return ''.join(s)

def bridge():
    return ('<path d="M528 688 Q600 640 672 694 L672 704 Q600 654 528 698 Z" fill="#7A4A2C"/>'
            '<path d="M532 690 Q600 646 668 694" stroke="#A0683F" stroke-width="3" fill="none"/>'
            '<path d="M528 664 Q600 614 672 670" stroke="#5A361E" stroke-width="4" fill="none"/>'
            '<g stroke="#5A361E" stroke-width="3"><path d="M536 684 L536 660"/><path d="M566 664 L566 640"/><path d="M600 654 L600 630"/><path d="M634 662 L634 638"/><path d="M664 684 L664 662"/></g>'
            '<g stroke="#4A2E1A" stroke-width="4"><path d="M540 692 L540 718"/><path d="M660 696 L660 722"/></g>')

def yard():
    s = []
    for x, y, h in [(770, 690, 104), (820, 694, 92), (870, 690, 104)]:
        s.append(f'<ellipse cx="{x - 8}" cy="{y + 2}" rx="20" ry="5" fill="#2B1E10" opacity="0.28"/>')
        s.append(f'<rect x="{x - 9}" y="{y - h}" width="18" height="{h}" fill="url(#wood)"/><ellipse cx="{x}" cy="{y - h}" rx="9" ry="3.5" fill="#C08B5A"/>')
        s.append(f'<rect x="{x - 11}" y="{y - h + 22}" width="22" height="20" fill="#D8B878"/><path d="M{x - 11} {y - h + 28} H{x + 11} M{x - 11} {y - h + 35} H{x + 11}" stroke="#A88746" stroke-width="1.5"/>')
        s.append(f'<rect x="{x - 11}" y="{y - h + 62}" width="22" height="5" fill="#4A2E1A"/>')
    x, y = 930, 692
    s.append(f'<ellipse cx="{x - 8}" cy="{y + 2}" rx="22" ry="5" fill="#2B1E10" opacity="0.28"/>')
    s.append('<g id="w-dummy" class="dummy">')
    s.append(f'<rect x="{x - 5}" y="{y - 112}" width="10" height="112" fill="url(#wood)"/><rect x="{x - 26}" y="{y - 84}" width="52" height="9" fill="url(#wood)"/>')
    s.append(f'<path d="M{x - 15} {y - 96} Q{x} {y - 104} {x + 15} {y - 96} L{x + 18} {y - 30} Q{x} {y - 22} {x - 18} {y - 30} Z" fill="#D9BC7C"/>')
    s.append(f'<path d="M{x - 16} {y - 76} Q{x} {y - 70} {x + 16} {y - 76} M{x - 17} {y - 52} Q{x} {y - 46} {x + 17} {y - 52}" stroke="#A88746" stroke-width="2" fill="none"/>')
    s.append(f'<circle cx="{x}" cy="{y - 106}" r="12" fill="#D9BC7C"/><rect x="{x - 11}" y="{y - 112}" width="22" height="5" fill="#FFC21A"/><path d="M{x + 11} {y - 110} L{x + 24} {y - 115} L{x + 22} {y - 105} Z" fill="#FFC21A"/>')
    s.append('</g>')
    s.append('<g><rect x="958" y="650" width="4" height="42" fill="#5E3920"/><rect x="986" y="650" width="4" height="42" fill="#5E3920"/><rect x="956" y="658" width="36" height="4" fill="#6E4428"/><rect x="956" y="676" width="36" height="4" fill="#6E4428"/>'
             '<path d="M965 640 L967 690" stroke="#C9A46A" stroke-width="3"/><path d="M974 638 L975 690" stroke="#B88F55" stroke-width="3"/><path d="M983 640 L983 690" stroke="#C9A46A" stroke-width="3"/></g>')
    if True:
        s.append('<g id="w-postvines" display="none"><g stroke="#4C7A34" stroke-width="2.5" fill="none"><path d="M763 690 Q756 660 768 640 Q778 620 764 600"/><path d="M876 690 Q884 666 872 646"/></g><g fill="#5E8F3A"><circle cx="760" cy="664" r="4"/><circle cx="770" cy="636" r="4"/><circle cx="880" cy="668" r="4"/></g></g>')
    return ''.join(s)

def canopy(cols):
    out = ''
    for cx, cy, r in [(452, 532, 24), (486, 508, 30), (528, 520, 26), (468, 552, 20), (512, 546, 22), (494, 530, 24)]:
        out += f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{cols[0]}"/><circle cx="{cx + r * 0.35}" cy="{cy - r * 0.35}" r="{r * 0.6}" fill="{cols[1]}"/><circle cx="{cx - r * 0.4}" cy="{cy + r * 0.3}" r="{r * 0.45}" fill="{cols[2]}"/>'
    return out

def cherry():
    s = ['<path d="M486 640 Q480 600 492 570 Q500 548 488 524" stroke="#5B3A27" stroke-width="11" fill="none" stroke-linecap="round"/>',
         '<path d="M490 566 Q466 548 450 546" stroke="#5B3A27" stroke-width="5" fill="none" stroke-linecap="round"/><path d="M494 548 Q518 532 532 530" stroke="#5B3A27" stroke-width="5" fill="none" stroke-linecap="round"/>',
         '<path d="M488 524 Q480 506 470 500 M488 524 Q500 504 512 498 M450 546 Q440 536 436 526 M532 530 Q544 520 548 510" stroke="#5B3A27" stroke-width="3" fill="none" stroke-linecap="round"/>']
    s.append('<ellipse cx="480" cy="642" rx="40" ry="6" fill="#2B1E10" opacity="0.22"/>')
    s.append(f'<g id="w-cb">{canopy(("#F2AFC3", "#F9CDDA", "#E595AD"))}<g fill="#F2AFC3">' + ''.join(f'<ellipse class="a-petal a-d{i % 4} a-p{i % 3}" cx="{x}" cy="{y}" rx="3.5" ry="2.2"/>' for i, (x, y) in enumerate([(460, 540), (500, 520), (530, 545), (476, 560), (512, 500), (448, 525), (540, 528), (490, 552)])) + '</g></g>')
    s.append(f'<g id="w-cg" display="none">{canopy(("#5E9A4A", "#78B35C", "#4C8040"))}</g>')
    s.append(f'<g id="w-ca" display="none">{canopy(("#E0782F", "#F2A641", "#C2522B"))}<g fill="#E0782F">' + ''.join(f'<ellipse class="a-petal a-d{i % 4} a-p{i % 3}" cx="{x}" cy="{y}" rx="3.5" ry="2.2"/>' for i, (x, y) in enumerate([(460, 540), (520, 530), (480, 556), (500, 510)])) + '</g></g>')
    return ''.join(s)

def dojo():
    s = ['<ellipse cx="1190" cy="604" rx="230" ry="10" fill="#2B1E10" opacity="0.22"/>']
    s.append('<rect x="990" y="560" width="420" height="42" fill="url(#stone)"/>')
    s.append('<g stroke="#6E7278" stroke-width="1.5" opacity="0.85"><path d="M990 581 H1410"/><path d="M1040 560 V581 M1110 560 V581 M1180 560 V581 M1250 560 V581 M1320 560 V581 M1380 560 V581 M1010 581 V602 M1075 581 V602 M1145 581 V602 M1215 581 V602 M1285 581 V602 M1355 581 V602"/></g>')
    s.append('<path d="M1150 602 h100 v14 h12 v14 h-124 v-14 h12 Z" fill="#B8BCC1"/><path d="M1138 616 h124 M1150 602 h100" stroke="#8E9298" stroke-width="1.5"/>')
    s.append('<rect x="1006" y="548" width="388" height="13" fill="#7A4D2D"/><rect x="1006" y="548" width="388" height="3" fill="#A06C43"/>')
    s.append('<rect x="1040" y="430" width="320" height="120" fill="url(#wall)"/><rect x="1040" y="430" width="320" height="18" fill="#2B1E10" opacity="0.2"/>')
    s.append('<g fill="#6B4229">' + ''.join(f'<rect x="{x}" y="430" width="8" height="120"/>' for x in (1040, 1100, 1156, 1236, 1292, 1352)) + '<rect x="1040" y="430" width="320" height="7"/></g>')
    s.append('<g stroke="#A08A66" stroke-width="1.5">' + ''.join(f'<path d="M{a} 470 H{b} M{a} 510 H{b} M{(a + b) / 2} 437 V550"/>' for a, b in ((1048, 1100), (1108, 1156), (1244, 1292), (1300, 1352))) + '</g>')
    s.append('<rect x="1164" y="437" width="72" height="113" fill="#3B2A1E"/><rect x="1164" y="500" width="72" height="50" fill="#4E3A2A"/>')
    s.append('<path d="M1166 437 h33 v46 q-16 6 -33 0 Z" fill="#26324A"/><path d="M1201 437 h33 v46 q-16 6 -33 0 Z" fill="#26324A"/>')
    s.append('<g fill="#FFC21A"><rect x="1172" y="452" width="7" height="7"/><rect x="1181" y="452" width="7" height="7"/><rect x="1181" y="443" width="7" height="7"/><rect x="1209" y="452" width="7" height="7"/><rect x="1218" y="452" width="7" height="7"/><rect x="1218" y="443" width="7" height="7"/></g>')
    s.append('<rect x="1014" y="440" width="9" height="110" fill="url(#wood)"/><rect x="1377" y="440" width="9" height="110" fill="url(#wood)"/>')
    s.append('<path d="M966 446 Q1030 436 1058 382 L1342 382 Q1370 436 1434 446 Q1430 457 1414 455 Q1364 449 1344 398 L1056 398 Q1036 449 986 455 Q970 457 966 446 Z" fill="url(#roof)"/>')
    s.append('<g stroke="#4F5970" stroke-width="1.5" fill="none" opacity="0.8"><path d="M990 446 Q1040 438 1062 404 L1338 404 Q1360 438 1410 446"/><path d="M1020 440 Q1052 430 1068 412 L1332 412 Q1348 430 1380 440"/><path d="M1052 432 Q1068 424 1074 418 L1326 418 Q1332 424 1348 432"/></g>')
    s.append('<path d="M1058 382 Q1112 332 1200 318 Q1288 332 1342 382 Z" fill="url(#roof)"/>')
    s.append('<g stroke="#4F5970" stroke-width="1.5" opacity="0.8"><path d="M1090 378 Q1140 344 1200 334 Q1260 344 1310 378"/><path d="M1124 380 Q1160 356 1200 348 Q1240 356 1276 380"/></g>')
    s.append('<path d="M1080 382 Q1124 344 1200 328 Q1276 344 1320 382" stroke="#5E6984" stroke-width="3" fill="none"/>')
    s.append('<rect x="1168" y="310" width="64" height="11" fill="#262B38"/><path d="M1162 313 l-9 -9 M1238 313 l9 -9" stroke="#262B38" stroke-width="6" stroke-linecap="round"/>')
    s.append('<rect x="1182" y="356" width="36" height="22" fill="#5E3920"/><rect x="1186" y="359" width="28" height="16" fill="#F6EDDB"/><g fill="#1D1E21"><rect x="1191" y="367" width="5" height="5"/><rect x="1197" y="367" width="5" height="5"/><rect x="1197" y="361" width="5" height="5"/><rect x="1203" y="367" width="5" height="5"/><rect x="1203" y="361" width="5" height="5"/></g>')
    for lx in (1030, 1370):
        s.append(f'<g class="a-sway a-d{lx % 3}"><path d="M{lx} 452 L{lx} 464" stroke="#3B2A1E" stroke-width="2"/><rect x="{lx - 11}" y="464" width="22" height="28" rx="9" fill="#F2B33D"/><path d="M{lx - 11} 473 H{lx + 11} M{lx - 11} 482 H{lx + 11}" stroke="#C9851B" stroke-width="1.5"/><rect x="{lx - 6}" y="461" width="12" height="4" fill="#3B2A1E"/><rect x="{lx - 6}" y="491" width="12" height="4" fill="#3B2A1E"/><rect class="n-only" x="{lx - 11}" y="464" width="22" height="28" rx="9" fill="#FFD37A"/></g>')
    s.append('<path d="M1452 606 L1452 360" stroke="#4A2E1A" stroke-width="5"/><g class="a-flag"><path d="M1454 366 L1494 366 L1494 520 L1474 508 L1454 520 Z" fill="#FFC21A"/>'
             '<g fill="#1D1E21"><rect x="1462" y="410" width="7" height="7"/><rect x="1471" y="410" width="7" height="7"/><rect x="1471" y="401" width="7" height="7"/><rect x="1480" y="410" width="7" height="7"/><rect x="1480" y="401" width="7" height="7"/><rect x="1480" y="392" width="7" height="7"/></g></g><path d="M1454 366 L1494 366" stroke="#4A2E1A" stroke-width="4"/>')
    s.append('<use href="#toro" x="1120" y="640"/><use href="#toro" x="1280" y="640"/>')
    s.append('<g id="w-floor2" display="none"><rect x="1124" y="238" width="152" height="78" fill="url(#wall)"/><g fill="#6B4229"><rect x="1124" y="238" width="7" height="78"/><rect x="1269" y="238" width="7" height="78"/><rect x="1196" y="238" width="8" height="78"/><rect x="1124" y="238" width="152" height="6"/></g><g stroke="#A08A66" stroke-width="1.5"><path d="M1131 266 H1196 M1131 292 H1196 M1204 266 H1269 M1204 292 H1269 M1163 244 V316 M1236 244 V316"/></g>'
             '<path d="M1086 244 Q1120 238 1134 214 L1266 214 Q1280 238 1314 244 Q1312 252 1300 250 Q1276 246 1262 226 L1138 226 Q1124 246 1100 250 Q1088 252 1086 244 Z" fill="url(#roof)"/><path d="M1134 214 Q1166 186 1200 180 Q1234 186 1266 214 Z" fill="url(#roof)"/><rect x="1178" y="174" width="44" height="9" fill="#262B38"/>'
             '<path d="M1290 250 L1290 262" stroke="#3B2A1E" stroke-width="2"/><rect x="1281" y="262" width="18" height="22" rx="7" fill="#F2B33D"/></g>')
    if True:
        s.append('<g id="w-floor2-ghost" display="none"><g fill="#FFFFFF" fill-opacity="0.2" stroke="#1D1E21" stroke-opacity="0.7" stroke-width="2.5" stroke-dasharray="8 6"><rect x="1120" y="226" width="160" height="70"/><path d="M1076 232 Q1120 226 1136 196 L1264 196 Q1280 226 1324 232 Z"/><path d="M1136 196 Q1170 168 1200 160 Q1230 168 1264 196 Z"/></g></g>')
    return ''.join(s)

def boulders():
    s = ['<g id="w-split1" display="none"><ellipse cx="1590" cy="740" rx="90" ry="9" fill="#2B1E10" opacity="0.28"/>']
    s.append('<path d="M1520 738 Q1506 676 1540 640 L1568 632 L1556 738 Z" fill="url(#boulder)"/><path d="M1568 632 L1556 738 L1566 738 L1578 634 Z" fill="url(#cut)"/>')
    s.append('<path d="M1592 738 L1602 628 Q1640 626 1656 662 Q1668 704 1650 738 Z" fill="url(#boulder)"/><path d="M1602 628 L1592 738 L1582 738 L1592 630 Z" fill="url(#cut)"/>')
    s.append('<path d="M1540 640 L1568 632 L1552 638 Z M1602 628 Q1632 624 1650 650 Q1630 636 1606 640 Z" fill="#6E9B4A"/>')
    s.append('<g fill="#FFC21A"><rect x="1618" y="680" width="9" height="9"/><rect x="1628" y="680" width="9" height="9"/><rect x="1628" y="670" width="9" height="9"/></g></g>')
    s.append('<g id="w-split2" display="none"><ellipse cx="1912" cy="748" rx="62" ry="7" fill="#2B1E10" opacity="0.28"/>'
             '<path d="M1866 746 Q1856 704 1880 680 L1900 674 L1892 746 Z" fill="url(#boulder)"/><path d="M1900 674 L1892 746 L1899 746 L1907 676 Z" fill="url(#cut)"/>'
             '<path d="M1916 746 L1922 672 Q1950 670 1960 696 Q1968 724 1956 746 Z" fill="url(#boulder)"/><path d="M1922 672 L1916 746 L1909 746 L1915 674 Z" fill="url(#cut)"/>'
             '<path d="M1880 680 L1900 674 L1888 678 Z M1922 672 Q1944 668 1956 688 Q1942 678 1924 682 Z" fill="#6E9B4A"/></g>')
    s.append('<g id="w-bosswait" display="none"><ellipse cx="1760" cy="720" rx="64" ry="7" fill="#2B1E10" opacity="0.26"/>')
    s.append('<path d="M1706 718 Q1690 658 1726 628 Q1764 608 1798 634 Q1826 668 1812 718 Z" fill="url(#boulder)"/><path d="M1726 628 Q1764 608 1798 634 Q1766 624 1730 640 Z" fill="#6E9B4A"/><path d="M1734 676 q22 -12 46 2" stroke="#5D6168" stroke-width="2" fill="none"/>')
    s.append('<path d="M1762 616 L1762 588" stroke="#4A2E1A" stroke-width="3"/><path class="a-flag" d="M1763 589 L1786 595 L1763 602 Z" fill="#FFC21A"/></g>')
    return ''.join(s)

HILL = [(1540, 606), (1600, 576), (1652, 542), (1700, 504), (1742, 466), (1782, 432), (1822, 402), (1852, 372), (1872, 340), (1880, 326), (1990, 326), (2002, 338), (2026, 368), (2060, 392), (2096, 432), (2136, 510), (2180, 606)]

def smooth(points, n=8):
    out = []
    p = [points[0]] + points + [points[-1]]
    for i in range(1, len(p) - 2):
        p0, p1, p2, p3 = p[i - 1], p[i], p[i + 1], p[i + 2]
        for k in range(n):
            t = k / n
            t2, t3 = t * t, t * t * t
            x = 0.5 * (2 * p1[0] + (-p0[0] + p2[0]) * t + (2 * p0[0] - 5 * p1[0] + 4 * p2[0] - p3[0]) * t2 + (-p0[0] + 3 * p1[0] - 3 * p2[0] + p3[0]) * t3)
            y = 0.5 * (2 * p1[1] + (-p0[1] + p2[1]) * t + (2 * p0[1] - 5 * p1[1] + 4 * p2[1] - p3[1]) * t2 + (-p0[1] + 3 * p1[1] - 3 * p2[1] + p3[1]) * t3)
            out.append((x, y))
    out.append(points[-1])
    return out

HILL_S = smooth(HILL)

def surface(x, curve=None):
    c = curve or HILL_S
    if x <= c[0][0] or x >= c[-1][0]:
        return 9999
    for (x0, y0), (x1, y1) in zip(c, c[1:]):
        if x0 <= x <= x1:
            return y0 + (y1 - y0) * (x - x0) / (x1 - x0 or 1)
    return 9999

PLACED = []

def rest(name, x0, x1, base, margin=0):
    top = min(surface(x) for x in range(int(x0), int(x1) + 1))
    if base < top + margin:
        raise SystemExit(f'{name} floats: base {base:.1f} is above the hill at {top:.1f}')
    PLACED.append(name)

HILL_STEPS = []

def hill():
    moss = []
    s = [f'<polygon points="{pts(HILL_S)}" fill="url(#hill)"/>']
    lit = [p for p in HILL_S if p[0] >= 1990]
    s.append(f'<polygon points="{pts(lit + [(2140, 606)] + [(x - 26 * (606 - y) / 280, y) for x, y in reversed(lit)])}" fill="#A8CB76" opacity="0.45"/>')
    legs = [((1664, 608), (1822, 570), 10), ((1822, 570), (1752, 500), 9), ((1752, 500), (1858, 426), 10), ((1858, 426), (1904, 330), 10)]
    steps = []
    n = 0
    for (x0, y0), (x1, y1), k in legs:
        for t in range(k):
            f = t / k
            depth = n / 35
            w = 44 - depth * 18
            h = 9.5 - depth * 3.5
            x = x0 + (x1 - x0) * f - w / 2
            y = y0 + (y1 - y0) * f
            rest(f'step {n}', x, x + w, y, 3)
            steps.append((x, y, w, h))
            HILL_STEPS.append((x, y, w, h))
            n += 1
    for i, (x, y, w, h) in enumerate(steps):
        s.append(f'<rect x="{x:.1f}" y="{y - h:.1f}" width="{w:.1f}" height="{h:.1f}" fill="url(#stone)"/><rect x="{x:.1f}" y="{y - 1.6:.1f}" width="{w:.1f}" height="1.6" fill="#5A5E65"/>')
        if True:
            moss.append(f'<ellipse cx="{x + w * 0.45 + (i % 3) * 3:.1f}" cy="{y - h + 1:.1f}" rx="{w * 0.3:.1f}" ry="2.8" fill="#5E8F3A"/>')
            if i % 2 == 0:
                moss.append(f'<use href="#tuftL" transform="translate({x + w:.1f} {y:.1f}) scale({0.9 - i / 60:.2f})"/>')
    s.append(f'<g id="w-moss" display="none">{"".join(moss)}</g>')
    for i in (4, 13, 22, 33):
        x, y, w, h = steps[i]
        sc = 0.8 - i * 0.012
        rest(f'lantern {i}', x - 4 - 13 * sc, x - 4 + 13 * sc, y, 2)
        s.append(f'<g transform="translate({x - 4:.1f} {y:.1f}) scale({sc:.2f})"><use href="#toro"/></g>')
    for tx, h in [(1700, 58), (1790, 40), (1840, 44), (2004, 56), (2064, 70), (2112, 50)]:
        base = surface(tx) + (h * 0.5 if tx < 1880 or tx > 1990 else 30)
        base = max(base, surface(tx) + 8)
        rest(f'tree {tx}', tx - 2, tx + 2, base, 4)
        s.append(pine(tx, base, h))
    gx, gy = 1935, 326
    rest('gate', gx - 60, gx + 60, gy)
    s.append(f'<rect x="{gx - 62}" y="{gy - 4}" width="124" height="8" fill="url(#stone)"/><rect x="{gx - 56}" y="{gy - 10}" width="20" height="8" fill="#8E9298"/><rect x="{gx + 36}" y="{gy - 10}" width="20" height="8" fill="#8E9298"/>')
    s.append(f'<rect x="{gx - 50}" y="{gy - 112}" width="9" height="104" fill="#3A2416"/><rect x="{gx + 41}" y="{gy - 112}" width="9" height="104" fill="#3A2416"/>')
    s.append(f'<path d="M{gx - 66} {gy - 120} Q{gx} {gy - 132} {gx + 66} {gy - 120} L{gx + 64} {gy - 110} Q{gx} {gy - 120} {gx - 64} {gy - 110} Z" fill="#3A2416"/>')
    s.append(f'<rect x="{gx - 56}" y="{gy - 98}" width="112" height="7" fill="#3A2416"/><rect x="{gx - 12}" y="{gy - 110}" width="24" height="12" fill="#FFC21A"/>')
    if True:
        s.append(f'<g id="w-gatevines" display="none"><g stroke="#4C7A34" stroke-width="3" fill="none"><path d="M{gx - 46} {gy - 8} Q{gx - 54} {gy - 38} {gx - 44} {gy - 62} Q{gx - 36} {gy - 84} {gx - 48} {gy - 104}"/><path d="M{gx + 46} {gy - 8} Q{gx + 54} {gy - 42} {gx + 44} {gy - 68}"/></g>')
        s.append(f'<g fill="#5E8F3A"><circle cx="{gx - 52}" cy="{gy - 38}" r="5"/><circle cx="{gx - 42}" cy="{gy - 66}" r="5"/><circle cx="{gx - 48}" cy="{gy - 92}" r="4"/><circle cx="{gx + 52}" cy="{gy - 42}" r="5"/></g></g>')
    return ''.join(s)

def forge():
    s = ['<ellipse cx="2200" cy="616" rx="150" ry="9" fill="#2B1E10" opacity="0.22"/>']
    s.append('<rect x="2100" y="486" width="200" height="126" fill="url(#plank)"/><g stroke="#55361F" stroke-width="1.5">' + ''.join(f'<path d="M2100 {y} H2300"/>' for y in (508, 530, 552, 574, 596)) + '</g>')
    s.append('<rect x="2094" y="486" width="10" height="126" fill="url(#wood)"/><rect x="2296" y="486" width="10" height="126" fill="url(#wood)"/>')
    s.append('<path d="M2070 494 L2330 452 L2334 468 L2074 512 Z" fill="#4B3A2C"/><path d="M2070 494 L2330 452" stroke="#6B5544" stroke-width="2"/>')
    s.append('<rect x="2250" y="420" width="26" height="54" fill="#7E828A"/><rect x="2246" y="414" width="34" height="8" fill="#5F636A"/>')
    s.append('<g id="w-fire"><g fill="#E9EAEC" opacity="0.7"><circle class="a-smoke" cx="2264" cy="396" r="11"/><circle class="a-smoke a-d1" cx="2274" cy="372" r="14"/><circle class="a-smoke a-d2" cx="2262" cy="344" r="17"/><circle class="a-smoke a-d3" cx="2280" cy="312" r="20"/><circle class="a-smoke a-d4" cx="2266" cy="276" r="22"/></g>')
    s.append('<circle cx="2236" cy="570" r="70" fill="url(#glow)" opacity="0.6"/></g>')
    s.append('<rect x="2200" y="548" width="76" height="64" fill="#8C9096"/><g stroke="#6E7278" stroke-width="1.5"><path d="M2200 568 H2276 M2200 588 H2276 M2238 548 V568 M2222 568 V588 M2256 568 V588"/></g><ellipse cx="2238" cy="550" rx="28" ry="7" fill="#4A4D55"/><g id="w-coals"><ellipse class="a-glow" cx="2238" cy="550" rx="28" ry="7" fill="url(#coal)"/></g>')
    s.append('<rect x="2128" y="578" width="30" height="34" fill="#6E4428"/><ellipse cx="2143" cy="578" rx="15" ry="4" fill="#A06C43"/>')
    s.append('<path d="M2120 556 h46 l-6 11 h-9 v11 h-16 v-11 h-9 Z" fill="#2E3035"/><path d="M2122 556 h42" stroke="#5F636A" stroke-width="2"/>')
    s.append('<path d="M2170 524 L2186 548" stroke="#6E4428" stroke-width="5" stroke-linecap="round"/><rect x="2162" y="516" width="18" height="10" fill="#3A3C42" transform="rotate(30 2171 521)"/>')
    s.append('<ellipse cx="2068" cy="606" rx="15" ry="5" fill="#5F636A"/><rect x="2054" y="578" width="28" height="28" fill="#6E4428"/><ellipse cx="2068" cy="578" rx="14" ry="4" fill="#8FC4D8"/>')
    return ''.join(s)

def road(points, w0, w1, fill='#D7BA88', edge='#B8975F'):
    n = len(points)
    left, right = [], []
    for k, (x, y) in enumerate(points):
        a = points[max(0, k - 1)]
        b = points[min(n - 1, k + 1)]
        dx, dy = b[0] - a[0], b[1] - a[1]
        L = math.hypot(dx, dy) or 1
        nx, ny = -dy / L, dx / L
        w = (w0 + (w1 - w0) * k / (n - 1)) / 2
        left.append((x + nx * w, y + ny * w))
        right.append((x - nx * w, y - ny * w))
    poly = left + list(reversed(right))
    out = f'<polygon points="{pts(poly)}" fill="{edge}"/>'
    left2, right2 = [], []
    for k, (x, y) in enumerate(points):
        a = points[max(0, k - 1)]
        b = points[min(n - 1, k + 1)]
        dx, dy = b[0] - a[0], b[1] - a[1]
        L = math.hypot(dx, dy) or 1
        nx, ny = -dy / L, dx / L
        w = (w0 + (w1 - w0) * k / (n - 1)) / 2 - 2.5
        left2.append((x + nx * w, y + ny * w))
        right2.append((x - nx * w, y - ny * w))
    out += f'<polygon points="{pts(left2 + list(reversed(right2)))}" fill="{fill}"/>'
    return out

def curve(p0, p1, p2, n=14):
    return [((1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * p1[0] + t * t * p2[0], (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * p1[1] + t * t * p2[1]) for t in [k / n for k in range(n + 1)]]

def paths():
    s = []
    s.append(road(curve((2140, 618), (1900, 626), (1664, 612)), 22, 24))
    s.append(road(curve((1664, 612), (1440, 630), (1240, 632)), 24, 26))
    s.append(road(curve((1214, 704), (960, 714), (690, 702)), 34, 28))
    s.append(road(curve((524, 698), (480, 690), (436, 676)), 24, 20))
    s.append(road(curve((1210, 800), (1222, 700), (1200, 634)), 120, 64))
    s.append('<g fill="#C6A673" opacity="0.8"><ellipse cx="1190" cy="760" rx="16" ry="4"/><ellipse cx="1226" cy="704" rx="10" ry="3"/><ellipse cx="900" cy="708" rx="9" ry="2.5"/><ellipse cx="1500" cy="630" rx="8" ry="2"/><ellipse cx="1960" cy="622" rx="7" ry="2"/></g>')
    return ''.join(s)

def foreground():
    random.seed(11)
    s = ['<path d="M0 742 Q300 724 620 744 L700 800 L0 800 Z" fill="#4E7A31" opacity="0.55"/><path d="M1260 770 Q1700 740 2400 756 L2400 800 L1260 800 Z" fill="#4E7A31" opacity="0.55"/>']
    spots = [(random.uniform(0, 2400), random.uniform(640, 795)) for _ in range(140)]
    for x, y in spots:
        if 1130 < x < 1280 and y > 620: continue
        if 640 < x < 830 and y > 700: continue
        sc = 0.6 + (y - 640) / 160 * 0.8
        s.append(f'<use href="#{random.choice(["tuft", "tuft", "tuftL"])}" transform="translate({x:.0f} {y:.0f}) scale({sc:.2f})"/>')
    for x, y in [(80, 720), (1020, 760), (1460, 790), (1900, 770), (2200, 740), (380, 780)]:
        s.append(f'<ellipse cx="{x}" cy="{y}" rx="18" ry="8" fill="#7E828A"/><ellipse cx="{x - 4}" cy="{y - 3}" rx="12" ry="4" fill="#9EA2A8"/>')
    for x, y in [(120, 740), (340, 760), (980, 770), (1500, 776), (2080, 780), (2300, 760)]:
        s.append(f'<circle cx="{x}" cy="{y}" r="3.5" fill="#FFC21A"/><circle cx="{x + 12}" cy="{y + 6}" r="3" fill="#F7F1E3"/>')
    s.append(f'<g class="a-tree">{pine(2380, 812, 520, "#254536", "#2F5644", "#3E2A1C")}</g>')
    s.append('<path d="M0 800 L0 700 Q30 720 44 800 Z" fill="#3B6A2A"/>')
    return ''.join(s)

def sky():
    random.seed(3)
    s = ['<rect width="2400" height="800" fill="url(#sky)"/>']
    s.append('<g id="w-sun"><circle cx="1980" cy="190" r="220" fill="url(#sunglow)"/><circle cx="1980" cy="190" r="52" fill="#FFF6DC"/></g>')
    s.append('<g id="w-nightsky" display="none"><rect width="2400" height="800" fill="#16224A" opacity="0.75"/>')
    s.append(''.join(f'<circle class="{"a-twinkle a-d" + str(i % 4) if i % 3 == 0 else ""}" cx="{random.randint(0, 2400)}" cy="{random.randint(6, 330)}" r="{random.choice([1, 1, 1.4, 1.8])}" fill="#FFFFFF" opacity="{random.choice([0.5, 0.7, 0.95])}"/>' for i in range(120)))
    s.append('<circle cx="1980" cy="150" r="120" fill="url(#sunglow)" opacity="0.3"/><mask id="mm"><rect width="2400" height="800" fill="#FFFFFF"/><circle id="w-moonshadow" cx="1998" cy="136" r="38" fill="#000000"/></mask><circle cx="1980" cy="150" r="42" fill="#FFF3C9" mask="url(#mm)"/></g>')
    s.append('<g fill="#FFFFFF" opacity="0.9"><g class="a-cloud"><ellipse cx="620" cy="110" rx="120" ry="16"/><ellipse cx="690" cy="96" rx="64" ry="20"/><ellipse cx="560" cy="100" rx="50" ry="14"/></g><g class="a-cloud a-c2"><ellipse cx="1420" cy="80" rx="140" ry="15"/><ellipse cx="1500" cy="66" rx="70" ry="20"/><ellipse cx="1360" cy="70" rx="46" ry="13"/></g><g class="a-cloud a-c3"><ellipse cx="2200" cy="120" rx="80" ry="12"/></g></g>')
    s.append('<g fill="#FFFFFF" opacity="0.54"><g class="a-cloud a-c3"><ellipse cx="1000" cy="200" rx="140" ry="8"/></g><g class="a-cloud a-c2"><ellipse cx="1760" cy="250" rx="120" ry="7"/></g></g>')
    s.append('<g id="w-birds" fill="none" stroke="#45506A" stroke-width="2" stroke-linecap="round"><g class="a-birds"><path class="a-flap" d="M1580 160 q7 -7 14 0 q7 -7 14 0"/><path class="a-flap a-d1" d="M1616 178 q5 -5 10 0 q5 -5 10 0"/><path class="a-flap a-d2" d="M1556 186 q4 -4 8 0 q4 -4 8 0"/></g></g>')
    return ''.join(s)

def night_overlay():
    s = ['<g id="w-night" display="none"><rect width="2400" height="800" fill="#0D1636" opacity="0.55"/>']
    for x, y, r in [(1030, 478, 50), (1370, 478, 50), (1120, 597, 26), (1280, 597, 26), (1200, 500, 90)]:
        s.append(f'<circle class="a-glow a-d{x % 4}" cx="{x}" cy="{y}" r="{r}" fill="url(#glow)"/>')
    s.append('<rect x="1164" y="480" width="72" height="70" fill="#FFC75A" opacity="0.4"/>')
    s.append('<rect x="1115" y="594" width="10" height="9" fill="#FFD37A"/><rect x="1275" y="594" width="10" height="9" fill="#FFD37A"/>')
    s.append('<g id="w-nightfire"><circle cx="2238" cy="556" r="110" fill="url(#glow)"/><ellipse cx="2238" cy="550" rx="28" ry="7" fill="url(#coal)"/></g>')
    s.append('<path class="a-flag" d="M1454 366 L1494 366 L1494 520 L1474 508 L1454 520 Z" fill="#FFC21A" opacity="0.55"/>')
    random.seed(9)
    s.append(''.join(f'<circle class="a-fly a-d{i % 5}" cx="{random.uniform(420, 2300):.0f}" cy="{random.uniform(560, 760):.0f}" r="{random.choice([1.5, 2, 2.4])}" fill="#D7F58A" opacity="0.9"/>' for i in range(26)))
    s.append('</g>')
    return ''.join(s)

def atmosphere():
    random.seed(77)
    s = ['<defs><linearGradient id="duskg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#5E4A86" stop-opacity="0.35"/><stop offset="0.45" stop-color="#FF8A50" stop-opacity="0.35"/><stop offset="0.75" stop-color="#FFB86B" stop-opacity="0.18"/><stop offset="1" stop-color="#FF9A50" stop-opacity="0.1"/></linearGradient>'
         '<linearGradient id="pinkg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FF7EB0" stop-opacity="0.35"/><stop offset="0.6" stop-color="#FFB3C9" stop-opacity="0.3"/><stop offset="1" stop-color="#FFD9C2" stop-opacity="0.08"/></linearGradient></defs>']
    s.append('<g id="w-dusk" display="none"><rect width="2400" height="800" fill="url(#duskg)"/></g>')
    s.append('<g id="w-pink" display="none"><rect width="2400" height="800" fill="url(#pinkg)"/></g>')
    s.append('<g id="w-monsoon" display="none"><rect y="560" width="2400" height="240" fill="#2F8F3A" opacity="0.1"/></g>')
    s.append('<g id="w-leaves" display="none" fill="#E0782F">' + ''.join(f'<ellipse cx="{x}" cy="{y}" rx="4" ry="2.4" transform="rotate({random.randint(0, 180)} {x} {y})"/>' for x, y in [(450, 650), (470, 660), (520, 648), (560, 680), (600, 690), (1180, 700), (1240, 760), (900, 712), (980, 708), (700, 706)]) + '</g>')
    clouds = ''.join(f'<g class="a-cloud a-c{k % 3 + 1}"><ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{rx * 0.22:.0f}"/><ellipse cx="{x + rx * 0.4:.0f}" cy="{y - rx * 0.12:.0f}" rx="{rx * 0.55:.0f}" ry="{rx * 0.24:.0f}"/></g>' for k, (x, y, rx) in enumerate([(200, 120, 220), (720, 90, 260), (1260, 130, 240), (1760, 100, 280), (2260, 140, 220)]))
    s.append(f'<g id="w-cloudy" display="none"><rect width="2400" height="800" fill="#7E8A9A" opacity="0.22"/><g fill="#C3CAD4" opacity="0.95">{clouds}</g></g>')
    s.append('<defs><linearGradient id="fogband" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#F2F5F8" stop-opacity="0"/><stop offset="0.5" stop-color="#F2F5F8" stop-opacity="0.75"/><stop offset="1" stop-color="#F2F5F8" stop-opacity="0"/></linearGradient>'
             '<radialGradient id="puff" cx="0.5" cy="0.5" r="0.5"><stop offset="0" stop-color="#FFFFFF" stop-opacity="1"/><stop offset="1" stop-color="#FFFFFF" stop-opacity="0"/></radialGradient></defs>')
    s.append('<g id="w-fog" display="none"><rect width="2400" height="800" fill="#E6EBF0" opacity="0.28"/><g class="a-cloud"><rect x="-100" y="430" width="2600" height="120" fill="url(#fogband)"/></g><g class="a-cloud a-c2"><rect x="-100" y="540" width="2600" height="90" fill="url(#fogband)"/></g><g class="a-cloud a-c3"><rect x="-100" y="360" width="2600" height="80" fill="url(#fogband)" opacity="0.7"/></g></g>')
    rain = []
    for col in range(110):
        x = col * 22 + random.uniform(0, 18)
        y0 = random.uniform(0, 80)
        for k in range(-1, 11):
            y = y0 + k * 80
            rain.append(f'M{x:.0f} {y:.0f} l-5 18')
    s.append(f'<g id="w-rain" display="none"><rect width="2400" height="800" fill="#4A5566" opacity="0.3"/><path class="a-rain" d="{" ".join(rain)}" stroke="#DCE6F0" stroke-width="1.4" opacity="0.55"/>'
             '<g fill="#9FC6DA" opacity="0.55"><ellipse cx="1200" cy="740" rx="40" ry="6"/><ellipse cx="930" cy="712" rx="26" ry="4"/><ellipse cx="1500" cy="632" rx="22" ry="3"/><ellipse cx="1214" cy="672" rx="20" ry="3"/></g>'
             '<rect class="a-flash" id="w-flash" width="2400" height="800" fill="#FFFFFF" opacity="0"/></g>')
    snow = []
    for col in range(90):
        x = col * 27 + random.uniform(0, 20)
        y0 = random.uniform(0, 100)
        for k in range(-1, 9):
            snow.append(f'<circle cx="{x + random.uniform(-6, 6):.0f}" cy="{y0 + k * 100:.0f}" r="{random.choice([1.5, 2, 2.5])}"/>')
    s.append(f'<g id="w-snow" display="none"><rect width="2400" height="800" fill="#DDE5EE" opacity="0.2"/><g class="a-snow" fill="#FFFFFF" opacity="0.85">{"".join(snow)}</g></g>')
    random.seed(88)
    cols = ['#FF4FA3', '#3FCB6B', '#FFC21A', '#4F8BFF', '#FF7A2E']
    holi = ''
    for x, y, r in [(1560, 712, 20), (1610, 690, 14), (1640, 726, 16), (1760, 680, 18), (1790, 702, 12), (772, 650, 10), (820, 656, 10), (868, 650, 10), (1190, 752, 26), (1236, 724, 18), (1168, 706, 16), (980, 712, 14), (1320, 634, 12), (1460, 640, 12), (700, 706, 12)]:
        c = random.choice(cols)
        holi += ''.join(f'<circle cx="{x + random.uniform(-r, r):.0f}" cy="{y + random.uniform(-r, r) * 0.35:.0f}" r="{random.uniform(r * 0.25, r * 0.6):.1f}" fill="{c}" opacity="0.85"/>' for _ in range(6))
    puffs = ''
    for k, (x, y) in enumerate([(800, 600), (1180, 650), (1580, 640), (1780, 620)]):
        c = cols[k % len(cols)]
        puffs += f'<g class="a-smoke a-d{k % 4}"><circle cx="{x}" cy="{y}" r="46" fill="{c}" opacity="0.32"/><circle cx="{x + 28}" cy="{y - 22}" r="30" fill="{c}" opacity="0.28"/><circle cx="{x - 26}" cy="{y - 14}" r="26" fill="{c}" opacity="0.25"/></g>'
    s.append(f'<g id="w-holi" display="none">{holi}{puffs}</g>')
    koi = '<g class="a-koi"><g transform="translate(462 664) rotate(18)"><ellipse cx="0" cy="0" rx="12" ry="5" fill="#FFB020"/><path d="M-11 0 L-20 -6 L-18 0 L-20 6 Z" fill="#FF8A1F"/><circle cx="6" cy="-1" r="1.2" fill="#1D1E21"/><ellipse cx="2" cy="-2" rx="4" ry="2" fill="#FFF2D0" opacity="0.7"/></g></g>'
    s.append(f'<g id="w-koi" display="none">{koi}<g class="a-koi a-k2">{koi}</g></g>')
    gx, gy = 1935, 326
    s.append(f'<g id="w-owl" display="none"><ellipse cx="{gx - 30}" cy="{gy - 106}" rx="9" ry="12" fill="#7A5A3A"/><circle cx="{gx - 30}" cy="{gy - 118}" r="8" fill="#8A6A48"/><path d="M{gx - 37} {gy - 124} l2 -6 l3 5 Z M{gx - 23} {gy - 124} l-2 -6 l-3 5 Z" fill="#7A5A3A"/>'
             f'<g class="a-blink"><circle cx="{gx - 33}" cy="{gy - 119}" r="2.6" fill="#FFC21A"/><circle cx="{gx - 27}" cy="{gy - 119}" r="2.6" fill="#FFC21A"/></g><path d="M{gx - 31} {gy - 115} l1 2 l1 -2 Z" fill="#3A2416"/></g>')
    s.append('<g id="w-cat" display="none"><g class="a-breathe"><ellipse cx="1262" cy="622" rx="18" ry="8" fill="#E0A060"/><circle cx="1248" cy="618" r="7" fill="#E0A060"/><path d="M1243 613 l1 -6 l4 4 Z M1250 612 l2 -6 l3 5 Z" fill="#E0A060"/><path d="M1280 624 Q1292 626 1288 616" stroke="#E0A060" stroke-width="4" fill="none" stroke-linecap="round"/><path d="M1252 618 h-6" stroke="#8A5A2A" stroke-width="1.2"/><path d="M1258 616 q6 -3 14 0 M1262 622 q6 -2 12 0" stroke="#C07C40" stroke-width="2" fill="none"/></g></g>')
    s.append('<g id="w-banner9000" display="none"><g class="a-flag"><path d="M1454 366 L1494 366 L1494 520 L1474 508 L1454 520 Z" fill="#1D1E21"/><path d="M1454 366 L1494 366 L1494 520 L1474 508 L1454 520 Z" fill="none" stroke="#FFC21A" stroke-width="3"/><g fill="#FFC21A"><rect x="1462" y="410" width="7" height="7"/><rect x="1471" y="410" width="7" height="7"/><rect x="1471" y="401" width="7" height="7"/><rect x="1480" y="410" width="7" height="7"/><rect x="1480" y="401" width="7" height="7"/><rect x="1480" y="392" width="7" height="7"/></g><text x="1474" y="452" text-anchor="middle" font-family="IBM Plex Mono, monospace" font-weight="600" font-size="11" fill="#FFC21A">9000</text></g></g>')
    return ''.join(s)

def lights():
    s = []
    diyas = [(1000 + k * 34, 600) for k in range(13)] + [(1160 + k * 26, 642) for k in range(4)]
    diyas += [(x + w / 2, y) for i, (x, y, w, h) in enumerate(HILL_STEPS) if i % 3 == 0]
    d = ''
    for x, y in diyas:
        d += f'<g><circle class="a-glow" cx="{x:.0f}" cy="{y - 5:.0f}" r="10" fill="url(#glow)"/><path d="M{x - 5:.0f} {y - 1:.0f} Q{x:.0f} {y + 4:.0f} {x + 5:.0f} {y - 1:.0f} Z" fill="#B5653A"/><ellipse class="a-flicker" cx="{x:.0f}" cy="{y - 5:.0f}" rx="1.8" ry="3.6" fill="#FFC75A"/></g>'
    bulbs = ''.join(f'<circle class="a-twinkle a-d{k % 4}" cx="{986 + k * 15}" cy="{455 - 6 * math.sin(k / 29 * math.pi):.0f}" r="2.6" fill="{["#FFC21A", "#FF7A2E", "#FFF2B0"][k % 3]}"/>' for k in range(29))
    s.append(f'<g id="w-diwali" display="none">{d}<path d="M986 455 Q1200 443 1414 455" stroke="#3A2416" stroke-width="1" fill="none"/>{bulbs}</g>')
    fw = ''
    for k, (x, y, c) in enumerate([(640, 150, '#FFC21A'), (1250, 110, '#FF4FA3'), (1700, 170, '#7FE0FF'), (980, 200, '#FFFFFF'), (2100, 120, '#9CFF7A')]):
        rays = ''.join(f'<path d="M{x} {y} L{x + 46 * math.cos(a * math.pi / 8):.0f} {y + 46 * math.sin(a * math.pi / 8):.0f}"/>' for a in range(16))
        fw += f'<g class="a-burst a-b{k % 5}" stroke="{c}" stroke-width="2.4" stroke-linecap="round">{rays}<circle cx="{x}" cy="{y}" r="4" fill="{c}" stroke="none"/></g>'
    s.append(f'<g id="w-fireworks" display="none">{fw}</g>')
    return ''.join(s)

def hotspots():
    return ('<rect class="w-hot" data-act="go" data-view="cliff" x="0" y="100" width="440" height="560" fill="#000000" fill-opacity="0"><title>Climb the cliff</title></rect>'
            '<rect class="w-hot" data-act="go" data-view="yard" x="740" y="560" width="160" height="140" fill="#000000" fill-opacity="0"><title>Go to the yard</title></rect>'
            '<rect class="w-hot" data-act="poke" x="900" y="570" width="64" height="130" fill="#000000" fill-opacity="0"><title>Poke the dummy</title></rect>'
            '<rect class="w-hot" data-act="go" data-view="forge" x="2060" y="400" width="280" height="220" fill="#000000" fill-opacity="0"><title>Go to the forge</title></rect>'
            '<rect class="w-hot" data-act="go" data-view="dojo" x="960" y="170" width="560" height="480" fill="#000000" fill-opacity="0"><title>Go inside the dojo</title></rect>'
            '<rect class="w-hot" data-act="go" data-view="climb" x="1560" y="180" width="500" height="430" fill="#000000" fill-opacity="0"><title>Climb the hill</title></rect>'
            '<rect class="w-hot" data-act="go" data-view="boulders" x="1490" y="600" width="490" height="160" fill="#000000" fill-opacity="0"><title>See the boulders</title></rect>')

def build():
    body = [sky(), mountains(), village(), '<rect x="0" y="380" width="2400" height="220" fill="url(#haze)"/>',
            forest(430, 2400, lambda x: 560 + 14 * math.sin(x / 160), 50, 86, 5, 'url(#forestFar)'),
            '<path d="M0 620 Q600 590 1200 600 Q1800 610 2400 596 L2400 800 L0 800 Z" fill="url(#ground)"/>',
            hill(), cliff(), waterfall(), stream(), bridge(), paths(), cherry(), yard(), dojo(), boulders(), forge(), foreground(),
            '<g id="w-warm"><rect width="2400" height="800" fill="#FFB25A" opacity="0.05"/></g>', atmosphere(), night_overlay(), lights(), hotspots()]
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" class="scene valley" role="img" aria-label="Your training grounds">{defs()}{"".join(body)}</svg>'

if __name__ == '__main__':
    out = sys.argv[1]
    open(f'{out}/valley.svg', 'w').write(build())
