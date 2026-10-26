import math, random, sys
from build import defs, pine, smooth, pts


def svg(name, w, h, label, body):
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" class="scene place-{name}" role="img" aria-label="{label}">{defs()}{body}</svg>'


def night(w, h, glows=()):
    g = ''.join(f'<circle class="a-glow" cx="{x}" cy="{y}" r="{r}" fill="url(#glow)"/>' for x, y, r in glows)
    return f'<g id="n-night" display="none"><rect width="{w}" height="{h}" fill="#0D1636" opacity="0.5"/>{g}</g>'


def sky_bg(w, h, top='#5C93CC', mid='#A9C9E4', low='#EBDDBF'):
    random.seed(5)
    stars = ''.join(f'<circle cx="{random.randint(0, w)}" cy="{random.randint(6, int(h * 0.4))}" r="{random.choice([1, 1.4, 1.8])}" fill="#FFFFFF" opacity="0.8"/>' for _ in range(60))
    return (f'<defs><linearGradient id="psky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{top}"/><stop offset="0.55" stop-color="{mid}"/><stop offset="1" stop-color="{low}"/></linearGradient></defs>'
            f'<rect width="{w}" height="{h}" fill="url(#psky)"/><g id="n-nightsky" display="none"><rect width="{w}" height="{h}" fill="#16224A" opacity="0.8"/>{stars}</g>')


def cliff():
    W, H = 900, 1600
    random.seed(21)
    s = [sky_bg(W, H)]
    s.append('<polygon points="0,700 120,560 230,640 330,520 430,620 430,1100 0,1100" fill="#9DB1CB"/><polygon points="600,560 720,430 820,520 900,470 900,1100 600,1100" fill="#9DB1CB"/>')
    face = [(150, 1600), (160, 1300), (140, 1000), (170, 700), (150, 420), (190, 200), (240, 150), (420, 132), (600, 120), (760, 150), (900, 170), (900, 1600)]
    s.append(f'<polygon points="{pts(face)}" fill="url(#rock)"/>')
    s.append('<g stroke="#4B5058" stroke-width="2.5" fill="none" opacity="0.5">' + ''.join(f'<path d="M{random.randint(200, 420)} {y} L{random.randint(600, 880)} {y + random.randint(-14, 14)}"/>' for y in range(240, 1500, 90)) + '</g>')
    s.append('<g fill="#A3A8AF" opacity="0.45">' + ''.join(f'<path d="M{x} {y} l{random.randint(50, 110)} 8 l-4 18 l-{random.randint(50, 100)} -6 Z"/>' for x, y in [(620, 300), (700, 520), (250, 640), (660, 880), (300, 1060), (720, 1180), (260, 1330)]) + '</g>')
    s.append('<path d="M150 420 Q130 300 190 200 L240 150 L420 132 L600 120 L760 150 L900 170 L900 196 L760 176 L600 146 L420 158 L250 176 L204 222 Q160 310 172 420 Z" fill="#5E8A4A"/>')
    s.append(pine(300, 140, 80) + pine(660, 128, 70) + pine(820, 162, 64))
    fall = [(70, 300), (110, 296), (150, 300), (160, 1500), (60, 1500)]
    s.append('<path d="M60 300 Q110 290 160 300 L166 1500 L54 1500 Z" fill="url(#fall)"/>')
    for k in range(30):
        x = 64 + k * 3.3
        s.append(f'<path class="a-fall a-d{k % 4}" d="M{x:.1f} {random.randint(310, 400)} L{x + (x - 110) * 0.05:.1f} {random.randint(1100, 1480)}" stroke="#FFFFFF" stroke-width="{random.choice([1, 1.5, 2])}" opacity="{random.uniform(0.5, 0.95):.2f}"/>')
    s.append('<path d="M0 300 L60 300 L54 1500 L0 1500 Z" fill="url(#rock)"/>')
    s.append('<ellipse cx="200" cy="1530" rx="260" ry="40" fill="url(#water)"/><ellipse class="a-mist" cx="110" cy="1480" rx="140" ry="50" fill="url(#mist)"/><g class="a-foam" fill="#FFFFFF" opacity="0.9"><ellipse cx="110" cy="1500" rx="70" ry="12"/></g>')
    s.append('<path d="M0 1560 Q450 1520 900 1550 L900 1600 L0 1600 Z" fill="#6E9A4C"/>')
    rx = 520
    s.append(f'<rect x="{rx - 40}" y="130" width="80" height="16" fill="url(#wood)"/><rect x="{rx - 6}" y="112" width="12" height="30" fill="#5E3920"/>')
    s.append(f'<path d="M{rx} 146 Q{rx + 8} 800 {rx - 4} 1520" stroke="#C9A46A" stroke-width="7" fill="none"/><path d="M{rx} 146 Q{rx + 8} 800 {rx - 4} 1520" stroke="#8F6E3E" stroke-width="2" fill="none" stroke-dasharray="4 7"/>')
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
    s.append(night(W, H))
    return svg('cliff', W, H, 'The cliff climb', ''.join(s))


def yard():
    W, H = 900, 1300
    random.seed(31)
    s = [sky_bg(W, H)]
    s.append('<polygon points="0,560 150,440 290,520 430,400 560,500 700,420 900,520 900,760 0,760" fill="#93A9C4"/>')
    s.append(''.join(pine(x, 700 + random.randint(0, 30), random.randint(110, 170), '#3A6650', '#4A7A60') for x in range(-20, 940, 46)))
    s.append('<path d="M0 720 Q450 690 900 720 L900 1300 L0 1300 Z" fill="url(#ground)"/>')
    s.append('<ellipse cx="450" cy="1010" rx="460" ry="190" fill="url(#dirt)"/><ellipse cx="450" cy="1000" rx="400" ry="150" fill="#DCC292" opacity="0.6"/>')
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
    s.append(f'<g id="n-dummy"><ellipse cx="{x - 14}" cy="{y + 6}" rx="50" ry="10" fill="#2B1E10" opacity="0.3"/><rect x="{x - 8}" y="{y - 250}" width="16" height="250" fill="url(#wood)"/><rect x="{x - 60}" y="{y - 186}" width="120" height="16" fill="url(#wood)"/>'
             f'<path d="M{x - 34} {y - 214} Q{x} {y - 232} {x + 34} {y - 214} L{x + 40} {y - 70} Q{x} {y - 52} {x - 40} {y - 70} Z" fill="#D9BC7C"/><path d="M{x - 36} {y - 170} Q{x} {y - 158} {x + 36} {y - 170} M{x - 38} {y - 116} Q{x} {y - 104} {x + 38} {y - 116}" stroke="#A88746" stroke-width="3" fill="none"/>'
             f'<circle cx="{x}" cy="{y - 238}" r="28" fill="#D9BC7C"/><rect x="{x - 26}" y="{y - 252}" width="52" height="10" fill="#FFC21A"/><path class="a-flag" d="M{x + 26} {y - 250} L{x + 56} {y - 260} L{x + 52} {y - 238} Z" fill="#FFC21A"/></g>')
    s.append(f'<g id="n-vines" display="none">{"".join(vines)}</g>')
    s.append(''.join(f'<use href="#tuft" transform="translate({random.randint(0, 900)} {random.randint(1180, 1295)}) scale(1.4)"/>' for _ in range(30)))
    s.append(night(W, H))
    return svg('yard', W, H, 'The push yard', ''.join(s))


def forge():
    W, H = 900, 1300
    random.seed(41)
    s = ['<rect width="900" height="1300" fill="url(#plank)"/>']
    s.append('<g stroke="#55361F" stroke-width="2">' + ''.join(f'<path d="M0 {y} H900"/>' for y in range(60, 900, 56)) + '</g>')
    s.append('<g fill="#4A2E1A">' + ''.join(f'<rect x="{x}" y="0" width="14" height="900"/>' for x in (0, 300, 600, 886)) + '</g>')
    s.append('<path d="M0 900 L900 900 L900 1300 L0 1300 Z" fill="#6B6F76"/><g stroke="#55595F" stroke-width="2">' + ''.join(f'<path d="M0 {y} H900"/>' for y in (960, 1040, 1140, 1260)) + '</g>')
    s.append('<path d="M60 380 L320 380 L300 300 L80 300 Z" fill="#5F636A"/><rect x="150" y="0" width="80" height="300" fill="#7E828A"/><rect x="60" y="560" width="260" height="340" fill="#8C9096"/><g stroke="#6E7278" stroke-width="2"><path d="M60 640 H320 M60 720 H320 M60 800 H320 M150 560 V640 M240 640 V720 M120 720 V800 M260 720 V800"/></g>')
    s.append('<rect x="90" y="470" width="200" height="94" fill="#2E2A28"/>')
    s.append('<g id="n-fire"><circle class="a-glow" cx="190" cy="520" r="220" fill="url(#glow)"/><ellipse cx="190" cy="556" rx="96" ry="18" fill="url(#coal)"/>'
             '<path class="a-flicker" d="M150 556 Q140 520 160 494 Q166 520 176 506 Q180 470 196 452 Q204 490 214 478 Q228 506 222 530 Q236 520 236 556 Z" fill="#FF9A2E"/>'
             '<path class="a-flicker a-d2" d="M170 556 Q166 530 180 512 Q186 530 192 520 Q200 500 208 494 Q214 520 212 556 Z" fill="#FFE08A"/></g>')
    s.append('<g id="n-cold" display="none"><ellipse cx="190" cy="556" rx="96" ry="16" fill="#5A5C61"/><g fill="#7E8186"><circle cx="160" cy="550" r="6"/><circle cx="196" cy="546" r="7"/><circle cx="224" cy="552" r="5"/></g></g>')
    rack_x0, rack_y0 = 400, 150
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
    ax, ay = 540, 1080
    s.append(f'<ellipse cx="{ax}" cy="{ay + 110}" rx="170" ry="22" fill="#2B1E10" opacity="0.35"/><rect x="{ax - 60}" y="{ay}" width="120" height="110" fill="#6E4428"/><ellipse cx="{ax}" cy="{ay}" rx="60" ry="14" fill="#A06C43"/>')
    s.append(f'<path d="M{ax - 130} {ay - 70} h220 l-26 30 h-40 v40 h-60 v-40 h-40 Z" fill="#2E3035"/><path d="M{ax - 126} {ay - 70} h212" stroke="#5F636A" stroke-width="5"/>')
    s.append(f'<path d="M{ax + 40} {ay - 150} L{ax + 110} {ay - 76}" stroke="#6E4428" stroke-width="12" stroke-linecap="round"/><rect x="{ax + 16}" y="{ay - 176}" width="54" height="30" fill="#3A3C42" transform="rotate(45 {ax + 43} {ay - 161})"/>')
    s.append('<ellipse cx="790" cy="1190" rx="70" ry="18" fill="#2B1E10" opacity="0.3"/><rect x="730" y="1050" width="120" height="140" fill="#6E4428"/><g stroke="#4A2E1A" stroke-width="5"><path d="M730 1080 H850 M730 1160 H850"/></g><ellipse cx="790" cy="1050" rx="60" ry="14" fill="#8FC4D8"/>')
    s.append(night(W, H, [(190, 520, 260)]))
    return svg('forge', W, H, 'The forge', ''.join(s))


def boulders():
    W, H = 900, 1300
    random.seed(51)
    s = [sky_bg(W, H)]
    s.append('<polygon points="0,520 160,400 300,480 460,380 620,470 780,400 900,450 900,700 0,700" fill="#93A9C4"/>')
    s.append('<rect x="0" y="560" width="900" height="120" fill="#C9BCA2"/><rect x="0" y="548" width="900" height="16" fill="#5E3920"/><g fill="#A99B80">' + ''.join(f'<rect x="{x}" y="564" width="2" height="116"/>' for x in range(0, 900, 60)) + '</g>')
    s.append(pine(80, 600, 190, '#2F5B47', '#3E6F57') + pine(830, 600, 210, '#2F5B47', '#3E6F57'))
    s.append('<path d="M0 680 L900 680 L900 1300 L0 1300 Z" fill="#D9D3C4"/>')
    s.append('<g stroke="#BDB5A2" stroke-width="2" fill="none">' + ''.join(f'<path d="M0 {y} Q225 {y - 6} 450 {y} Q675 {y + 6} 900 {y}"/>' for y in range(700, 1300, 22)) + '</g>')
    spots = []
    for row, (y, k, xs) in enumerate([(800, 0.55, (170, 340, 560, 730)), (960, 0.75, (130, 340, 560, 770)), (1160, 1.0, (150, 450, 750))]):
        for x in xs:
            spots.append((x, y, k))
    for i, (x, y, k) in enumerate(spots[:12]):
        r = 70 * k
        s.append(f'<g class="u" data-i="{i}" data-y="{y:.0f}">'
                 f'<g class="u-on"><ellipse cx="{x}" cy="{y + 4}" rx="{r * 1.2:.0f}" ry="{12 * k:.0f}" fill="#2B1E10" opacity="0.25"/>'
                 f'<path d="M{x - r:.0f} {y:.0f} Q{x - r * 1.05:.0f} {y - r * 1.1:.0f} {x - 10 * k:.0f} {y - r * 1.25:.0f} L{x - 4 * k:.0f} {y:.0f} Z" fill="url(#boulder)"/>'
                 f'<path d="M{x + 10 * k:.0f} {y:.0f} L{x + 16 * k:.0f} {y - r * 1.25:.0f} Q{x + r * 1.05:.0f} {y - r * 1.1:.0f} {x + r:.0f} {y:.0f} Z" fill="url(#boulder)"/>'
                 f'<path d="M{x - 10 * k:.0f} {y - r * 1.25:.0f} L{x - 4 * k:.0f} {y:.0f} L{x + 2 * k:.0f} {y:.0f} L{x - 2 * k:.0f} {y - r * 1.25:.0f} Z" fill="url(#cut)"/>'
                 f'<text class="u-label" x="{x + r * 0.5:.0f}" y="{y - r * 0.4:.0f}" text-anchor="middle" font-family="IBM Plex Mono, monospace" font-weight="600" font-size="{18 * k:.0f}" fill="#3A3D44"></text></g>'
                 f'<g class="u-ghost"><ellipse cx="{x}" cy="{y + 4}" rx="{r * 1.2:.0f}" ry="{12 * k:.0f}" fill="#2B1E10" opacity="0.25"/><path d="M{x - r:.0f} {y:.0f} Q{x - r:.0f} {y - r * 1.3:.0f} {x:.0f} {y - r * 1.3:.0f} Q{x + r:.0f} {y - r * 1.3:.0f} {x + r:.0f} {y:.0f} Z" fill="url(#boulder)"/>'
                 f'<path d="M{x + r * 0.2:.0f} {y - r * 1.28:.0f} L{x + r * 0.2:.0f} {y - r * 1.8:.0f}" stroke="#4A2E1A" stroke-width="{3 * k:.1f}"/><path class="a-flag" d="M{x + r * 0.2:.0f} {y - r * 1.8:.0f} L{x + r * 0.2 + 28 * k:.0f} {y - r * 1.72:.0f} L{x + r * 0.2:.0f} {y - r * 1.62:.0f} Z" fill="#FFC21A"/></g>'
                 f'<ellipse class="u-off" cx="{x}" cy="{y - 2}" rx="{r:.0f}" ry="{18 * k:.0f}" fill="none" stroke="#9E9682" stroke-width="2" stroke-dasharray="6 5"/></g>')
    s.append('<use href="#toro" transform="translate(60 1240) scale(1.6)"/><use href="#toro" transform="translate(860 1240) scale(1.6)"/>')
    s.append(night(W, H, [(60, 1160, 80), (860, 1160, 80)]))
    return svg('boulders', W, H, 'The boulder garden', ''.join(s))


if __name__ == '__main__':
    out = sys.argv[1]
    for name, fn in (('cliff', cliff), ('yard', yard), ('forge', forge), ('boulders', boulders)):
        open(f'{out}/{name}.svg', 'w').write(fn())
